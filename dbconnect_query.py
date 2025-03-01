import mysql.connector as mysql
import os
def dbConnect_query(sqlCommand, params1, many=False):
    mysql_db_ip = "172.16.1.103"
    db = mysql.connect(
        host = mysql_db_ip,
        user = "root",
        passwd = "1qaz@WSX",
        database = "DoorSecurity",
        port = "13306"
    )
    ConnectDB = db.cursor(dictionary=True)
    if many:
        ConnectDB.executemany(sqlCommand, params1)
    else:
        ConnectDB.execute(sqlCommand, params1)
    db.commit()
    db.close()
    