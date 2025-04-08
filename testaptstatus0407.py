import httpx
import time

def check_api_status(url="http://172.16.1.195:5020/api/output/status"):
    try:
        response = httpx.get(url)
        # 檢查是否連接成功
        if response.status_code == 200:
            return f"連接成功！API回應: {response.text}"
        else:
            return f"連接失敗，狀態碼: {response.status_code}"
    except httpx.ConnectError:
            return "錯誤: 連線不到服務器"
    except Exception as e:
            return f"錯誤: {str(e)}"

if __name__ == "__main__":
    result = check_api_status()
    print(result)