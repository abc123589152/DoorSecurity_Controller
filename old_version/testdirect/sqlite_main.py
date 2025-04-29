from pysqlcipher3 import dbapi2 as sqlcipher
import pandas as pd
import os
class sqlcipherClass:
    def __init__(self,db_path,password):
        self.db_path = db_path
        self.conn = sqlcipher.connect(db_path)
        self.password = password
        self.cursor = self.conn.cursor()
        # Set encryption key (password)
        self.cursor.execute(f"PRAGMA key = '{self.password}';")
        
        # Optional: Set encryption settings
        self.cursor.execute("PRAGMA cipher_page_size = 4096;")  # Default is 1024
        self.cursor.execute("PRAGMA kdf_iter = 64000;")         # Default is 64000
        self.cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA512;")  # Default in SQLCipher 4.x
    #建立資料庫
    def create_encrypted_db(self):
        try:
            check_file_exist = os.path.isfile(self.db_path)
            
            if check_file_exist:
                print(f"{self.db_path} 資料庫已經存在")
                # 檢查是否可以讀取資料庫
                try:
                    self.cursor.execute("SELECT count(*) FROM sqlite_master;")
                    self.cursor.fetchone()
                    print("成功連接到現有資料庫")
                except Exception as e:
                    print(f"連接到現有資料庫時發生錯誤: {e}")
                    return False
            sql_table_script = """
                CREATE TABLE IF NOT EXISTS doorsetting (
                    id INTEGER PRIMARY KEY,
                    control TEXT,
                    wiegand TEXT,
                    fingerprint_mode TEXT,
                    door TEXT,
                    door_sensor TEXT,
                    door_lock TEXT,
                    doorRelease_button TEXT,
                    reset_time TEXT,
                    openTimeLimit TEXT,
                    remark TEXT,
                    creation_time TEXT,
                    modification_time TEXT
                );
                CREATE TABLE IF NOT EXISTS employ(
                    id INTEGER PRIMARY KEY ,
                    username TEXT,
                    cardnumber TEXT,
                    doorgroup TEXT,
                    status TEXT,
                    activation TEXT,
                    expiration TEXT,
                    remark TEXT,
                    creation_time TEXT,
                    modification_time TEXT
                );
                CREATE TABLE IF NOT EXISTS door_status(
                    id INTEGER PRIMARY KEY ,
                    doorname TEXT,
                    doorstatus TEXT,
                    quickOpen TEXT,
                    keepDoorOpen TEXT,
                    checkDoorPermition TEXT
                );
                CREATE TABLE IF NOT EXISTS doorgroup(
                    id INTEGER PRIMARY KEY ,
                    groupname TEXT,
                    doorname TEXT,
                    remark TEXT,
                    creation_time TEXT,
                    modification_time TEXT
                );
                CREATE TABLE IF NOT EXISTS eventAction (
                    id INTEGER PRIMARY KEY,
                    eventName TEXT,
                    doorName TEXT,
                    eventClass TEXT,
                    outputPort TEXT,
                    remark TEXT,
                    eventStat TEXT,
                    creation_time TEXT,
                    modification_time TEXT
                );
                CREATE TABLE IF NOT EXISTS controllerInput (
                    id INTEGER PRIMARY KEY,
                    controller TEXT,
                    inputType TEXT,
                    inputName TEXT,
                    inputPort TEXT,
                    inputStat TEXT,
                    remark TEXT,
                    creation_time TEXT,
                    modification_time TEXT
                );
                 CREATE TABLE IF NOT EXISTS controllerOutput (
                    id INTEGER PRIMARY KEY,
                    controller TEXT,
                    outputType TEXT,
                    outputName TEXT,
                    outputPort TEXT,
                    outputStat TEXT,
                    remark TEXT,
                    creation_time TEXT,
                    modification_time TEXT
                );
            """
            # 無論資料庫是否存在，都嘗試創建表格
            print("初始話作業開始創建表格")
            # 執行腳本
            self.cursor.executescript(sql_table_script)
            self.conn.commit()   
            # 驗證表格是否存在
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result = self.cursor.fetchone()
            if result:
                print(f"表格都已成功創建或已存在")
            else:
                print("表格創建失敗")
                return False
            return self.conn
        except Exception as e:
            print(f"創建加密資料庫時發生錯誤: {e}")
            return False
                
        except sqlcipher.DatabaseError as e:
                if "file is not a database" in str(e):
                    print(f"檔案存在，但不是有效的 SQLCipher 資料庫或密碼不正確")
                else:
                    print(f"資料庫錯誤: {e}")
                return False
        except Exception as e:
                print(f"發生錯誤: {e}")
                return False
    def dict_query(self,sql_query,params=None):
        try:
            if params:
                df = pd.read_sql_query(sql_query,self.conn,params=params)
            else:
                df = pd.read_sql_query(sql_query,self.conn)
        
            result_dict = df.to_dict(orient="records")
            return result_dict
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error executing query: {e}")
    def array_query(self,sql_query,params=None):
        try:
            if params:
                self.cursor.execute(sql_query,params)
            else:
                self.cursor.execute(sql_query)
            result_arr = self.cursor.fetchall()
            return result_arr
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error executing query: {e}")
    #sqlite新增資料
    def insert_record(self, table_name, column_data):
        try:
            cursor = self.conn.cursor()
            
            # Extract column names and values from the dictionary
            columns = ', '.join(column_data.keys())
            placeholders = ', '.join(['?'] * len(column_data))
            values = tuple(column_data.values())
            
            # Build and execute SQL statement
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            # Get the ID of the last inserted row
            last_row_id = cursor.lastrowid
            
            # Commit changes
            self.conn.commit()
            
            return last_row_id
        except sqlcipher.Error as e:
            # Rollback on error
            self.conn.rollback()
            raise Exception(f"Error occurred during data insertion: {e}")
    def update_record(self, table_name, column_data, condition_data):
        try:
            cursor = self.conn.cursor()
            # Build SET clause
            set_clause = ', '.join([f"{column} = ?" for column in column_data.keys()])
            set_values = list(column_data.values())
            
            # Build WHERE clause
            where_clause = ' AND '.join([f"{column} = ?" for column in condition_data.keys()])
            where_values = list(condition_data.values())
            
            # Combine all values
            all_values = set_values + where_values
            
            # Build and execute complete SQL statement
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            cursor.execute(query, all_values)
            
            # Get number of affected rows
            rows_affected = cursor.rowcount
            
            # Commit changes
            self.conn.commit()
            
            return rows_affected
            
        except sqlcipher.Error as e:
            # Rollback on error
            self.conn.rollback()
            raise Exception(f"Error occurred during data update: {e}")
    def delete(self,table_name,colume_name,params=None):
        try:
            if params:
                self.cursor.execute("delete from "+table_name+" where "+colume_name+" = ?",params)
            else:
                self.cursor.execute("delete from "+table_name)
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error occurred during data update: {e}")