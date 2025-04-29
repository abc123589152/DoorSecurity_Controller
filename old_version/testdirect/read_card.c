#include <stdio.h>
#include <sqlcipher/sqlite3.h>

int main() {
    sqlite3 *db;
    sqlite3_stmt *stmt;
    int rc;
    
    // 打開加密資料庫
    rc = sqlite3_open("encrypted.db", &db);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "無法開啟資料庫: %s\n", sqlite3_errmsg(db));
        return 1;
    }
    
    // 提供密碼
    rc = sqlite3_exec(db, "PRAGMA key = '1qaz@WSX3edc';", 0, 0, 0);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "密碼錯誤: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }
    
    // 準備SQL查詢語句，帶參數
    const char *sql = "SELECT * FROM employ WHERE cardnumber = ?;";
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "準備SQL失敗: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }
    
    // 綁定參數
    sqlite3_bind_text(stmt, 1, "2291941972", -1, SQLITE_STATIC);
    
    // 執行查詢並處理結果
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        // 有結果，獲取列數
        int columns = sqlite3_column_count(stmt);
        
        printf("找到符合條件的記錄:\n");
        
        // 印出所有欄位
        for (int i = 0; i < columns; i++) {
            const char *column_name = sqlite3_column_name(stmt, i);
            const char *value = (const char *)sqlite3_column_text(stmt, i);
            
            printf("%s = %s\n", column_name, value ? value : "NULL");
        }
    } else {
        printf("沒有找到 cardnumber 為 2291941972 的記錄\n");
    }
    
    // 釋放資源
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    
    return 0;
}