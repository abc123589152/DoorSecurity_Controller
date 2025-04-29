from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from typing import List, Optional
from gpiozero import LED
import asyncio
from dbconnect_new import dbConnect_new
from dbconnect_query import dbConnect_query
from dbconnect_query_return_result import dbConnect_query_return_result
app = FastAPI()

# 設定允許的 IP 和網域
ALLOWED_IPS = {"127.0.0.1", "172.16.1.103"}
ALLOWED_ORIGINS = {"http://172.16.1.103:5001"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        with open("/controller_output/ifconfig/ip.conf","r") as readip:
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
@app.get("/api/output/status")
async def get_raspberry_pi_status():
    return {"status":"ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5020
    )