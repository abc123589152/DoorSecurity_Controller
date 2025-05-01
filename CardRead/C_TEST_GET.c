#include <stdio.h>
#include <string.h>
#include <curl/curl.h>

// 简单的响应缓冲区
char buffer[256];

// 回调函数
size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    // 清空缓冲区并复制响应数据
    memset(buffer, 0, sizeof(buffer));
    size_t bytes = size * nmemb;
    if(bytes < sizeof(buffer)) {
        memcpy(buffer, ptr, bytes);
    }
    return bytes;
}

int main() {
    CURL *curl;
    CURLcode res;
    int status_ok = 0;
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if(curl) {
        // 设置URL和回调
        curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5020/api/output/status");
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        
        // 执行请求
        res = curl_easy_perform(curl);
        
        if(res == CURLE_OK) {
            // 检查状态是否为ok
            if(strstr(buffer, "\"status\":\"ok\"") != NULL) {
                status_ok = 1;
            }
        }
        
        curl_easy_cleanup(curl);
    }
    
    // 输出结果
    printf("状态结果: %d\n", status_ok);
    
    curl_global_cleanup();
    return 0;
}