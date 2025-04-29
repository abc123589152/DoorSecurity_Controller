import mysql.connector
from datetime import datetime
import time
import os
from sqlite_main import sqlcipherClass  # 導入您的 SQLite 加密類

class MySQLtoSQLiteSynchronizer:
    def __init__(self, mysql_config, sqlite_db_path, sqlite_password):
        """
        初始化同步器
        
        Args:
            mysql_config (dict): MySQL 連接配置 (host, user, password, database)
            sqlite_db_path (str): SQLite 資料庫路徑
            sqlite_password (str): SQLite 加密密碼
        """
        self.mysql_config = mysql_config
        self.sqlite_db_path = sqlite_db_path
        self.sqlite_password = sqlite_password
        self.tables = [
            "doorsetting", 
            "employ", 
            "door_status", 
            "doorgroup", 
            "eventAction", 
            "controllerInput", 
            "controllerOutput"
        ]
        
        # 初始化 SQLite 連接
        self.sqlite_db = sqlcipherClass(sqlite_db_path, sqlite_password)
        self.sqlite_db.create_encrypted_db()  # 確保表格存在
        
    def connect_mysql(self):
        """建立 MySQL 連接"""
        try:
            conn = mysql.connector.connect(**self.mysql_config)
            return conn
        except mysql.connector.Error as e:
            print(f"MySQL 連接錯誤: {e}")
            return None
    
    def get_mysql_data(self, table_name):
        """從 MySQL 獲取表格數據"""
        conn = self.connect_mysql()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except mysql.connector.Error as e:
            print(f"從 MySQL 獲取 {table_name} 數據時出錯: {e}")
            if conn:
                conn.close()
            return []
    
    def synchronize_table(self, table_name):
        """同步單個表格"""
        print(f"開始同步表格: {table_name}")
        
        # 獲取 MySQL 資料
        mysql_data = self.get_mysql_data(table_name)
        if not mysql_data:
            print(f"無法獲取 {table_name} 資料或表格為空")
            return 0
        
        # 清空 SQLite 表格並重新插入資料
        try:
            # 刪除現有數據
            self.sqlite_db.delete(table_name, None)
            
            # 插入新數據
            records_inserted = 0
            for record in mysql_data:
                # 處理可能的特殊欄位類型
                for key, value in record.items():
                    if isinstance(value, datetime):
                        record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                
                # 插入記錄
                self.sqlite_db.insert_record(table_name, record)
                records_inserted += 1
            
            print(f"成功同步 {table_name}: 插入了 {records_inserted} 條記錄")
            return records_inserted
        except Exception as e:
            print(f"同步表格 {table_name} 時發生錯誤: {e}")
            return 0
    
    def synchronize_all(self):
        """同步所有表格"""
        start_time = time.time()
        total_records = 0
        
        for table in self.tables:
            records = self.synchronize_table(table)
            total_records += records
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n同步完成!")
        print(f"總共同步了 {total_records} 條記錄")
        print(f"耗時: {duration:.2f} 秒")
        
        # 記錄同步時間
        with open("last_sync.txt", "w") as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 使用範例
if __name__ == "__main__":
    # MySQL 連接配置
    mysql_config = {
        "host": "172.16.1.221",
        "user": "root",
        "password": "1qaz@WSX",
        "port":"13306",
        "database": "DoorSecurity"
    }
    #初始化
    # SQLite 配置
    sqlite_db_path = "DoorSecurity_controller_local_db"
    sqlite_password = "1qaz@WSX3edc"
    
    # 建立同步器
    synchronizer = MySQLtoSQLiteSynchronizer(mysql_config, sqlite_db_path, sqlite_password)
    
    # 執行同步
    synchronizer.synchronize_all()