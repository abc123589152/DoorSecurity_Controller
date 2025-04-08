from dbconnect_new import dbConnect_new
Get_doorsetting = dbConnect_new("Select *FROM doorsetting",False,"")
print(Get_doorsetting)