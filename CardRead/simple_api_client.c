#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

// 回调函数用于接收响应数据
size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    // 简单地打印收到的数据
    printf("%.*s", (int)(size * nmemb), ptr);
    return size * nmemb;
}

int main(int argc, char *argv[]) {
    CURL *curl;
    CURLcode res;
    
    // 初始化libcurl
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    
    if(curl) {
        // 设置API的URL
        // 默认使用localhost，如果命令行提供参数则使用参数
        const char *url = argc > 1 ? argv[1] : "http://localhost:8000/api/check/permition";
        char cardnumber[100] = "2291941972";
        char doorname[100] = "D566";
        char full_url[300];
        snprintf(full_url, sizeof(full_url), "%s%s/%s", url, doorname, cardnumber);
        printf("正在请求: %s\n", full_url);
        
        // 设置URL
        curl_easy_setopt(curl, CURLOPT_URL, full_url);
        
        // 设置回调函数
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        // 执行请求
        res = curl_easy_perform(curl);
        
        // 检查错误
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() 失败: %s\n", curl_easy_strerror(res));
        }
        
        // 获取HTTP状态码
        long http_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
        printf("\nHTTP状态码: %ld\n", http_code);
        // 清理
        curl_easy_cleanup(curl);
    }
    
    curl_global_cleanup();
    return 0;
}