#include <stdio.h>
#include <sqlite3.h>  // 這實際上是SQLCipher的頭文件

int main() {
    sqlite3 *db;
    int rc;
    char *err_msg = 0;
    
    // 打開資料庫連接
    rc = sqlite3_open("encrypted.db", &db);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }
    
    // 提供密碼以解密資料庫
    rc = sqlite3_exec(db, "PRAGMA key = '1qaz@WSX3edc';", 0, 0, &err_msg);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    
    // 嘗試讀取資料以驗證密碼是否正確
    rc = sqlite3_exec(db, "SELECT count(*) FROM sqlite_master;", 0, 0, &err_msg);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "密碼可能不正確: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    
    printf("成功打開加密資料庫！\n");
    
    // 從這裡開始，您可以正常使用SQLite API讀取和操作資料
    
    // 關閉資料庫
    sqlite3_close(db);
    return 0;
}