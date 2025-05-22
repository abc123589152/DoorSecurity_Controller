from tinydb import TinyDB, Query
from kafka import KafkaConsumer
import json
import threading
import time
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tinydb_encrypt.tinydb_start_sync as tinydbstart
#引入本地資料庫，並且用key進行解密
db_path = "/mnt/secure_data/encrypted_db.json"
key_path = "/mnt/secure_data/db.key"
class KafkaTinyDBSync:
    def __init__(self, topics,):
        with open("../mysql_config/mysql_ip.conf","r") as readmysql_conf:    
            bootstrap_servers=[f'{readmysql_conf.read().strip()}']
        print("開始同步資料庫")
        #先進行同步資料庫
        tinydbstart.tinydb_init_sync(db_path).init_tinydb()
        print("同步完畢開始載入資料庫")
        import tinydb_encrypt.tinydb_control_function as tinycon
        self.key = tinycon.get_encryption_key(key_path)
        self.db = tinycon.EncryptedTinyDB(db_path,self.key)
        self.Query = Query()
        # 要監聽的主題
        self.topics = topics
        # 建立 Kafka 消費者
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='tinydb-sync-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        # 初始化同步檢查
        #self.check_sync_on_startup()
    
    def process_message(self, message):
        """處理從 Kafka 接收到的消息"""
        try:
            print(f"收到消息: {message.topic}")
            
            # 從消息主題中提取表名
            topic_parts = message.topic.split('.')
            if len(topic_parts) >= 3:
                table_name = topic_parts[2]  # mysql_master.DoorSecurity.tablename
            else:
                print(f"無法從主題 {message.topic} 解析表名")
                return
            
            # 獲取 payload
            if 'payload' in message.value:
                payload = message.value['payload']
            else:
                print("消息中未找到 payload 字段")
                return
                
            # 獲取操作類型
            if 'op' in payload:
                operation = payload['op']
            else:
                print("未找到操作類型 (op)")
                return
            
            # 獲取數據
            before_data = payload.get('before')
            after_data = payload.get('after')
            
            # 打印解析結果
            print(f"操作: {operation}, 表名: {table_name}")
            
            # 取得對應表
            table = self.db.table(table_name)
            
            # 根據操作類型處理
            if operation == 'c':  # 插入
                if after_data:
                    self._handle_insert(table, after_data)
                else:
                    print("插入操作缺少 after 數據")
            elif operation == 'u':  # 更新
                if after_data:
                    self._handle_update(table, after_data)
                else:
                    print("更新操作缺少 after 數據")
            elif operation == 'd':  # 刪除
                if before_data:
                    self._handle_delete(table, before_data)
                else:
                    print("刪除操作缺少 before 數據")
            elif operation == 'r':  # 讀取 (Debezium 快照操作)
                if after_data:
                    self._handle_insert(table, after_data)
                else:
                    print("讀取操作缺少 after 數據")
            else:
                print(f"未知操作類型: {operation}")
                
        except Exception as e:
            print(f"處理消息時發生錯誤: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _handle_insert(self, table, data):
        """處理插入操作"""
        # 處理 None 值
        for key, value in data.items():
            if value is None:
                data[key] = ''
                
        # 檢查記錄是否已存在
        if not table.contains(self.Query.id == data['id']):
            table.insert(data)
            self.db._save_db()
            print(f"已插入新記錄, ID: {data['id']}")
        else:
            print(f"記錄已存在, ID: {data['id']}")
    
    def _handle_update(self, table, data):
        """處理更新操作"""
        # 處理 None 值
        for key, value in data.items():
            if value is None:
                data[key] = ''
                
        # 更新記錄
        result = table.update(data, self.Query.id == data['id'])
        self.db._save_db()
        if result:
            print(f"已更新記錄, ID: {data['id']}")
        else:
            # 如果記錄不存在，則插入
            table.insert(data)
            print(f"記錄不存在，已插入, ID: {data['id']}")
    
    def _handle_delete(self, table, data):
        """處理刪除操作"""
        # 刪除記錄
        result = table.remove(self.Query.id == data['id'])
        self.db._save_db()
        if result:
            print(f"已刪除記錄, ID: {data['id']}")
        else:
            print(f"找不到要刪除的記錄, ID: {data['id']}")
    
    def check_sync_on_startup(self):
        """啟動時檢查同步狀態"""
        print("開始檢查資料同步狀態...")
        
        for topic in self.topics:
            # 從主題提取資料庫裡面表的名稱
            topic_parts = topic.split('.')
            if len(topic_parts) >= 3:
                table_name = topic_parts[2]
                self._sync_table(table_name)
            else:
                print(f"無法從主題 {topic} 解析表名")
    
    def start_consuming(self):
        """開始消費 Kafka 消息"""
        print("開始監聽 Kafka 消息...")
        for message in self.consumer:
            self.process_message(message)
    
    def start(self):
        """啟動服務"""
        # 在另一個線程中啟動 Kafka 消費
        kafka_thread = threading.Thread(target=self.start_consuming)
        kafka_thread.daemon = True
        kafka_thread.start()
        
        print("同步服務已啟動")
        
        # 主線程保持運行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("服務正在關閉...")

if __name__ == "__main__":
    # 要監聽的 Kafka 主題
    topics = [
        'mysql_master.DoorSecurity.doorsetting',
        'mysql_master.DoorSecurity.eventAction',
        'mysql_master.DoorSecurity.controllerInput',
        'mysql_master.DoorSecurity.controllerOutput',
        'mysql_master.DoorSecurity.door_status',
        'mysql_master.DoorSecurity.doorgroup',
        'mysql_master.DoorSecurity.employ'
    ]
    
    # 創建並啟動同步服務
    sync_service = KafkaTinyDBSync(topics)
    sync_service.start()