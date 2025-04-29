from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import socket
import uvicorn
import json
import os
from gpiozero import Button
import asyncio
import threading
import time
import httpx
from dbconnect_new import dbConnect_new
from tinydb import Query,TinyDB
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
app = FastAPI()
states = ""
wiegand_halt_open_check = {}
from datetime import datetime
check_is_halt_open = 0
raspberry_pi_ip = "172.16.1.195"
mysql_ip = "172.16.1.100"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#定義tinyDB連接的資料庫，使用的是產生同步好的json檔案
db = TinyDB("door_control_system.json")
unsyncdb = TinyDB("unsync_data.json")
# 全局設置事件循環
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class GPIOMonitor(FileSystemEventHandler):
    def __init__(self, pin_numbers,db_instance,unsync_db_instance):
        self.pins = {}
        self.connections = set()
        self.running = True
        self.previous_states = {}
        self.door_sensor_dict = {}
        self.door_threads = {}
        self.http_client = httpx.Client(timeout=2.0)
        
        self.unsyncdb = unsync_db_instance
        #未同步的事件狀態
        self.unsync_event_table = self.unsyncdb.table("unsync_event_table")
        #未同步的ControllerOutput狀態
        self.unsync_event_output_table = self.unsyncdb.table("unsync_event_output_table")
        #未同步的eventLog狀態
        self.unsync_event_log_table = self.unsyncdb.table("unsync_event_log_table")
        #==============
        self.db = db_instance
        self.doorsetting_table = self.db.table("doorsetting")
        self.eventAction_table = self.db.table("eventAction")
        self.controllerInput_table = self.db.table("controllerInput")
        self.controllerOutput_table = self.db.table("controllerOutput")
        self.door_status_table = self.db.table("door_status")
        self.query_table = Query()
        # 初始化 GPIO，使用 Button，
        for pin in pin_numbers:
            button = Button(pin, pull_up=True, bounce_time=0.1)
            self.pins[pin] = button
            self.previous_states[pin] = button.is_pressed  # 使用 is_pressed 替代 value
            
            # 設置回調函數來處理狀態變化
            button.when_pressed = lambda p=pin: self.handle_state_change(p, True)
            button.when_released = lambda p=pin: self.handle_state_change(p, False)
        
        # 預先獲取門的設置信息，以減少後續查詢
        self.cache_door_settings()
    def on_modified(self, event):
        if event.src_path.endswith('door_control_system.json'):
            print("檢測到文件變更，重新加載數據庫")
            self.db.close()
            self.db = TinyDB('door_control_system.json')
            self.doorsetting_table = self.db.table("doorsetting")
            self.eventAction_table = self.db.table("eventAction")
            self.controllerInput_table = self.db.table("controllerInput")
            self.controllerOutput_table = self.db.table("controllerOutput")
            self.door_status_table = self.db.table("door_status")
            self.query_table = Query()
            self.cache_door_settings()
    def cache_door_settings(self):
        """預先緩存門的設置信息"""
        self.door_settings = {}
        for pin in self.pins.keys():
            door_info= self.doorsetting_table.search((self.query_table.door_sensor == str(pin))&(self.query_table.control == raspberry_pi_ip)) 
            #door_info = dbConnect_new("SELECT * FROM doorsetting WHERE door_sensor = %s and control = %s", (pin, raspberry_pi_ip))
            print(door_info)
            if door_info:
                self.door_settings[pin] = door_info[0]
                # 預取door_status表中的信息
                door_status = self.door_status_table.search(self.query_table.doorname == door_info[0]['door'])
                #door_status = dbConnect_new("SELECT * FROM door_status WHERE doorname = %s", (door_info[0]['door'],))
                if door_status:
                    self.door_settings[pin]['door_status'] = door_status[0]
    
    def handle_state_change(self, pin, is_pressed):
        """處理GPIO狀態變化的回調函數"""
        # 確保狀態實際發生了變化
        if self.previous_states.get(pin) == is_pressed:
            return
            
        self.previous_states[pin] = is_pressed
        
        # 使用一個單獨的線程來處理狀態變化邏輯，避免阻塞回調
        threading.Thread(target=self.process_state_change, args=(pin, is_pressed), daemon=True).start()
    
    def process_state_change(self, pin, is_pressed):
        """在單獨的線程中處理狀態變化邏輯"""
        # 從緩存中獲取門的信息
        door_info = self.door_settings.get(pin)
        # 準備狀態消息
        if door_info:
            # 門狀態處理
            state_status = 'closed' if is_pressed else 'open'
            door_name = door_info['door']
            #檢查是否還有觸發開門過久，在開門的時候檢測
            wiegand_halt_open_check[pin] = False
            # 檢查強迫開門
            if state_status == "open":
                with open("./permition/checkwiegand1permition.conf", "r") as readpermition:
                    if readpermition.read().strip() == "0":
                        state_status = "ForceOpen"
                    else:
                        # 啟動門開啟計時器，如果之前有線程正在運行，先停止它
                        if door_name in self.door_threads and self.door_threads[door_name].is_alive():
                            # 不能直接停止線程，但我們可以設置一個標誌來讓它自己退出
                            pass
                        
                        # 創建新的開門計時線程
                        self.door_threads[door_name] = threading.Thread(
                            target=self.limittime, 
                            args=(int(door_info.get('openTimeLimit', 30)), pin, door_name,door_info),
                            daemon=True
                        )
                        self.door_threads[door_name].start()
            print(wiegand_halt_open_check[pin])
            if(wiegand_halt_open_check[pin]):
                if (is_pressed):
                    states = "閉合(Close)"
                    wiegand_halt_open_check[pin] = False
                else:
                    states = "開路(Open)開門過久"
                state_message = {
                    'door_status_id': door_info.get('door_status', {}).get('id', 0),
                    'pin': pin,
                    'state': states,
                    'states': "HaltOpen",
                    'value': is_pressed
                }
            else:
                state_message = {
                    'door_status_id': door_info.get('door_status', {}).get('id', 0),
                    'pin': pin,
                    'state': "閉合(Close)" if is_pressed else "開路(Open)",
                    'states': state_status,
                    'value': is_pressed
                }
            
            # 打印日誌
            if is_pressed:
                print(f"門號:{door_name} 關閉")
            else:
                print(f"門號:{door_name} {state_status}")
        else:
            # 普通GPIO處理
            state_message = {
                'pin': pin,
                'state': "閉合(Close)" if is_pressed else "開路(Open)",
                'value': is_pressed
            }
            # 打印日誌
            if is_pressed:
                print(f"Input{pin} 乾接點關閉")
            else:
                print(f"Input{pin} 乾接點打開")
        
        # 將廣播任務提交給事件循環並且將目前門的狀態藉由broadcast_update來去發送到WebSocket Client前端網頁
        asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), loop)
    async def broadcast_update(self, message):
        """向所有連接的客戶端廣播更新"""
        dead_connections = set()
        for websocket in self.connections:
            try:
                await websocket.send_json(message)
            except:
                dead_connections.add(websocket)
        # 移除斷開的連接
        self.connections -= dead_connections
    def limittime(self, openlimit, pin, doorname,door_info):
        """監控門打開時間的函數"""
        start_time = time.time()
        
        while True:
            # 獲取當前狀態
            current_status = self.previous_states.get(pin)
            elapsed_time = time.time() - start_time
            
            # 如果門已關閉或超時，則退出
            if current_status or elapsed_time >= openlimit:
                break
            
            # 輸出狀態但降低頻率
            if int(elapsed_time) % 5 == 0:  # 只在5秒的倍數時輸出
                print(f"門 {doorname} 尚未關門持續 {int(elapsed_time)} 秒")
            
            time.sleep(1)  # 每秒檢查一次
        
        # 檢查是否因為超時而退出
        if elapsed_time >= openlimit and not current_status:
            print(f"警報！門 {doorname} 開啟過久！")
            # 使用一個單獨的線程處理事件觸發
            threading.Thread(target=self.trigger_halt_open_event, args=(doorname,door_info,pin), daemon=True).start()
    
    def trigger_halt_open_event(self, doorname,door_info,pin):
        """觸發開門過久事件"""
        get_event = self.eventAction_table.search((self.query_table.doorName == doorname)&(self.query_table.eventClass == "HaltOpen"))
        #get_event = dbConnect_new("SELECT * FROM eventAction WHERE doorName=%s AND eventClass=%s", (doorname, "HaltOpen"))
        if not get_event:
            print(f"{doorname} not have haltopen event so do noting!")
            return
        wiegand_halt_open_check[pin] = True
        state_message = {
                'door_status_id': door_info.get('door_status', {}).get('id', 0),
                'state': "開門過久",
                'states':"HaltOpen"
        }
        # 將廣播任務提交給事件循環
        asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), loop)
        #判斷是否有連線到mysql server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((mysql_ip,13306))
        print(f"是否有連線到mysql serevr:{result}")
        if (result == 0):
            print("connect mysql server successful!")
            #新增開門過久事件log到mysql
            getnowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #dbConnect_new("INSERT INTO eventLog(eventName,eventClass,eventCause,timeToEvent,eventStatus)VALUES(%s,%s,%s,%s,%s)",True,(get_event[0]['eventName'],"HaltOpen","systemAction",getnowtime,"unconfirmed"))
            dbConnect_new("INSERT INTO eventLog(eventName,eventClass,eventCause,timeToEvent,eventStatus)VALUES(%s,%s,%s,%s,%s)", True, (get_event[0]['eventName'], "HaltOpen", "systemAction", getnowtime, "unconfirmed"))
            dbConnect_new("UPDATE eventAction SET eventStat = %s where eventName = %s ",True,("active",get_event[0]['eventName']))
        else:
            print("No connect mysql server!")
            getnowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            event_log_file_path = "unSyncEventlog.json"
            event_action_status = "event_action.json"
            new_unsync_event = {
                "eventName": get_event[0]['eventName'],
                "eventClass": "HaltOpen",
                "eventCause": "systemAction",
                "timeToEvent": getnowtime,
                "eventStatus": "unconfirmed"   
            }
            update_event_action_data = {
                "eventName":get_event[0]['eventName'],
                "status": "active"
            }
            Event = Query()
            self.unsync_event_log_table.upsert(
                new_unsync_event,
                (Event.eventName == new_unsync_event["eventName"])
            )
            #self.unsync_data(event_log_file_path,new_unsync_event)
            #self.unsync_data(event_action_status,update_event_action_data)
        output_names = get_event[0]['outputPort'].split(",")
        # 用於儲存按 controller 分組的結果
        controller_groups = {}
        # 遍歷每個 outputName
        for output in output_names:
            # 查詢符合 outputName 的記錄
            output_results = self.controllerOutput_table.search(self.query_table.outputName == output)
            
            # 遍歷查詢結果
            for item in output_results:
                controller = item['controller']
                port = item['outputPort']
                
                # 如果這個 controller 尚未在分組字典中，創建一個新的列表
                if controller not in controller_groups:
                    controller_groups[controller] = []
                
                # 將 port 添加到相應的 controller 組
            controller_groups[controller].append(port)
        # listoutputpin = dbConnect_new(
        #     "SELECT controller, GROUP_CONCAT(outputPort ORDER BY outputPort) AS outputPort "
        #     "FROM DoorSecurity.controllerOutput "
        #     "WHERE FIND_IN_SET(outputName, %s) > 0 GROUP BY controller",
        #     (get_event[0]['outputPort'],)
        # )
        thread_task = {}
        for controller, ports in controller_groups.items():
            thread_task[controller] = threading.Thread(target=self.send_event_action,args=(ports,controller,get_event[0]['eventName']))
            thread_task[controller].start()
        # for controller_output in listoutputpin:
        #     self.send_event_action(controller_output, get_event[0])
    def unsync_data(self, file_path, data):
        # 使用線程鎖來確保一次只有一個線程可以訪問文件
        lock = threading.Lock()
        with lock:
            try:
                # 檢查文件是否存在或為空
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump([], file)
                
                # 讀取文件內容
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read().strip()
                        if content:
                            events = json.loads(content)
                        else:
                            events = []
                except json.JSONDecodeError:
                    # 如果 JSON 解析失敗，重置為空列表
                    events = []
                
                # 確保 events 是列表
                if not isinstance(events, list):
                    events = [events] if events else []
                
                # 添加新數據
                events.append(data)
                
                # 寫回文件
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(events, file, ensure_ascii=False, indent=4)
                    
                print(f"已添加新事件，目前尚未同步的資料共有 {len(events)} 條記錄")
            
            except Exception as e:
                print(f"處理未同步數據錯誤: {e}")
                # 確保即使出錯也能寫入數據
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump([data], file, ensure_ascii=False, indent=4)
                    print("已重設並添加新事件")
                except Exception as write_error:
                    print(f"重置文件錯誤: {write_error}")
    # def unsync_data(self,file_path,data):
    #     if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
    #             with open(file_path, "w", encoding="utf-8") as file:
    #                 json.dump([], file)
    #     with open(file_path, "r", encoding="utf-8") as file:
    #         events = json.load(file)
    #     events.append(data)
    #     with open(file_path, "w", encoding="utf-8") as file:
    #         json.dump(events, file, ensure_ascii=False, indent=4)
    #     print(f"已添加新事件，目前尚未同步的資料共有 {len(events)} 條記錄")
    #會把controllerOutput的Port從非作用中改為作用中
    def update_outputPort_status(self,outputPort,controller,check):
        for output in outputPort:
            if check == 0:
                print("有執行到將output寫入到資料庫")
                dbConnect_new("UPDATE controllerOutput SET outputStat = %s where outputPort = %s and controller = %s",True,("active",output,controller))
            else:
                print("No connect mysql server!")
                print(f"正在將這一筆輸出加入到未同步清單:{output}")
                controller_output_file_path = "unSyncControllerOutput.json"
                new_unsync_controller_output = {
                    "controller": controller,
                    "outputPort": output,
                    "outputStat": "active"
                }
                self.unsync_data(controller_output_file_path,new_unsync_controller_output)
    #確認mysql是否可以正常連線
    async def check_port_async(host, port, timeout=1):
        try:
            # 使用帶超時的連接協程
            fut = asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(fut, timeout=timeout)
            # 關閉連接
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False
    #發送事件的Output port號碼與eventname的資訊到Output控制器程式，利用API方式進行
    def send_event_action(self, controller_output,controller_ip, event):
        """發送事件動作到控制器"""
        eventAction_url = f"http://{controller_ip}:5020/eventaction/output/active"
        check_controller_output_status = f"http://{controller_ip}:5020/api/output/status"
        dict_output = {
            "outputPort": controller_output,
            "eventName": event
        }
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((mysql_ip,13306))
        print(f"controller output list is {controller_output}")
        self.update_outputPort_status(controller_output,controller_ip,result)
        try:
            # 使用with語句確保及時釋放資源
            # with httpx.Client(timeout=5.0) as client:  # 設置超時
                # 檢查服務器狀態
                response = self.http_client.get(check_controller_output_status)
                if response.status_code == 200:
                    # 發送事件
                    response = self.http_client.post(eventAction_url, json=dict_output)
                    print(f"事件發送成功: {response.json()}")
                else:
                    print(f"連接失敗，狀態碼: {response.status_code}")
        except httpx.ConnectError:
            print("錯誤: 連線不到服務器")
        except Exception as e:
            print(f"錯誤: {str(e)}")

    def get_current_door_states(self):
        """獲取所有門的當前狀態"""
        current_states = []
        
        for pin, door_info in self.door_settings.items():
            if 'door_status' in door_info:
                current_state = self.previous_states.get(pin)
                state_status = 'closed' if current_state else 'open'
                
                # 檢查是否為強迫開門
                if state_status == "open":
                    with open("./permition/checkwiegand1permition.conf", "r") as readpermition:
                        if readpermition.read().strip() == "0":
                            state_status = "ForceOpen"
                        else:
                            if (wiegand_halt_open_check[pin]):
                                state_status = "HaltOpen"
                state_info = {
                    'door_status_id': door_info['door_status']['id'],
                    'states': state_status
                }
                current_states.append(state_info)
        
        return current_states

    

    def get_all_states(self):
        """獲取所有 GPIO 的當前狀態"""
        return {
            pin: "閉合(Close)" if button.is_pressed else "開路(Open)"
            for pin, button in self.pins.items()
        }

    async def register(self, websocket: WebSocket):
        """處理新的 WebSocket 連接"""
        await websocket.accept()
        self.connections.add(websocket)
        try:
            # 發送初始門狀態
            initial_states = self.get_current_door_states()
            for state in initial_states:
                await websocket.send_json(state)
            
            # 保持連接
            while True:
                try:
                    await websocket.receive_text()
                except:
                    break
        finally:
            self.connections.remove(websocket)

    def cleanup(self):
        """清理資源"""
        self.running = False
        for button in self.pins.values():
            button.close()

# 創建並啟動事件循環線程
def start_event_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

event_loop_thread = threading.Thread(target=start_event_loop, daemon=True)
event_loop_thread.start()

# 創建 GPIO 監控器實例
monitor = GPIOMonitor([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],db,unsyncdb)
# 創建觀察者
observer = Observer()
observer.schedule(monitor, path='.', recursive=False)
observer.start()
observer.join
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await monitor.register(websocket)
@app.get("/")
async def get_current_states():
    return monitor.get_all_states()

if __name__ == "__main__":
    try:
        print("Starting GPIO monitor server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        print("Cleaning up...")
        monitor.cleanup()
        # 關閉事件循環
        loop.call_soon_threadsafe(loop.stop)
        event_loop_thread.join(timeout=1.0)