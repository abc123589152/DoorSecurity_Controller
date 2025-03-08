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
ALLOWED_IPS = {"*"}
ALLOWED_ORIGINS = {"*"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 定義事件資料結構，使用 Optional 來允許 None 值
class EventData(BaseModel):
    outputPort: Optional[str] = None
class GpioOutputRequest(BaseModel):
    outputPort: List[str]
    eventName: Optional[str] = None
    controller: Optional[str] = None

#取得目前控制器的IP，讀取config檔案的形式製作
def get_wlan_ip():
    try:
        with open("/controller_output/ifconfig/ip.conf","r") as readip:
            ip = readip.read().strip()
            return ip
    except Exception as e:
        return f"read ip error please check {str(e)}"
#建立API供給門禁事件(event)使用，可進行多點位一次觸發inactive
@app.post("/eventaction/message")
def handle_event_action_gpio_output_off(request: GpioOutputRequest):
    try:
        outputlist = request.outputPort
        print(outputlist)
        return {"status": "success", "received_data": outputlist}
    except Exception as e:
        print(f"{get_wlan_ip()} api error:{str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5020
    )