import socket
import time

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
if __name__ == "__main__":
    print(check_port_with_socket("172.16.1.100",13306))