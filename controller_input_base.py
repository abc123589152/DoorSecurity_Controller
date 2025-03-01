from fastapi import FastAPI, WebSocket,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from gpiozero import Button  # 改用 Button
import asyncio
import threading
import time
from dbconnect_new import dbConnect_new
import sqlite_db
import sqlite3
from contextlib import asynccontextmanager
# 在應用啟動時初始化資料庫
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 在應用啟動時執行
    try:
        # 建立資料庫實例
        db = sqlite_db.DeviceDatabase()
        # 初始化資料庫
        db.create_table()
        
        # 從主資料庫獲取這台控制器上的門禁資訊list裡面放入dict的資料格式
        doors = db.initialize_doors()
        #本地資料庫的資料
        all_doorlocal_database = db.get_all_doorlocal_database()
        #確認本地資料庫有沒有相同的資料，如果有就不會在新增進去
        #如果是空的就直接新增資料進去本地資料庫
        if(all_doorlocal_database == []):
            for data in doors:
                await db.insert_device(data)
        else:
            #取得目前本地資料庫doorinfo最大的id值在去跟主資料庫的doorsetting的id值比較，大於這個號碼的資料會被新增
            Get_localdb_max_id = all_doorlocal_database[len(all_doorlocal_database)-1]['id']
            for data in doors:
                if (int(data['id'])>int(Get_localdb_max_id)):
                    print(f"新增的資料是{data}")
                    await db.insert_device(data)
        #找出本地資料庫與master比較已經不存在的進行刪除
        if(all_doorlocal_database!=[]):
            doorlocal_db_doorinfo = db.get_all_doorlocal_database()
            print(await sqlite_db.find_diffrent_delete_local_db(doors,doorlocal_db_doorinfo))
    except Exception as e:
        print(f"Startup error: {e}")
    
    yield  # 這裡是應用運行的地方
    
    # Shutdown: 在應用關閉時執行
    try:
        db.conn.close()
    except Exception as e:
        print(f"Shutdown error: {e}")
app = FastAPI(lifespan=lifespan)
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
        conn = sqlite3.connect("doorlocal_database.db")
        cursor = conn.cursor()
        current_states = []
        
        for pin, button in self.pins.items():
            current_state = button.is_pressed
            # 獲取門的信息
            get_door_name = cursor.execute("SELECT * FROM doorinfo WHERE door_sensor = ?", (pin,))
            result = get_door_name.fetchone()
            
            if result is not None:
                # 獲取door_status的ID
                get_door_controller = dbConnect_new("SELECT * FROM door_status WHERE doorname = %s", (result[3],))
                if get_door_controller:
                    state_status = 'closed' if current_state else 'open'
                    if state_status == "open":
                        # 檢查是否為強制開門
                        with open("./permition/checkwiegand1permition.conf", "r") as readpermition:
                            if readpermition.read().strip() == "0":
                                state_status = "ForceOpen"
                    
                    state_info = {
                        'door_status_id': get_door_controller[0]['id'],
                        'states': state_status
                    }
                    current_states.append(state_info)
        
        conn.close()
        return current_states
    #在單獨的thread裡面監控每個port的狀態
    def monitor_gpio(self):
        """在單獨的線程中監控 GPIO 狀態"""
        conn = sqlite3.connect("doorlocal_database.db")
        cursor = conn.cursor()
        pin_results = {}  # 用於儲存每個 pin 的結果
        while self.running:
            for pin, button in self.pins.items():
                current_state = button.is_pressed  # 使用 is_pressed 檢查按鈕狀態
                if current_state != self.previous_states[pin]:
                    # 狀態發生改變
                    get_door_name = cursor.execute("SELECT * FROM doorinfo where door_sensor = ?", (pin,))
                    result = get_door_name.fetchone()
                    if (result!=None):
                        pin_results[pin] = {
                            'id': result[0],
                            'control': result[1],
                            'wiegand': result[2],   
                            'door': result[3],
                            'door_sensor': result[4],
                            'doorRelease_button': result[5],
                            'reset_time': result[6],
                            'openTimeLimit': result[7]
                        }
                    else:
                        pin_results[pin] = None
                    #get_door_status_table_id = dbConnect_new("SELECT id from door_status where doorname = %s",(door_id,))
                    self.previous_states[pin] = current_state
                    if pin_results[pin]!=None:
                        get_door_controller = dbConnect_new("SELECT *FROM door_status where doorname = %s",(pin_results[pin]['door'],))
                        state_status = 'closed' if current_state else 'open'
                        if state_status == "closed":
                            print(f"門號:{pin_results[pin]['door']} 關閉")
                        elif(state_status == "open"):
                            with open("./permition/checkwiegand1permition.conf","r") as readpermition:
                                if (readpermition.read().strip() == "0"):
                                    state_status = "ForceOpen"
                                else:
                                    state_status = "open"
                            print(f"門號:{pin_results[pin]['door']} {state_status}")
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
            time.sleep(0.5)  # 50ms 延遲
    
            
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