from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import time
import platform
import psutil
from datetime import datetime

# # 使用 lifespan 管理應用生命週期
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 啟動前執行的代碼
#     print("伺服器正在啟動...")
#     start_time = time.time()
#     app.state.start_time = start_time
#     app.state.boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     yield  # FastAPI 在這裡處理請求
    
#     # 關閉時執行的代碼
#     print("伺服器正在關閉...")

# 創建 FastAPI 應用實例
app = FastAPI(
    title="測試伺服器",
    description="一個簡單的 FastAPI 服務，用於測試啟動性能",
    version="1.0.0",
    #lifespan=lifespan
)

@app.get("/api/status")
async def get_status():
    """
    返回伺服器的狀態信息
    """
    uptime = time.time() - app.state.start_time
    
    return {
        "status": "運行中",
        "version": "1.0.0",
        "uptime": f"{int(uptime)} 秒",
        "boot_time": app.state.boot_time,
        "system_info": {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_used": f"{psutil.virtual_memory().percent}%",
            "platform": platform.platform()
        }
    }

# 測試路由，返回簡單的問候
@app.get("/")
async def root():
    return {"message": "歡迎使用測試伺服器！請訪問 /api/status 獲取伺服器狀態"}

if __name__ == "__main__":
    # 顯示啟動信息
    print("啟動 FastAPI 測試伺服器...")
    
    # 使用不同的配置啟動 uvicorn 伺服器
    # 標準配置
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # 或者可以嘗試其他配置來測試性能差異:
    # 單一工作進程
    # uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
    
    # 限制並發連接
    # uvicorn.run(app, host="0.0.0.0", port=8000, limit_concurrency=20)
    
    # 使用 uvloop (僅適用於非 Windows 系統)
    # uvicorn.run(app, host="0.0.0.0", port=8000, loop="uvloop")