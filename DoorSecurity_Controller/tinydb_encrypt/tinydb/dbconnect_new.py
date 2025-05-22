import mysql.connector as mysql
from mysql.connector.pooling import MySQLConnectionPool
import time

# 全局連接池，只在模塊載入時創建一次
mysql_db_ip = "192.168.110.131"
dbconfig = {
    "host": mysql_db_ip,
    "user": "root",
    "passwd": "1qaz@WSX",
    "database": "DoorSecurity",
    "port": "13306"
}

# 建立連接池，調整 pool_size 可以控制同時維持的連接數量
try:
    pool = MySQLConnectionPool(
        pool_name="door_security_pool",
        pool_size=5,  # 同時維持的連接數，可根據需求調整
        pool_reset_session=True,  # 每次使用前重置會話狀態
        **dbconfig
    )
    print("數據庫連接池初始化成功")
except Exception as e:
    print(f"數據庫連接池初始化失敗: {e}")
    # 如果連接池初始化失敗，後續將使用普通連接作為備用方案

def dbConnect_new(sqlCommand,check,params1):
    """使用連接池執行SQL查詢"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 嘗試從連接池獲取連接
            if 'pool' in globals():
                conn = pool.get_connection()
                cursor = conn.cursor(dictionary=True)
                if check:
                    cursor.execute(sqlCommand, params1)
                else:
                    cursor.execute(sqlCommand)
                result = cursor.fetchall()
                cursor.close()
                conn.close()  # 將連接返回到池中，而不是真正關閉
                return result
            else:
                # 如果連接池初始化失敗，使用普通連接作為備用
                return dbConnect_legacy(sqlCommand, params1)
        except mysql.errors.PoolError:
            # 連接池已滿，等待短暫時間後重試
            time.sleep(0.1)
            retry_count += 1
        except Exception as e:
            print(f"數據庫查詢錯誤: {e}")
            # 特定錯誤可能需要重新連接
            if 'Connection' in str(e):
                retry_count += 1
                time.sleep(0.5)
            else:
                # 其他錯誤直接返回空結果
                return []
    
    # 如果所有重試都失敗，使用普通連接
    return dbConnect_legacy(sqlCommand, params1)

def dbConnect_legacy(sqlCommand, params1):
    """如果連接池不可用，使用普通連接作為備用方案"""
    try:
        db = mysql.connect(**dbconfig)
        ConnectDB = db.cursor(dictionary=True)
        ConnectDB.execute(sqlCommand, params1)
        ConnectDB_result = ConnectDB.fetchall()
        ConnectDB.close()
        db.close()
        return ConnectDB_result
    except Exception as e:
        print(f"備用連接錯誤: {e}")
        return []

# 提供一個關閉連接池的函數，通常在程式結束時調用
def close_pool():
    """關閉連接池，釋放所有連接"""
    if 'pool' in globals():
        # 實際上 MySQLConnectionPool 沒有直接的關閉方法
        # 但如果將來 API 變更或使用其他連接池庫，這裡可以處理關閉邏輯
        print("連接池資源已釋放")
