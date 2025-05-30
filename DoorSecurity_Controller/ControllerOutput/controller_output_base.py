from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import List, Optional
from gpiozero import LED
import asyncio
import os,sys
app = FastAPI()
import tinydb_encrypt.tinydb_sync_no_api as tinydb
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_connect.dbconnect_new import dbConnect_new
# 設定允許的 IP 和網域
ALLOWED_IPS = {"*"}
ALLOWED_ORIGINS = {"*"}
#取得密鑰
db_path = "./secure_data/encrypted_db.json"
key_path = "./secure_data/db.key"
key = tinydb.get_encryption_key(key_path)
#初始化tinydb
db = tinydb.EncryptedTinyDB(db_path, key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 創建一個檔案系統事件處理類
class TinyDBFileHandler(FileSystemEventHandler):
    def __init__(self, db_instance, db_path,monitor):
        self.monitor = monitor
        self.db = db_instance
        self.db_path = db_path
        self.last_modified = os.path.getmtime(db_path) if os.path.exists(db_path) else 0
        print(f"初始化監控 TinyDB 檔案: {db_path}")
    def on_modified(self, event):
        # 只關注我們的資料庫檔案
        if event.src_path == self.db_path:
            current_modified = os.path.getmtime(self.db_path)
            
            # 避免重複處理同一事件
            if current_modified > self.last_modified:
                self.last_modified = current_modified
                print(f"檔案已被修改: {event.src_path}")
                print("重新載入資料庫...")
                
                # 重新載入資料庫
                # 注意：由於您的 EncryptedTinyDB 是加密的，需要特殊處理
                try:
                    # 這裡假設 db 有 _load_db 方法（從您的程式碼中看到有此方法）
                    #self.db._load_db()
                    self.monitor.modified()
                    print("資料庫重新載入成功")
                except Exception as e:
                    print(f"重新載入資料庫時發生錯誤: {e}")
class AsyncGPIOController:
    def __init__(self):
        self.leds = {}
     # 創建一個非同步的 LED 控制方法
    async def led_control(self, led, state):
        try:
            if state:
                led.on()
            else:
                led.off()
        except Exception as e:
            print(f"LED 控制錯誤：{str(e)}")
    #取得需要觸發active的輸出(output)點位gpio號碼
    async def control_output_pins_on(self, gpio_list):
        try:
            # 初始化新的 GPIO pins
            tasks = []
            for pin in gpio_list:
                tasks.append(self.led_control(gpio_dict[int(pin)], True))
            
            # 同時執行所有 GPIO 操作
            await asyncio.gather(*tasks)
            
            print(f"GPIO pins {gpio_list} 已同時開啟")
            return True
        except Exception as e:
            print(f"GPIO 控制錯誤：{str(e)}")
            return False
    #取得需要觸發的inactive輸出(output)點位gpio號碼
    async def control_output_pins_off(self, gpio_list):
        try:
            # 初始化新的 GPIO pins
            tasks = []
            for pin in gpio_list:
                tasks.append(self.led_control(gpio_dict[int(pin)], False))
            
            # 同時執行所有 GPIO 操作
            await asyncio.gather(*tasks)
            
            print(f"GPIO pins {gpio_list} 已同時關閉")
            return True
        except Exception as e:
            print(f"GPIO 控制錯誤：{str(e)}")
            return False
# 定義事件資料結構，使用 Optional 來允許 None 值
class EventData(BaseModel):
    outputPort: Optional[str] = None
class GpioOutputRequest(BaseModel):
    outputPort: List[str]
    eventName: Optional[str] = None
    controller: Optional[str] = None
# GPIO 初始化
gpio_dict = {}
try:
    #定義哪些gpio port要做為輸出點位(output)使用
    gpio_ports = [13,14,15,16,19,20,21,24,25,26,27]
    for pin in gpio_ports:
        gpio_dict[pin] = LED(pin)
except Exception as e:
    print(f"Error setting up GPIO: {e}")
#點位觸發active
async def inside_gpio_output_on(gpio_number:int):
    #active gpio output port
    gpio_dict[gpio_number].on()
    return {"status":"active ok"}
#點位觸發inactive
async def inside_gpio_output_off(gpio_number:int):
    #active gpio output port
    gpio_dict[gpio_number].off()
    return {"status":"active ok"}
#取得目前控制器的IP，讀取config檔案的形式製作
def get_wlan_ip():
    try:
        with open("/controller_output/raspberrypi_ipaddress.config","r") as readip:
            ip = readip.read().strip()
            return ip
    except Exception as e:
        return f"read ip error please check {str(e)}"
#建立API供給門禁事件(event)使用，可進行多點位一次觸發active
@app.post("/eventaction/output/active")
async def handle_event_action_gpio_output_on(request: GpioOutputRequest):
    try:
        # data 會自動被轉換為 Python list
        #print(gpio_output_nunber_list+"gpio port on")  # 會印出 ['15', '16']
        #啟動傳送過來需要開啟的gpio port number
        gpio_output_nunber_list = request.outputPort
        output_pin_operator = AsyncGPIOController()
        await output_pin_operator.control_output_pins_on(gpio_output_nunber_list)
        return {"status": "success", "received_data": gpio_output_nunber_list}
    except Exception as e:
        print(f"{get_wlan_ip()} api error:{str(e)}")
#建立API供給門禁事件(event)使用，可進行多點位一次觸發inactive
@app.post("/eventaction/output/inactive")
async def handle_event_action_gpio_output_off(request: GpioOutputRequest):
    try:
        gpio_output_nunber_list = request.outputPort
        output_pin_operator = AsyncGPIOController()
        await output_pin_operator.control_output_pins_off(gpio_output_nunber_list)
        return {"status": "success", "received_data": gpio_output_nunber_list}
    except Exception as e:
        print(f"{get_wlan_ip()} api error:{str(e)}")
#建立API供給需要進行遠端開啟單點GPIO點位使用
@app.post("/gpio/{port}/on")
async def gpio_on(port: int):
    if port in gpio_ports:
        gpio_dict[port].on()
        return {
            "status": "success",
            "port": port,
            "action": "on"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid GPIO port"
        )
#建立API供給需要進行遠端關閉單點GPIO點位使用
@app.post("/gpio/{port}/off")
async def gpio_off(port: int):
    if port in gpio_ports:
        gpio_dict[port].off()
        return {
            "status": "success",
            "port": port,
            "action": "off"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid GPIO port"
        )

@app.get("/gpio/{port}/status")
async def gpio_status(port: int):
    if port in gpio_ports:
        state = gpio_dict[port].is_lit
        return {
            "status": "success",
            "port": port,
            "state": "on" if state else "off"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid GPIO port"
        )
def setup_db_watchdog(db_instance, db_path,monitor):
    """設置資料庫檔案監控"""
    event_handler = TinyDBFileHandler(db_instance, db_path,monitor)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(db_path), recursive=False)
    observer.start()
    print(f"已啟動對 {db_path} 的監控")
    
    # 返回觀察者以便後續可能需要的停止操作
    return observer
@app.get("/api/ControllerOutput/status")
async def get_api_output_status():
    return {"status":"ok"}
@app.post("/api/check/permition/{door}/{cardnumber}")
async def checkpermition(door:str,cardnumber:str):
    

if __name__ == "__main__":
    # 設置資料庫監控
    observer = setup_db_watchdog(db, db_path,monitor)
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5020
    )
