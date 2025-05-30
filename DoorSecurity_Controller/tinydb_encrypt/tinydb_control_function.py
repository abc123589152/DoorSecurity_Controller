from tinydb import TinyDB
from tinydb.storages import MemoryStorage
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from tinydb.queries import Query
import subprocess,re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import db_connect.dbconnect_new as mysqldb
import time
# 全局字典，用於追踪每個門鎖的計時器
door_timers = {}
def get_eth0_ip(interface):
    try:
        output = subprocess.check_output("ip addr show "+interface, shell=True, text=True)
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
        if match:
            return match.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        return None
# 創建一個檔案系統事件處理類
class TinyDBFileHandler(FileSystemEventHandler):
    def __init__(self, db_instance, db_path):
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
                    self.db._load_db()

                    print("資料庫重新載入成功")
                except Exception as e:
                    print(f"重新載入資料庫時發生錯誤: {e}")
class EncryptedTinyDB:
    def __init__(self, path, key=None):
        """
        初始化加密的 TinyDB 實例
        
        Parameters:
        path - 資料庫檔案路徑
        key - 加密密鑰 (如果為 None，則生成新密鑰)
        """
        #確認資料庫已經建立才會做下一步驟
        while True:
            if os.path.exists("/mnt/secure_data/checkSync.conf"):
                with open("/mnt/secure_data/checkSync.conf","r") as readchecksync:
                    if(readchecksync.read().strip() =="1"):
                        #確認同步完畢結束確認
                        break
            else:
                print("等待本地資料庫初始化同步完成...")
                time.sleep(5)
        print("tinydb control 本地資料庫初始化完成，開始載入資料庫...")
        self.path = path
        self.key = key
        # # 生成或使用提供的密鑰
        # if key is None:
        #     self.key = Fernet.generate_key()
        #     print(f"生成的新密鑰: {self.key.decode()}")
        # else:
        #     self.key = key if isinstance(key, bytes) else key.encode()
            
        self.fernet = Fernet(self.key)
        self.db = None
        self._load_db()
    def _load_db(self):
        """從檔案載入並解密數據庫"""
        try:
            # 檢查檔案是否存在
            if os.path.exists(self.path) and os.path.getsize(self.path) > 0:
                # 讀取並解密文件
                with open(self.path, 'rb') as f:
                    encrypted_data = f.read()
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    data = json.loads(decrypted_data)
                    
                    # 創建內存中的 TinyDB 實例
                    self.db = TinyDB(storage=MemoryStorage)
                    self.db.storage.write(data)
                    print("資料庫已經存在")
                    print(f"Control function 成功載入並解密資料庫: {self.path}")
            else:
                print("資料庫載入失敗，可能原因為不存在")
        except InvalidToken:
            print("錯誤：無法解密資料庫，密鑰可能不正確")
            raise
        except Exception as e:
            print(f"載入資料庫時發生錯誤: {e}")
            # 創建新的資料庫
            self.db = TinyDB(storage=MemoryStorage)
    def _save_db(self):
        """加密並保存資料庫到檔案"""
        try:
            # 獲取資料並加密
            data = self.db.storage.read()
            encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
            
            # 確保目錄存在
            os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
            
            # 寫入檔案
            with open(self.path, 'wb') as f:
                f.write(encrypted_data)
            
            # 設置檔案權限 (僅 Linux/Unix 系統)
            if os.name != 'nt':  # 不是 Windows
                os.chmod(self.path, 0o600)  # 只有檔案擁有者可讀寫
                
            return True
        except Exception as e:
            print(f"保存資料庫時發生錯誤: {e}")
            return False

    # 實現 TinyDB 的主要方法
    def table(self, name):
        """獲取指定名稱的表格"""
        return self.db.table(name)
    
    def insert(self, document):
        """插入文檔"""
        result = self.db.insert(document)
        self._save_db()
        return result
    
    def insert_multiple(self, documents):
        """批量插入多個文檔"""
        result = self.db.insert_multiple(documents)
        self._save_db()
        return result
    
    def all(self):
        """獲取所有文檔"""
        return self.db.all()
    
    def search(self, query):
        """搜索符合條件的文檔"""
        return self.db.search(query)
    
    def get(self, query):
        """獲取符合條件的第一個文檔"""
        return self.db.get(query)
    
    def update(self, fields, query):
        """更新符合條件的文檔"""
        result = self.db.update(fields, query)
        self._save_db()
        return result
    
    def upsert(self, document, query):
        """更新現有文檔或插入新文檔"""
        result = self.db.upsert(document, query)
        self._save_db()
        return result
    
    def remove(self, query):
        """刪除符合條件的文檔"""
        result = self.db.remove(query)
        self._save_db()
        return result
    
    def truncate(self):
        """清空資料庫"""
        result = self.db.truncate()
        self._save_db()
        return result
    
    def close(self):
        """關閉資料庫並保存"""
        if self.db:
            self._save_db()
            self.db = None
            print(f"資料庫已關閉並保存: {self.path}")
    # 在 EncryptedTinyDB 類中添加此方法
    def tables(self):
        """獲取資料庫中的所有表格名稱"""
        if self.db is None:
            return []
    
        tables = list(self.db._tables.keys())
        # 可選：過濾掉默認表格
        if '_default' in tables:
            tables.remove('_default')
    
        return tables
    def get_table_data(self,tablename):
        data = self.db.table(tablename).all()
        return data
def get_encryption_key(key_path=None):
    """
    獲取加密密鑰
    
    Parameters:
    key_path - 密鑰檔案路徑 (如果為 None，則生成新密鑰)
    
    Returns:
    key - 加密密鑰
    """
    if key_path and os.path.exists(key_path):
        try:
            with open(key_path, 'rb') as f:
                key = f.read().strip()
            print(f"已從檔案載入密鑰: {key_path}")
            return key
        except Exception as e:
            print(f"讀取密鑰檔案時發生錯誤: {e}")
    return key
def convert_datetime(obj):
    """處理 MySQL 日期時間格式到 JSON 可序列化格式"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return obj

# db_path = "/mnt/secure_data/encrypted_db.json"
# key_path = "/mnt/secure_data/db.key"
# # 獲取或生成密鑰
# key = get_encryption_key(key_path)
# # 初始化加密資料庫
# db = EncryptedTinyDB(db_path, key)

def setup_db_watchdog(db_instance, db_path):
    """設置資料庫檔案監控"""
    event_handler = TinyDBFileHandler(db_instance, db_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(db_path), recursive=False)
    observer.start()
    print(f"已啟動對 {db_path} 的監控")
    
    # 返回觀察者以便後續可能需要的停止操作
    return observer