from tinydb import TinyDB
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class DBFileHandler(FileSystemEventHandler):
    def __init__(self, db_instance):
        self.db = db_instance
    
    def on_modified(self, event):
        if event.src_path.endswith('door_control_system.json'):
            print("檢測到文件變更，重新加載數據庫")
            self.db.close()
            self.db = TinyDB('door_control_system.json')
    def printtinydb(self):
        table = self.db.table("doorsetting")
        print(table.all())

# 創建 TinyDB 實例
db = TinyDB('door_control_system.json')

# 創建事件處理器並傳入 db 實例
event_handler = DBFileHandler(db)

# 創建觀察者
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()

try:
    while True:
        choice = input("1.print all json,2.end")
        if choice == "1":
            event_handler.printtinydb()
        else:
            print("Exit program.")
            break
except KeyboardInterrupt:
    observer.stop()
observer.join()