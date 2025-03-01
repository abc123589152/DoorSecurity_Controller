from datetime import datetime
#取得當下時間
def get_now_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')