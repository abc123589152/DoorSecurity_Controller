from fastapi import FastAPI, WebSocket,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gpiozero import Button  # 改用 Button
import asyncio
import threading
import time
from dbconnect_new import dbConnect_new
import httpx
app = FastAPI()
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
    def limittime(self,openlimit,pin,doorname):
        elapsed_time = 0
        start_time = time.time() 

        while elapsed_time <= openlimit:
            current_status = self.previous_states[pin]
            elapsed_time = time.time() - start_time
            if(current_status):
                print("已經關門")
                break
            else:
                print("尚未關門%d"%(elapsed_time))
            time.sleep(1)  # 每 1 秒檢查一次
        if(openlimit==int(elapsed_time)):
            print("警報！門開啟過久！")
            get_event = dbConnect_new("SELECT * FROM eventAction WHERE doorName=%s AND eventClass=%s",(doorname,"HaltOpen"))
            print(get_event[0]['outputPort'])
            print(get_event[0]['eventName'])
            listoutputpin = dbConnect_new("SELECT * FROM controllerOutput where outputName = %s and controller = %s",(get_event[0]['outputPort'],raspberry_pi_ip))
            url = "http://172.16.1.197:5020/eventaction/output/active"
            #payload = {"outputPort": ["15", "16"]}  # 需要開啟的 GPIO port
            listarr = []
            listarr.append(listoutputpin[0]['outputPort'])
            dict_output = {
                "outputPort": listarr,
                "eventName": get_event[0]['eventName']
                        }
            with httpx.Client() as client:
                response = client.post(url, json=dict_output)
                print(response.json())

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
                        state_status = 'closed' if current_state else 'open'
                        if state_status == "closed":
                            print(f"門號:{get_door_name[0]['door']} 關閉")
                        elif(state_status == "open"):
                            with open("./permition/checkwiegand1permition.conf","r") as readpermition:
                                if (readpermition.read().strip() == "0"):
                                    state_status = "ForceOpen"
                                else:
                                    state_status = "open"
                                    open_door = get_door_name[0]['door']
                                    open_door = threading.Thread(target = self.limittime, args=(3,pin,get_door_name[0]['door']))
                                    open_door.start()
                            print(f"門號:{get_door_name[0]['door']} {state_status}")
                        state_message = {
                            'door_status_id':get_door_controller[0]['id'],
                            'pin': pin,
                            'state': "閉合(Close)" if current_state else "開路(Open)",  # 按下為閉合
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
    
    def haltOpenTime(self,pin,limit_time):
        #這裡是目前pin腳的狀態是開路還是閉路
        time_sec = 0
        while time_sec<=limit_time:
            current_state = self.previous_states[pin]
            print(f"{pin}的目前打開了{time_sec}秒")
            if time_sec == limit_time:
                print("已經觸發開門過久了")
            elif current_state:
                print("門已經關閉重新計時")
                break
            time_sec+=1
            time.sleep(1)
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