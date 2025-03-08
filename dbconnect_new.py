import mysql.connector as mysql
import os
def dbConnect_new(sqlCommand,params1):
    mysql_db_ip = "172.16.1.100"
    db = mysql.connect(
    host = mysql_db_ip,
    user = "root",
    passwd = "1qaz@WSX",
    database = "DoorSecurity",
    port = "13307"
    )
    ConnectDB = db.cursor(dictionary=True)
    ConnectDB.execute(sqlCommand,params1)
    ConnectDB_result = ConnectDB.fetchall()
    return ConnectDB_result