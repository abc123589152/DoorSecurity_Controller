from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gpiozero import Button
import asyncio
import threading
import time
import httpx
from dbconnect_new import dbConnect_new

app = FastAPI()
raspberry_pi_ip = "172.16.1.195"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局設置事件循環
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class GPIOMonitor:
    def __init__(self, pin_numbers):
        self.pins = {}
        self.connections = set()
        self.running = True
        self.previous_states = {}
        self.door_sensor_dict = {}
        self.door_threads = {}
        
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
        
    def cache_door_settings(self):
        """預先緩存門的設置信息"""
        self.door_settings = {}
        for pin in self.pins.keys():
            door_info = dbConnect_new("SELECT * FROM doorsetting WHERE door_sensor = %s and control = %s", (pin, raspberry_pi_ip))
            if door_info:
                self.door_settings[pin] = door_info[0]
                # 預取door_status表中的信息
                door_status = dbConnect_new("SELECT * FROM door_status WHERE doorname = %s", (door_info[0]['door'],))
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
                            args=(int(door_info.get('openTimeLimit', 30)), pin, door_name),
                            daemon=True
                        )
                        self.door_threads[door_name].start()
            
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
        
        # 將廣播任務提交給事件循環
        asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), loop)

    def limittime(self, openlimit, pin, doorname):
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
            threading.Thread(target=self.trigger_halt_open_event, args=(doorname,), daemon=True).start()
    
    def trigger_halt_open_event(self, doorname):
        """觸發開門過久事件"""
        get_event = dbConnect_new("SELECT * FROM eventAction WHERE doorName=%s AND eventClass=%s", (doorname, "HaltOpen"))
        
        if not get_event:
            print(f"{doorname} not have haltopen event so do noting!")
            return
            
        listoutputpin = dbConnect_new(
            "SELECT controller, GROUP_CONCAT(outputPort ORDER BY outputPort) AS outputPort "
            "FROM DoorSecurity.controllerOutput "
            "WHERE FIND_IN_SET(outputName, %s) > 0 GROUP BY controller",
            (get_event[0]['outputPort'],)
        )
        
        for controller_output in listoutputpin:
            self.send_event_action(controller_output, get_event[0])
    
    def send_event_action(self, controller_output, event):
        """發送事件動作到控制器"""
        eventAction_url = f"http://{controller_output['controller']}:5020/eventaction/output/active"
        check_controller_output_status = f"http://{controller_output['controller']}:5020/api/output/status"
        
        listarr = []
        listarr.append(controller_output['outputPort'])
        dict_output = {
            "outputPort": listarr,
            "eventName": event['eventName']
        }
        
        try:
            # 使用with語句確保及時釋放資源
            with httpx.Client(timeout=5.0) as client:  # 設置超時
                # 檢查服務器狀態
                response = client.get(check_controller_output_status)
                
                if response.status_code == 200:
                    # 發送事件
                    response = client.post(eventAction_url, json=dict_output)
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
                
                state_info = {
                    'door_status_id': door_info['door_status']['id'],
                    'states': state_status
                }
                current_states.append(state_info)
        
        return current_states

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
monitor = GPIOMonitor([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

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
    finally:
        print("Cleaning up...")
        monitor.cleanup()
        # 關閉事件循環
        loop.call_soon_threadsafe(loop.stop)
        event_loop_thread.join(timeout=1.0)
        dbConnect_new.close_pool()