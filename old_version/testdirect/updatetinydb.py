# from tinydb import TinyDB, Query

# db = TinyDB("door_control_system.json")
# data = {'id': 66, 'control': '172.16.1.195', 'wiegand': 'Wiegand1', 'fingerprint_mode': '', 'door': 'D838', 'door_sensor': '4', 'door_lock': '14', 'doorRelease_button': '6', 'reset_time': '5', 'openTimeLimit': '5', 'remark': '用來測試程式的門禁', 'creation_time': '2025-04-02 10:58:44', 'modification_time': ''}
# doorsetting_table = db.table("doorsetting")

# update_query = Query()

# doorsetting_table.update(data,update_query.id == 66)

# print("===================")
# print(doorsetting_table.all())
# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.settimeout(2)                                      #2 Second Timeout
# result = sock.connect_ex(('172.16.1.100',13306))
# if result == 0:
#   print('port OPEN')
# else:
#   print('port CLOSED, connect_ex returned: '+str(result))
# import json
# import os
# from datetime import datetime

# file_path = "events_log.json"

# # 检查文件是否存在，如果不存在则创建一个空列表
# if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
#     with open(file_path, "w", encoding="utf-8") as file:
#         json.dump([], file)

# # 读取现有数据
# with open(file_path, "r", encoding="utf-8") as file:
#     events = json.load(file)
# # 添加新事件
# new_event = {
#     "eventName": "测试事件" + str(len(events) + 1),
#     "eventClass": "HaltOpen",
#     "eventCause": "systemAction",
#     "timeToEvent": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#     "eventStatus": "unconfirmed"
# }

# events.append(new_event)

# # 写回文件
# with open(file_path, "w", encoding="utf-8") as file:
#     json.dump(events, file, ensure_ascii=False, indent=4)

# print(f"已添加新事件，当前共有 {len(events)} 条记录")
import socket
from time import sleep

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("172.16.1.100",13306))
    print(result)
    sleep(1)
