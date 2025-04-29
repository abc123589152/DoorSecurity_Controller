from tinydb import TinyDB
from tinydb.storages import MemoryStorage
import mysql.connector
import json
import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from tinydb.queries import Query
app = FastAPI()
# MySQL 連接配置
mysql_config = {
    'host': '172.16.1.221',      # 修改為你的 MySQL 主機
    'user': 'root',       # 修改為你的 MySQL 用戶名
    'password': '1qaz@WSX',   # 修改為你的 MySQL 密碼
    'port':"13306",
    'database':'DoorSecurity'     # 修改為你的數據庫名稱
}
class EncryptedTinyDB:
    def __init__(self, path, key=None):
        """
        初始化加密的 TinyDB 實例
        
        Parameters:
        path - 資料庫檔案路徑
        key - 加密密鑰 (如果為 None，則生成新密鑰)
        """
        self.path = path
        
        # 生成或使用提供的密鑰
        if key is None:
            self.key = Fernet.generate_key()
            print(f"生成的新密鑰: {self.key.decode()}")
        else:
            self.key = key if isinstance(key, bytes) else key.encode()
            
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
                    print(f"成功載入並解密資料庫: {self.path}")
            else:
                # 檔案不存在或為空，創建新的 TinyDB 實例
                self.db = TinyDB(storage=MemoryStorage)
                print(f"創建新的資料庫: {self.path}")
                self._save_db()  # 保存空資料庫
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
def get_encryption_key(key_path=None):
    """
    獲取或生成加密密鑰
    
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
    
    # 生成新密鑰
    key = Fernet.generate_key()
    
    # 保存密鑰 (如果提供了路徑)
    if key_path:
        try:
            # 確保目錄存在
            os.makedirs(os.path.dirname(os.path.abspath(key_path)), exist_ok=True)
            
            with open(key_path, 'wb') as f:
                f.write(key)
            
            # 設置檔案權限
            if os.name != 'nt':  # 不是 Windows
                os.chmod(key_path, 0o400)  # 只有檔案擁有者可讀
                
            print(f"新密鑰已保存到: {key_path}")
        except Exception as e:
            print(f"保存密鑰時發生錯誤: {e}")
    
    return key
def convert_datetime(obj):
    """處理 MySQL 日期時間格式到 JSON 可序列化格式"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return obj

def fetch_mysql_data(table_name):
    """從 MySQL 獲取指定表格的所有資料"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        
        # # 處理日期時間格式
        # for item in data:
        #     for key, value in item.items():
        #         item[key] = convert_datetime(value)
                
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"從 MySQL 提取 {table_name} 資料時出錯: {str(e)}")
        return []

def sync_to_tinydb(db):
    """將 MySQL 數據同步到 TinyDB"""
    try:
        # 清空並重新創建表格
        #db.drop_tables()
        
        # 獲取並同步每個表
        tables = {
            'doorsetting': db.table('doorsetting'),
            'doorgroup': db.table('doorgroup'),
            'employ': db.table('employ')
        }
        
        for table_name, tinydb_table in tables.items():
            # 獲取 MySQL 資料
            mysql_data = fetch_mysql_data(table_name)
            if mysql_data:
                # 清空現有 TinyDB 表格數據
                #tinydb_table.truncate()
                # 插入新數據
                tinydb_table.insert_multiple(mysql_data)
                print(f"表格 {table_name} 同步成功，共 {len(mysql_data)} 筆記錄")
            else:
                print(f"表格 {table_name} 無資料或同步失敗")
        db._save_db()
        return True
    except Exception as e:
        print(f"同步到 TinyDB 時發生錯誤: {str(e)}")
        return False

def initialization_db(): 
    # 檔案路徑
    db_path = "secure_data/encrypted_db.json"
    key_path = "secure_data/db.key"
    # 獲取或生成密鑰
    key = get_encryption_key(key_path)
    # 初始化加密資料庫
    db = EncryptedTinyDB(db_path, key)
    # 使用資料庫
    try:
        # 查詢
        User = Query()
        alice = db.get(User.name == "Alice")
        print(f"找到 Alice: {alice}")
        
        # 更新
        db.update({"age": 31}, User.name == "Alice")
        
        # 再次查詢
        alice = db.get(User.name == "Alice")
        print(f"更新後的 Alice: {alice}")
        
        # 獲取所有資料
        all_users = db.all()
        print(f"所有用戶: {all_users}")
        
    finally:
        # 關閉資料庫
        db.close()
db_path = "secure_data/encrypted_db.json"
key_path = "secure_data/db.key"
# 獲取或生成密鑰
key = get_encryption_key(key_path)
# 初始化加密資料庫
db = EncryptedTinyDB(db_path, key)

# @app.get("/api/create/table")
# def table():
#     table_list = ['doorsetting','employ','doorgroup']
#     # 獲取表格並插入資料
#     for table in table_list:
#         table = db.table(table)
#     # 顯式保存數據庫
#     db._save_db()
@app.get("/api/get/table")
def get_table():
    a = db.tables()
    return {"tables":a}
@app.get("/api/mysql/sync")
def sync_mysql():
    sync_to_tinydb(db)
    return {"message","sync done"}

@app.get("/api/get/{tablename}/data/")
def data(tablename: str):
    a = db.table(tablename).all()
    return {"message":a}
@app.get("/api/test/insert/doorsetting")
def test_insert_doorsetting():
    try:
        # 建立測試資料
        test_record = {
            "door": "Test Door",
            "location": "Test Location",
            "door_sensor": "5",
            "door_lock": "10",
            "openTimeLimit": "30",
            "control": "172.16.1.195",
            "creation_time": datetime.now().isoformat()
        }
        
        # 獲取表格並插入資料
        table = db.table("doorsetting")
        doc_id = table.insert(test_record)
        
        # 顯式保存數據庫
        db._save_db()
        
        # 檢查插入後的資料
        all_records = table.all()
        
        return {
            "status": "success",
            "inserted_id": doc_id,
            "record_count": len(all_records),
            "test_record": test_record,
            "all_records": all_records
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)