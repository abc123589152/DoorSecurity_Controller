import tinydb_start_sync as ts
db_path = "/mnt/secure_data/encrypted_db.json" 
tinydb = ts.tinydb_init_sync(db_path)
tinydb.init_tinydb()