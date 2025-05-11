from fastapi import FastAPI, WebSocket,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gpiozero import Button  # 改用 Button
import asyncio
import threading
import time
import httpx
from tinydb import TinyDB,Query
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
from dotenv import load_dotenv
import sys,os,subprocess,re
import module.drycontact as drycontact
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connect.dbconnect_new import dbConnect_new
import tinydb_encrpy.tinydb_sync_no_api as tinycon
app = FastAPI()
db_path = "secure_data/encrypted_db.json"
key_path = "secure_data/db.key"
key = tinycon.get_encryption_key(key_path)
wiegand_halt_open_check = {}
def get_eth0_ip(interface):
    try:
        output = subprocess.check_output("ip addr show "+interface, shell=True, text=True)
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
        if match:
            return match.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        return None
raspberry_pi_ip = get_eth0_ip("wlan0")
with open("../mysql_config/mysql_ip.conf","r") as mysql_config:
    mysql_ip = mysql_config.read().strip()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#定義tinyDB連接的資料庫，使用的是產生同步好的json檔案
#db = TinyDB("door_control_system.json")
#unsyncdb = TinyDB("unsync_data.json")
# 全局設置事件循環
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
def check_port_with_socket(host, port, timeout=2):
    start_time = time.time()
    # 創建套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 設置超時
    s.settimeout(timeout)
    try:
        # 嘗試連接
        result = s.connect_ex((host, port))
        success = (result == 0)
        # 優雅關閉
        if success:
            s.shutdown(socket.SHUT_RDWR)
    except (socket.timeout, socket.error) as e:
        print(f"連接錯誤: {e}")
        success = False
    finally:
        s.close()
    duration = time.time() - start_time
    print(f"檢查耗時: {duration:.2f} 秒")
    return success
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
class GPIOMonitor(FileSystemEventHandler):
    #def __init__(self, pin_numbers,db_instance,unsync_db_instance):
    def __init__(self, pin_numbers):
        self.pins = {}
        self.connections = set()
        self.running = True
        self.previous_states = {}
        self.door_sensor_dict = {}
        self.door_threads = {}
        self.http_client = httpx.Client(timeout=2.0)
        self.db = tinycon.EncryptedTinyDB(db_path,key)
        # self.unsyncdb = unsync_db_instance
        # #未同步的事件狀態
        # self.unsync_event_table = self.unsyncdb.table("unsync_event_table")
        # #未同步的ControllerOutput狀態
        # self.unsync_event_output_table = self.unsyncdb.table("unsync_event_output_table")
        # #未同步的eventLog狀態
        # self.unsync_event_log_table = self.unsyncdb.table("unsync_event_log_table")
        # #==============
        # self.db = db_instance
        self.doorsetting_table = self.db.table("doorsetting")
        self.eventAction_table = self.db.table("eventAction")
        self.controllerInput_table = self.db.table("controllerInput")
        self.controllerOutput_table = self.db.table("controllerOutput")
        self.door_status_table = self.db.table("door_status")
        self.query_table = Query()
        self.drycontact = drycontact.drycontact(self.eventAction_table,self.controllerOutput_table,self.query_table)

        # 初始化 GPIO，使用 Button，
        for pin in pin_numbers:
            button = Button(pin, pull_up=True,bounce_time=0.1)
            self.pins[pin] = button
            self.previous_states[pin] = button.is_pressed  # 使用 is_pressed 替代 value
            # 設置回調函數來處理狀態變化
            button.when_pressed = lambda p=pin: self.handle_state_change(p, True)
            button.when_released = lambda p=pin: self.handle_state_change(p, False)
        # # 啟動監控線程
        # self.monitor_thread = threading.Thread(target=self.monitor_gpio)
        # self.monitor_thread.daemon = True
        # self.monitor_thread.start()
    # 預先獲取門的設置信息，以減少後續查詢
        self.cache_door_settings()
    #用來處理input的開啟與關閉事件
    def handle_state_change(self, pin, is_pressed):
        """處理GPIO狀態變化的回調函數"""
        # 確保狀態實際發生了變化
        if self.previous_states.get(pin) == is_pressed:
            return
        self.previous_states[pin] = is_pressed
        # 使用一個單獨的線程來處理狀態變化邏輯，避免阻塞回調
        threading.Thread(target=self.monitor_gpio, args=(pin, is_pressed), daemon=True).start()
    def process_state_change(self, pin, is_pressed):
        """在單獨的線程中處理狀態變化邏輯"""
        # 從緩存中獲取門的信息
        door_info = self.door_settings.get(pin)
        wiegand_halt_open_check[pin] = False
        # 準備狀態消息
        if door_info:
            # 門狀態處理
            state_status = 'closed' if is_pressed else 'open'
            door_name = door_info['door']
            #檢查是否還有觸發開門過久，在開門的時候檢測
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
    #在單獨的thread裡面監控每個port的狀態
    def monitor_gpio(self,pin,is_pressed):
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
                self.drycontact.drycontact_open(pin)
                print(f"Input{pin} 乾接點打開")
        
        # 將廣播任務提交給事件循環並且將目前門的狀態藉由broadcast_update來去發送到WebSocket Client前端網頁
        asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), loop)
    #檢測到TinyDB有異動就重新加載資料庫
    # def on_modified(self, event):
    #     if event.src_path.endswith('door_control_system.json'):
    #         print("檢測到文件變更，重新加載資料庫")
    #         self.db.close()
    #         self.db = TinyDB('door_control_system.json')
    #         self.doorsetting_table = self.db.table("doorsetting")
    #         self.eventAction_table = self.db.table("eventAction")
    #         self.controllerInput_table = self.db.table("controllerInput")
    #         self.controllerOutput_table = self.db.table("controllerOutput")
    #         self.door_status_table = self.db.table("door_status")
    #         self.query_table = Query()
    #         self.cache_door_settings()
    #先預存門的設定
    def cache_door_settings(self):
        """預先緩存門的設置信息"""
        self.door_settings = {}
        for pin in self.pins.keys():
            door_info= self.doorsetting_table.search((self.query_table.door_sensor == str(pin))&(self.query_table.control == raspberry_pi_ip)) 
            #door_info = dbConnect_new("SELECT * FROM doorsetting WHERE door_sensor = %s and control = %s", (pin, raspberry_pi_ip))
            print(door_info)
            if door_info:
                wiegand_halt_open_check[pin] = False
                self.door_settings[pin] = door_info[0]
                # 預取door_status表中的信息
                door_status = self.door_status_table.search(self.query_table.doorname == door_info[0]['door'])
                #door_status = dbConnect_new("SELECT * FROM door_status WHERE doorname = %s", (door_info[0]['door'],))
                if door_status:
                    self.door_settings[pin]['door_status'] = door_status[0]
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
                            print(wiegand_halt_open_check)
                            if (wiegand_halt_open_check[pin]):
                                state_status = "HaltOpen"
                state_info = {
                    'door_status_id': door_info['door_status']['id'],
                    'states': state_status
                }
                current_states.append(state_info)
        return current_states
    def limittime(self,openlimit,pin,doorname,door_info):
        elapsed_time = 0
        start_time = time.time() 
        while elapsed_time <= openlimit:
            current_status = self.previous_states[pin]
            elapsed_time = time.time() - start_time
            if(current_status):
                print("已經關門")
                break
            else:
                print("尚未關門持續%d second"%(elapsed_time))
            time.sleep(1)  # 每 1 秒檢查一次
        if(openlimit==int(elapsed_time)):
            print("警報！門開啟過久！")
            get_event = self.eventAction_table.search((self.query_table.doorName == doorname)&(self.query_table.eventClass == "HaltOpen"))
            if not get_event:
                print(f"{doorname} not have haltopen event so do noting!")
                wiegand_halt_open_check[pin] = True
                state_message = {
                    'door_status_id': door_info.get('door_status', {}).get('id', 0),
                    'state': "開門過久",
                    'states':"HaltOpen"
                }
                # 將廣播任務提交給事件循環
                asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), loop)
            else:
                wiegand_halt_open_check[pin] = True
                state_message = {
                    'door_status_id': door_info.get('door_status', {}).get('id', 0),
                    'state': "開門過久",
                    'states':"HaltOpen"
                }
                # 將廣播任務提交給事件循環
                asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), loop)
                #Check DoorSecurity mysql database可以連接到
                result = asyncio.run(check_port_async(mysql_ip,13306))
                if result:
                    print("Connect DoorSecurity database successful.")
                     #新增開門過久事件log到mysql
                    getnowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dbConnect_new("INSERT INTO eventLog(eventName,eventClass,eventCause,timeToEvent,eventStatus)VALUES(%s,%s,%s,%s,%s)", True, (get_event[0]['eventName'], "HaltOpen", "systemAction", getnowtime, "unconfirmed"))
                    dbConnect_new("UPDATE eventAction SET eventStat = %s where eventName = %s ",True,("active",get_event[0]['eventName']))
                else:
                    #如果連結DoorSecurity database異常就會將資訊先暫存到未同步的本地資料庫進行儲存
                    print("No connect mysql server!")
                    getnowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    new_unsync_event = {
                        "eventName": get_event[0]['eventName'],
                        "eventClass": "HaltOpen",
                        "eventCause": "systemAction",
                        "timeToEvent": getnowtime,
                        "eventStatus": "unconfirmed"   
                    }
                    new_event_action_data = {
                        "eventName":get_event[0]['eventName'],
                        "status": "active"
                    }
                    # Event = Query()
                    # self.unsync_event_log_table.upsert(
                    #     new_unsync_event,
                    #     (Event.eventName == new_unsync_event["eventName"])
                    # )
                    # self.unsync_event_table.upsert(
                    #     new_event_action_data,
                    #     (Event.eventName == new_unsync_event["eventName"])
                    # )
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
                for controller, ports in controller_groups.items():
                    eventAction_url = f"http://{controller}:5020/eventaction/output/active"
                    check_controller_output_status = f"http://{controller}:5020/api/output/status"
                    #payload = {"outputPort": ["15", "16"]}  # 需要開啟的 GPIO port
                    dict_output = {
                        "outputPort": ports,
                        "eventName": get_event[0]['eventName']
                    }
                    try:
                        response = check_port_with_socket(mysql_ip,13306)
                        if response:
                            print(f"連接成功！API回應: {response.text} ,可以重新進行Event API 派送")
                            with httpx.Client() as client:
                                response = client.post(eventAction_url, json=dict_output)
                                print(response.json())
                        else:
                            print("DoorSecurity mysql 資料庫連接失敗")
                    except Exception as e:
                        print(f"測試mysql連線發生錯誤，錯誤記錄訊息:{str(e)}")
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

    def get_all_states(self):
        """獲取所有 GPIO 的當前狀態"""
        return {
            pin: "閉合(Close)" if button.is_pressed else "開路(Open)"  # 使用 is_pressed
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
monitor = GPIOMonitor([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
#monitor = GPIOMonitor([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],db,unsyncdb)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await monitor.register(websocket)
# 創建觀察者
observer = Observer()
observer.schedule(monitor, path='.', recursive=False)
observer.start()
observer.join
@app.get("/")
async def get_current_states():
    return monitor.get_all_states()
db_path = "secure_data/encrypted_db.json"
key_path = "secure_data/db.key"
# 初始化加密資料庫
db = tinycon.EncryptedTinyDB(db_path, key)
if __name__ == "__main__":
    # 設置資料庫監控
    observer = tinycon.setup_db_watchdog(db, db_path)
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