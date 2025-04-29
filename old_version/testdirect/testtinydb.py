from tinydb import TinyDB, Query

# 打開之前創建的 TinyDB 數據庫
db = TinyDB('door_control_system.json')

# 獲取 door_access 表
door_table = db.table('doorsetting')
event_table = db.table('eventAction')
controllerOutput_table = db.table("controllerOutput")
# 獲取所有記錄
all_records = door_table.all()
print(f"資料庫中共有 {len(all_records)} 條記錄\n")
while True:
    choice = input("1.print all json,2.end")
    if choice == "1":
        print(all_records)
    else:
        print("Exit program.")
        break
# # 顯示所有記錄的重要信息，特別是包含中文的欄位
# print("==== 記錄詳情 ====")
# for i, record in enumerate(all_records):
#     print(f"\n記錄 #{i+1}:")
#     print(f"ID: {record['id']}")
#     print(f"門禁: {record['door']}")
#     print(f"控制器IP: {record['control']}")
#     print(f"Wiegand: {record['wiegand']}")
#     print(f"備註: {record['remark']}")  # 特別檢查這個字段中的中文

# # 測試查詢功能
# Input = Query()
# #print(all_records)
# # 查詢特定ID的記錄
# #gpio_pin = 20  # 這是有中文備註的記錄之一
# # 查詢所有 controller 為 "172.16.1.195" 的記錄
# # results = door_table.search(
# #     (Input.controllerInput.any(lambda _, value: 
# #         value['controller'] == '172.16.1.195' and 
# #         value['inputPort'] == '9'
# #     ))
# # )
# results = event_table.search((Input.doorName == "D892") & (Input.eventClass == "HaltOpen"))
# output_names = results[0]['outputPort'].split(",")

# # 用於儲存按 controller 分組的結果
# controller_groups = {}

# # 遍歷每個 outputName
# for output in output_names:
#     # 查詢符合 outputName 的記錄
#     output_results = controllerOutput_table.search(Input.outputName == output)
    
#     # 遍歷查詢結果
#     for item in output_results:
#         controller = item['controller']
#         port = item['outputPort']
        
#         # 如果這個 controller 尚未在分組字典中，創建一個新的列表
#         if controller not in controller_groups:
#             controller_groups[controller] = []
        
#         # 將 port 添加到相應的 controller 組
#         controller_groups[controller].append(port)

# # 輸出結果
# for controller, ports in controller_groups.items():
#     print(f"Controller: {controller}, Ports: {ports}")

    #listarr.append((controllerOutput_table.search(Input.outputName == "output"))[0])
#print(listarr)

# if result:
#     print(f"\n\n==== 查詢ID為{record_id}的記錄 ====")
#     print(f"ID: {result['id']}")
#     print(f"門禁: {result['door']}")
#     print(f"備註: {result['remark']}")  # 檢查中文是否正確

# # 查詢包含特定中文字符的記錄
# chinese_keyword = "測試"
# results = door_table.search(Door.remark.search(chinese_keyword))
# print(f"\n\n==== 查詢備註包含「{chinese_keyword}」的記錄 ====")
# print(f"找到 {len(results)} 條符合條件的記錄")
# for i, record in enumerate(results):
#     print(f"\n結果 #{i+1}:")
#     print(f"ID: {record['id']}")
#     print(f"門禁: {record['door']}")
#     print(f"備註: {record['remark']}")

# print("\n測試完成！")