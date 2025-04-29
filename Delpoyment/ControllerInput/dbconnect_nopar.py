import mysql.connector as mysql
def dbConnect_noparams(sqlCommand):
    mysql_db_ip = "172.16.1.103"
    db = mysql.connect(
    host = mysql_db_ip,
    user = "root",
    passwd = "1qaz@WSX",
    database = "DoorSecurity",
    port = "13306"
    )
    ConnectDB = db.cursor(dictionary=True)
    ConnectDB.execute(sqlCommand)
    ConnectDB_result = ConnectDB.fetchall()
    db.close()
    return ConnectDB_result