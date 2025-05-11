from tinydb import TinyDB, Query
from dbconnect_new import dbConnect_new

def insertDatatoTinydb(tablename):
    # 假設你已經從MySQL取得的數據
    mysql_data = dbConnect_new(f"Select *FROM {tablename}",False,"")

    # 創建或打開TinyDB數據庫
    db = TinyDB('door_control_system.json')

    # 使用Table來組織數據
    door_table = db.table(tablename)

    # 處理None值
    for item in mysql_data:
        for key, value in item.items():
            if value is None:
                item[key] = ''  # 將None轉換為空字符串

    # 檢查記錄是否已存在，不存在則新增
    Door = Query()
    new_count = 0
    existing_count = 0

    for item in mysql_data:
        # 檢查記錄是否已存在（根據id檢查）
        if not door_table.contains(Door.id == item['id']):
            # 記錄不存在，新增它
            door_table.insert(item)
            new_count += 1
        else:
            # 記錄已存在，跳過
            existing_count += 1

    print(f"處理完成：新增了{new_count}條記錄，{existing_count}條記錄已存在（被跳過）")

    # 可選：如果想查看當前表中的所有記錄
    all_records = door_table.all()
    print(f"表中共有{len(all_records)}條記錄")

    # 不需要顯式關閉TinyDB

if __name__ == "__main__":
    #doorsetting
    insertDatatoTinydb("doorsetting")
    #eventAction
    insertDatatoTinydb("eventAction")
    #controllerInput
    insertDatatoTinydb("controllerInput")
    #controllerOutput
    insertDatatoTinydb("controllerOutput")
    insertDatatoTinydb("door_status")
