from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os,time,sys
import json
from tinydb import Query,TinyDB
from tinydb.storages import MemoryStorage
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db_connect.dbconnect_new as mysqldb
key_path = "/mnt/secure_data/db.key"
class tinydb_init_sync:
    """
        開機時候初始化TinyDB 
        
        Parameters:
        path - 資料庫檔案路徑
        key - 加密密鑰 (如果為 None，則生成新密鑰)
    """
    def __init__(self,path):
        """
        初始化加密的 TinyDB 實例
        
        Parameters:
        path - 資料庫檔案路徑
        key - 加密密鑰 (如果為 None，則生成新密鑰)
        """
        self.path = path
        self.key = self.get_encryption_key(key_path)
        self.fernet = Fernet(self.key)
    def init_tinydb(self):
        #暫存到記憶體
        self.db = TinyDB(storage=MemoryStorage)
        #開始同步主資料庫資訊到本地端
        if os.path.exists("/mnt/secure_data/encrypted_db.json"):
            print("資料庫已經存在無需在初始化同步!")
        else:
            self.sync_to_tinydb()
    def get_encryption_key(self,key_path=None):
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
    def fetch_mysql_data(self,table_name):
        """從 MySQL 獲取指定表格的所有資料"""
        try:
            data = mysqldb.dbConnect_new(f"SELECT *FROM {table_name}",False,("",))
            return data
        except Exception as e:
            print(f"從 MySQL 提取 {table_name} 資料時出錯: {str(e)}")
            return []
    def sync_to_tinydb(self):
        """將 MySQL 數據同步到 TinyDB"""
        try:
            # 清空並重新創建表格
            #db.drop_tables()
            # 獲取並同步每個表
            tables = {
                'doorsetting': self.table('doorsetting'),
                'doorgroup': self.table('doorgroup'),
                'employ': self.table('employ'),
                'controllerInput':self.table('controllerInput'),
                'controllerOutput':self.table('controllerOutput'),
                'door_status':self.table('door_status'),
                'eventAction':self.table('eventAction')
            }
            
            for table_name, tinydb_table in tables.items():
                # 獲取 MySQL 資料
                mysql_data = self.fetch_mysql_data(table_name)
                if mysql_data:
                    # 清空現有 TinyDB 表格數據
                    #tinydb_table.truncate()
                    # 插入新數據
                    tinydb_table.insert_multiple(mysql_data)
                    print(f"表格 {table_name} 同步成功，共 {len(mysql_data)} 筆記錄")
                    time.sleep(2)
                else:
                    print(f"表格 {table_name} 無資料或同步失敗")
            with open("/mnt/secure_data/checkSync.conf","w") as writecheck:
                writecheck.write("1")
            self._save_db()
            return True
        except Exception as e:
            print(f"同步到 TinyDB 時發生錯誤: {str(e)}")
        return False
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
    def insert_multiple(self, documents):
        """批量插入多個文檔"""
        result = self.db.insert_multiple(documents)
        self._save_db()
        return result
    # 實現 TinyDB 的主要方法
    def table(self, name):
        """獲取指定名稱的表格"""
        return self.db.table(name)
    def init_create_wiegand(self):
            if not os.path.exists("/mnt/secure_data/wiegand_config"):
                os.mkdir("/mnt/secure_data/wiegand_config")
            doorsetting_table = self.db.table("doorsetting")
            wiegand_list = ['Wiegand1','Wiegand2','Wiegand3']
            user = Query()
            for wiegand in wiegand_list:
                with open(f"/mnt/secure_data/wiegand_config/{wiegand}.conf","w") as wiegand_write:
                    get_wiegand_doorname = doorsetting_table.get((user.wiegand == wiegand) & (user.control == get_eth0_ip("wlan0")))
                    if get_wiegand_doorname!=None:
                        wiegand_write.write(get_wiegand_doorname['door'])