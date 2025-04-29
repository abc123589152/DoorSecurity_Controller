import socket
import asyncio
import tinydb
from time import sleep
from dbconnect_query import dbConnect_query
async def check_port_async(host, port, timeout=1):
    try:
        # 使用帶超時的連接協程
        fut = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
        # 關閉連接
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False
while True:
    db = tinydb.TinyDB("unsync_data.json")
    # 獲取 unsync_event_log_table 表格
    unsync_event_log_table = db.table("unsync_event_log_table")
    all_event_records = unsync_event_log_table.all()
    with open("mysql_ip.conf","r") as mysql_ip:
        mysqlip = mysql_ip.read().strip()
        result = asyncio.run(check_port_async(mysqlip, 13306))
        if result:
            Event = tinydb.Query()
            if len(all_event_records)>0:
                for eventlog in all_event_records:
                    print(f"將還未同步的訊息{eventlog['eventName']}加入到主資料庫，加入完畢後刪除這筆未同步資訊")
                    removed_count = unsync_event_log_table.remove(Event.eventName == eventlog['eventName'])
            else:
                print("目前未有未同步之資料")
        sleep(15)