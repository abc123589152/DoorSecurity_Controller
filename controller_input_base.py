from fastapi import FastAPI, WebSocket,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gpiozero import Button  # 改用 Button
import asyncio
import threading
import time
from dbconnect_new import dbConnect_new
app = FastAPI()
#當下那台控制器Raspnerry Pi的IP，這裡是暫時測試用，未來會用程式自己抓取目前現在的IP
raspberry_pi_ip = "172.16.1.195"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class GPIOMonitor:
    def __init__(self, pin_numbers):
        #存放初始話過後的GPIO點位
        self.pins = {}
        self.connections = set()
        self.running = True
        self.previous_states = {}
        self.door_sensor_dict = {}
        
        # 初始化 GPIO，使用 Button，
        for pin in pin_numbers:
            button = Button(pin, pull_up=True,bounce_time=0.1)
            self.pins[pin] = button
            self.previous_states[pin] = button.is_pressed  # 使用 is_pressed 替代 value
        
        # 啟動監控線程
        self.monitor_thread = threading.Thread(target=self.monitor_gpio)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    #這裡用來取得當下的門位狀態
    def get_current_door_states(self):
        """獲取所有門的當前狀態"""
        current_states = []
        for pin, button in self.pins.items():
            current_state = button.is_pressed
            # 獲取門的信息
            get_door_name = dbConnect_new("SELECT * FROM doorsetting WHERE door_sensor = %s and control = %s", (pin,raspberry_pi_ip))
            if get_door_name!=[]:
                # 獲取door_status的ID
                get_door_controller = dbConnect_new("SELECT * FROM door_status WHERE doorname = %s", (get_door_name[0]['door'],))
                if get_door_controller:
                    state_status = 'closed' if current_state else 'open'
                    if state_status == "open":
                        # 檢查是否為強迫開門
                        with open("./permition/checkwiegand1permition.conf", "r") as readpermition:
                            if readpermition.read().strip() == "0":
                                state_status = "ForceOpen"
                    state_info = {
                        'door_status_id': get_door_controller[0]['id'],
                        'states': state_status
                    }
                    current_states.append(state_info)
        return current_states
    #在單獨的thread裡面監控每個port的狀態
    def monitor_gpio(self):
        """在單獨的線程中監控 GPIO 狀態"""
        while self.running:
            for pin, button in self.pins.items():
                current_state = button.is_pressed  # 使用 is_pressed 檢查按鈕狀態
                if current_state != self.previous_states[pin]:
                    # 狀態發生改變
                    get_door_name = dbConnect_new("SELECT * FROM doorsetting where door_sensor = %s and control = %s", (pin,raspberry_pi_ip))
                    #get_door_status_table_id = dbConnect_new("SELECT id from door_status where doorname = %s",(door_id,))
                    self.previous_states[pin] = current_state
                    if get_door_name!=[]:
                        get_door_controller = dbConnect_new("SELECT *FROM door_status where doorname = %s",(get_door_name[0]['door'],))
                        #這裡是用來判斷門位點是否為打開的
                        state_status = 'closed' if current_state else 'open'
                        if state_status == "closed":
                            print(f"門號:{get_door_name[0]['door']} 關閉")
                        elif(state_status == "open"):
                            #讀取該門禁設定的wiegand編號權限檔案，1為有權限,0為沒有權限
                            with open("./permition/checkwiegand1permition.conf","r") as readpermition:
                                if (readpermition.read().strip() == "0"):
                                    state_status = "ForceOpen"
                                else:
                                    state_status = "open"
                            print(f"門號:{get_door_name[0]['door']} {state_status}")
                        #建立Websocket需要傳送的訊息，這個訊息要傳送到前端網頁進行顯示，內容是開關門訊息
                        state_message = {
                            #取得門禁控制欄位資料庫裡這個門號的id，這裡會對應到前端網頁顯示門狀態的html欄位id
                            'door_status_id':get_door_controller[0]['id'],
                            'pin': pin,
                            'state': "閉合(Close)" if current_state else "開路(Open)",  # 按下為閉合也就是關閉，反之則是打開
                            'states':state_status,
                            'value': current_state
                        }
                        # 發送更新到所有連接
                        asyncio.run(self.broadcast_update(state_message))
                    else:
                        state_message = {
                            'pin': pin,
                            'state': "閉合(Close)" if current_state else "開路(Open)",  # 按下為閉合
                            'value': current_state
                        }
                        if current_state:
                            print(f"Input{pin} 乾接點關閉")
                        else:
                            print(f"Input{pin} 乾接點打開")
                        # 發送更新到所有連接
                        asyncio.run(self.broadcast_update(state_message))
            # 降低 CPU 使用率
            time.sleep(0.5)  # 500ms 延遲
    #將欲傳送到websocket client端訊息進行廣播
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
        self.monitor_thread.join(timeout=1.0)
        for button in self.pins.values():
            button.close()

# 創建 GPIO 監控器實例
monitor = GPIOMonitor([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
#建立websocket的連接名稱
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