/*
 * linked with -lpthread -lwiringPi -lrt
 */
 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include <wiringPi.h>
 #include <time.h>
 #include <unistd.h>
 #include <memory.h>
 #include <curl/curl.h>
 #define PIN_0 17 // GPIO Pin 17 | Green cable | Data0
 #define PIN_1 18 // GPIO Pin 18 | White cable | Data1
 #define PIN_SOUND 25 // GPIO Pin 26 | Yellow cable | Sound
 
 #define MAXWIEGANDBITS 32
 #define READERTIMEOUT 3000000
 #define LEN 256
 #define MAX_LINE_LENGTH 256
 static unsigned char __wiegandData[MAXWIEGANDBITS];
 static unsigned long __wiegandBitCount;
 static struct timespec __wiegandBitTime;
 
 void getData0(void) {
     if (__wiegandBitCount / 8 < MAXWIEGANDBITS) {
         __wiegandData[__wiegandBitCount / 8] <<= 1;
         __wiegandBitCount++;
     }
     clock_gettime(CLOCK_MONOTONIC, &__wiegandBitTime);
 }
 
 void getData1(void) {
     if (__wiegandBitCount / 8 < MAXWIEGANDBITS) {
         __wiegandData[__wiegandBitCount / 8] <<= 1;
         __wiegandData[__wiegandBitCount / 8] |= 1;
         __wiegandBitCount++;
     }
     clock_gettime(CLOCK_MONOTONIC, &__wiegandBitTime);
 }
 
 int wiegandInit(int d0pin, int d1pin) {
     // Setup wiringPi
     //wiringPiSetup() ;
     wiringPiSetupGpio();
     pinMode(d0pin, INPUT);
     pinMode(d1pin, INPUT);
     pinMode(PIN_SOUND, OUTPUT);
     // 啟用內建上拉電阻
     pullUpDnControl(d0pin, PUD_UP);
     pullUpDnControl(d1pin, PUD_UP);
     wiringPiISR(d0pin, INT_EDGE_FALLING, getData0);
     wiringPiISR(d1pin, INT_EDGE_FALLING, getData1);
 }
 
 void wiegandReset() {
     memset((void *)__wiegandData, 0, MAXWIEGANDBITS);
     __wiegandBitCount = 0;
 }
 
 int wiegandGetPendingBitCount() {
     struct timespec now, delta;
     clock_gettime(CLOCK_MONOTONIC, &now);
     delta.tv_sec = now.tv_sec - __wiegandBitTime.tv_sec;
     delta.tv_nsec = now.tv_nsec - __wiegandBitTime.tv_nsec;
 
     if ((delta.tv_sec > 1) || (delta.tv_nsec > READERTIMEOUT))
         return __wiegandBitCount;
 
     return 0;
 }
 
 int wiegandReadData(void* data, int dataMaxLen) {
     if (wiegandGetPendingBitCount() > 0) {
         int bitCount = __wiegandBitCount;
         int byteCount = (__wiegandBitCount / 8) + 1;
         memcpy(data, (void *)__wiegandData, ((byteCount > dataMaxLen) ? dataMaxLen : byteCount));
 
         wiegandReset();
         return bitCount;
     }
     return 0;
 }
 
 void printCharAsBinary(unsigned char ch) {
     int i;
     for (i = 0; i < 8; i++) {
         printf("%d", (ch & 0x80) ? 1 : 0);
         ch <<= 1;
     }
 }
 
 
 void makeBeep(int millisecs, int times){
     int i;
     for (i = 0; i < times; i++) {
         digitalWrite (PIN_SOUND,  LOW);
         delay(millisecs);
         digitalWrite (PIN_SOUND, HIGH);
         delay(millisecs/2);
     }
 }
 // 轉換成10進制號碼
void printDataAsDecimal(char* data, int bytes) {
    unsigned long long decimal_value = 0;
    
    for (int i = 0; i < 4; i++) {
        decimal_value = (decimal_value << 8) | (unsigned char)data[i];
    }
    
    printf("%llu", decimal_value);
    
}
// 轉換成10進制號碼
unsigned long long convertToDecimal(char* data, int bytes) {
    unsigned long long decimal_value = 0;
    
    for (int i = 0; i < 4; i++) {
        decimal_value = (decimal_value << 8) | (unsigned char)data[i];
    }
    
    return decimal_value;  // 返回值而不是直接打印
}
// 回调函数用于接收响应数据
size_t write_callback(char *ptr, size_t size, size_t nmemb, void *userdata) {
    // 简单地打印收到的数据
    printf("%.*s", (int)(size * nmemb), ptr);
    return size * nmemb;
}
//取得Raspberry Pi IP address
char get_raspberry_ip(char *buffer,size_t buffer_size){
   FILE *file;
   file = fopen("controller_output_containerID.conf","r");
   if(file == NULL){
      perror("無法打開文件");
      return 1;
   }
   while(fgets(buffer,buffer_size,file)!=NULL){
       buffer[strcspn(buffer,"\n")] = 0;
   }
   fclose(file);
   return 0;
}
void curlfunction(char* cardnumber,int argc,char *argv[]){
    CURL *curl;
    CURLcode res;
    char raspberry_ip_address[20];
    // 初始化libcurl
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    int result = get_raspberry_ip(raspberry_ip_address,sizeof(raspberry_ip_address));
    if(curl) {
        // 设置API的URL
        // 默认使用localhost，如果命令行提供参数则使用参数
        const char *url = argc > 1 ? argv[1] : "http://controller-gpio-output-base:8000/api/check/permition/";
        //char cardnumber[100] = "2291941972";
        char doorname[100] = "D566";
        char full_url[300];
        snprintf(full_url, sizeof(full_url), "%s%s%s/%s",url,raspberry_ip_address, doorname, cardnumber);
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
}
 int main(int argc, char *argv[]) {
     int i;
 
     wiegandInit(PIN_0, PIN_1);
 
 
     while(1) {
         int bitLen = wiegandGetPendingBitCount();
         if (bitLen == 0) {
             usleep(5000);
         } else {
             char data[100];
             char string1[100];
             bitLen = wiegandReadData((void *)data, 100);
             int bytes = bitLen / 8 + 1;
             printf("%lu ", (unsigned long)time(NULL));
             printf("Read %d bits (%d bytes): ", bitLen, bytes);
             for (i = 0; i < bytes; i++)
                 printf("%02X", (int)data[i]);
 
             printf(" : ");;
             for (i = 0; i < bytes; i++)
                 printCharAsBinary(data[i]);
             // 輸出十進制
             printDataAsDecimal(data, bytes);
             printf("\n");
             // 轉換成十進制
             unsigned long long card_number = convertToDecimal(data, bytes);
             // 轉換成字串
             char card_string[32];
             snprintf(card_string, sizeof(card_string), "%llu", card_number);
             curlfunction(card_string,argc,argv);
             makeBeep(200, 1);
         }
     }
 }
