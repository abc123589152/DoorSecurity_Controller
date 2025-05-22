step1.第一步驟創建mysql-connector-json的檔案裡面包含以下的資訊
{
    "name": "mysql-connector",
    "config": {
      "connector.class": "io.debezium.connector.mysql.MySqlConnector",
      "database.hostname": "172.16.1.66",
      "database.port": "13306",
      "database.user": "root",
      "database.password": "1qaz@WSX",
      "database.server.id": "184054",
      "topic.prefix": "mysql_master",
      "database.include.list": "DoorSecurity",
      "table.include.list": "cdc_test.customers,DoorSecurity.doorsetting",
      "schema.history.internal.kafka.bootstrap.servers": "172.16.1.66:9092",
      "schema.history.internal.kafka.topic": "schema-changes.cdc_test",
      "schema.history.internal": "io.debezium.storage.kafka.history.KafkaSchemaHistory",
      "include.schema.changes": "true",
      "snapshot.mode": "initial",
      "tombstones.on.delete": "false",
      "database.allowPublicKeyRetrieval": "true",
      "database.ssl.mode": "disabled"
    }
  }

Step2.開始註冊Topic到kafka裡面，使用指令的方式進行，這裡的步驟是會先POST到debezium conector在上面建立一個連接的資訊，然後再轉拋到kafka上面，當新增完畢後不會跳出error log就算成功了，8083
port 就是debezium的port號碼
curl -X POST -H "Content-Type: application/json" --data @mysql-connector.json http://localhost:8083/connectors
新增完畢後再kafka裡面的topic就建立完畢

Step3.開始進行kafka監控到mysql變化將其同步到加密過後的tinyDB