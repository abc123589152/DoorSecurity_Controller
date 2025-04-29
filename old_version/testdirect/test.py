from DoorSecurity_Controller.dbconnect_new import dbConnect_new
import httpx
import asyncio
#如何送API
async def send_gpio_output_request(output):
    url = "http://172.16.1.100:5020/eventaction/message"
    #payload = {"outputPort": ["15", "16"]}  # 需要開啟的 GPIO port
    dict_output = {"outputPort": output}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dict_output)
        print(response.json())
#Class 類別的定義
class exampletest:
    def __init__(self):
        self.password = "1qaz@WSX"
    def printpasswor(self,message):
        print(f"{message}:{self.password}")
example_class = exampletest()
example_class.printpasswor("My password")

#===========================
#資料庫的連接
Get_doorsetting_table = dbConnect_new("SELECT *from doorsetting where control = %s",("172.16.1.181",))
#事件的判斷
message = "ForceOpen"
output_arr = []
if message == "ForceOpen":
    doorname = "D892"
    Get_doorsetting_table = dbConnect_new("""SELECT *from eventAction where doorname = %s and eventClass = %s """
                                          ,(doorname,"ForceOpen"))
    print(Get_doorsetting_table[0]['outputPort'])
    outputport_list = Get_doorsetting_table[0]['outputPort'].split(",")
    for output_port in outputport_list:
        Get_port_number = dbConnect_new("SELECT *FROM controllerOutput where outputName = %s",(output_port,))
        output_arr.append(Get_port_number[0]['outputPort'])
    # 在 async 環境下執行
    asyncio.run(send_gpio_output_request(output_arr))
    



    