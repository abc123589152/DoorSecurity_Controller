from datetime import datetime
import httpx
class forceopenclass():
    def __init__(self,doorname,eventaction_table,query_table,asyncio,loop,door_info,dbConnect_new,check_port_async,read_mysql_ip,check_port_with_socket,http_client,broadcast_update,controllerOutput_table):
        self.doorname = doorname
        self.eventAction_table = eventaction_table
        self.query_table = query_table
        self.asyncio = asyncio
        self.loop = loop
        self.door_info = door_info
        self.dbConnect_new = dbConnect_new
        self.check_port_async = check_port_async
        self.read_mysql_ip = read_mysql_ip
        self.check_port_with_socket = check_port_with_socket
        self.http_client = http_client
        self.broadcast_update = broadcast_update
        self.controllerOutput_table = controllerOutput_table
    def forceopen_eventfunction(self):
        get_event = self.eventAction_table.search((self.query_table.doorName == self.doorname)&(self.query_table.eventClass == "ForceOpen"))
        if not get_event:
            print(f"{self.doorname} not have ForceOpen event so do noting!")
            state_message = {
                'door_status_id': self.door_info.get('door_status', {}).get('id', 0),
                'state': "強迫開門",
                'states':"ForceOpen"
            }
            # 將廣播任務提交給事件循環
            self.asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), self.loop)
        else:
            state_message = {
                'door_status_id': self.door_info.get('door_status', {}).get('id', 0),
                'state': "強迫開門",
                'states':"ForceOpen"
            }
            # 將廣播任務提交給事件循環
            self.asyncio.run_coroutine_threadsafe(self.broadcast_update(state_message), self.loop)
            #Check DoorSecurity mysql database可以連接到
            result = self.asyncio.run(self.check_port_async(self.read_mysql_ip(),13306))
            if result:
                print("Connect DoorSecurity database successful.")
                    #新增開門過久事件log到mysql
                getnowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.dbConnect_new("INSERT INTO eventLog(eventName,eventClass,eventCause,timeToEvent,eventStatus)VALUES(%s,%s,%s,%s,%s)", True, (get_event[0]['eventName'], "ForceOpen", "systemAction", getnowtime, "unconfirmed"))
                self.dbConnect_new("UPDATE eventAction SET eventStat = %s where eventName = %s ",True,("active",get_event[0]['eventName']))
            else:
                #如果連結DoorSecurity database異常就會將資訊先暫存到未同步的本地資料庫進行儲存
                print("No connect mysql server!")
                getnowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_unsync_event = {
                    "eventName": get_event[0]['eventName'],
                    "eventClass": "HaltOpen",
                    "eventCause": "systemAction",
                    "timeToEvent": getnowtime,
                    "eventStatus": "unconfirmed"   
                }
                new_event_action_data = {
                    "eventName":get_event[0]['eventName'],
                    "status": "active"
                }
            output_names = get_event[0]['outputPort'].split(",")
            # 用於儲存按 controller 分組的結果
            controller_groups = {}
            # 遍歷每個 outputName
            for output in output_names:
                # 查詢符合 outputName 的記錄
                output_results = self.controllerOutput_table.search(self.query_table.outputName == output)
                # 遍歷查詢結果
                for item in output_results:
                    controller = item['controller']
                    port = item['outputPort']
                    # 如果這個 controller 尚未在分組字典中，創建一個新的列表
                    if controller not in controller_groups:
                        controller_groups[controller] = []
                    # 將 port 添加到相應的 controller 組
                controller_groups[controller].append(port)
            for controller, ports in controller_groups.items():
                eventAction_url = f"http://{controller}:5020/eventaction/output/active"
                check_controller_output_status = f"http://{controller}:5020/api/output/status"
                #payload = {"outputPort": ["15", "16"]}  # 需要開啟的 GPIO port
                dict_output = {
                    "outputPort": ports,
                    "eventName": get_event[0]['eventName']
                }
                try:
                    response = self.check_port_with_socket(self.read_mysql_ip(),13306)
                    if response:
                        print(f"連接成功！API回應: {response} ,可以重新進行Event API 派送")
                        with httpx.Client() as client:
                            response = client.post(eventAction_url, json=dict_output)
                            print(response.json())
                    else:
                        print("DoorSecurity mysql 資料庫連接失敗")
                except Exception as e:
                    print(f"測試mysql連線發生錯誤，錯誤記錄訊息:{str(e)}")
        return 