from sqlite_main import sqlcipherClass
import os
from dotenv import load_dotenv
import pandas as pd
from pysqlcipher3 import dbapi2 as sqlcipher 
print("Start create db...")
password = "1qaz@WSX3edc"
conn = sqlcipher.connect("./DoorSecurity_controller_local_db")
#sqlinit = sqlcipherClass("DoorSecurity_controller_local_db","1qaz@WSX3edc")
cursor = conn.cursor()
cursor.execute(f"PRAGMA key = '{password}';")
def dict_query(sql_query,params=None):
        try:
            if params:
                df = pd.read_sql_query(sql_query,conn,params=params)
            else:
                df = pd.read_sql_query(sql_query,conn)
        
            result_dict = df.to_dict(orient="records")
            return result_dict
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error executing query: {e}")
while True:
    option = input("Please input 1.show 2.exit:")
    if option == "1":            
        doorname = dict_query("select *from doorsetting where door = ?",("D892",))
        print(doorname)
    else:
        break
# sqliteconnect = sqlcipherClass("./DoorSecurity_controller.db","1qaz@WSX")
# #Create database
# sqliteconnect.create_encrypted_db()
# #insert data to sqlite database
# door_setting = {
#     "control": "172.16.1.195",
#     "wiegand": "wiegand1",
#     "fingerprint_mode": "disable",
#     "door": "D892",
#     "door_sensor": "4",
#     "door_lock": "24",
#     "doorRelease_button": "5",
#     "reset_time": "15",
#     "openTimeLimit": "180",
#     "remark": "Test door setting",
#     "creation_time": "2025-04-26 21:49:00",
#     "modification_time": ""
# }
# sqliteconnect.insert_record("doorsetting",door_setting)
# #show doorsetting data
# data = sqliteconnect.dict_query("Select *from doorsetting")
# print(f"doorsetting data is {data}")
load_dotenv()
readpass = os.environ.get('sqlite_pass')
print(readpass)