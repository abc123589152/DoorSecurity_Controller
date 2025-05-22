#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>  // 用於chmod函式
#include <ifaddrs.h>
#include <netinet/in.h>
#include <arpa/inet.h>
//IP抓取到後存放的位置
#define IP_FILE "/opt/eth0_ip.txt"
#define IP_FILE_WLAN "/opt/wlan_ip.txt"
//
#define INTERFACE "eth0"
#define INTERFACE_WLAN "wlan0"
#define CHECK_INTERVAL 1  // 檢查間隔時間

// Get當下的時間
char* get_time_str() {
    static char time_str[64];
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    
    strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", tm_info);
    return time_str;
}

// Get指定interface的IP
int get_interface_ip(const char *interface, char *ip_buffer, size_t buffer_size) {
    struct ifaddrs *ifaddr, *ifa;
    int found = 0;
    
    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return 0;
    }
    
    // 尋找出所有的網卡
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL)
            continue;
            
        // 只要抓取IPV4
        if (ifa->ifa_addr->sa_family == AF_INET && strcmp(ifa->ifa_name, interface) == 0) {
            struct sockaddr_in *addr = (struct sockaddr_in *)ifa->ifa_addr;
            inet_ntop(AF_INET, &addr->sin_addr, ip_buffer, buffer_size);
            found = 1;
            break;
        }
    }
    
    freeifaddrs(ifaddr);
    return found;
}

//將IP寫入到IP的File檔案裡面
void write_ip_to_file(const char *ip,int check) {
    if(check==0){
        FILE *file = fopen(IP_FILE, "w");
        if (file == NULL) {
            perror("Error opening file");
            return;
        }
        
        fprintf(file, "%s", ip);
        fclose(file);
        
        // 設定IP資訊File文件的權限只有管理者可以讀寫
        chmod(IP_FILE, 0644);
        
        printf("[%s] IP address update successful: %s\n", get_time_str(), ip);
    }else if(check == 1){
        FILE *file = fopen(IP_FILE_WLAN, "w");
        if (file == NULL) {
            perror("Error opening file");
            return;
        }
        
        fprintf(file, "%s", ip);
        fclose(file);
        
        // 設定IP資訊File文件的權限只有管理者可以讀寫
        chmod(IP_FILE, 0644);
        
        printf("[%s] IP address update successful: %s\n", get_time_str(), ip);
    }
   
}

int main() {
    char current_ip[INET_ADDRSTRLEN] = {0};
    char last_ip[INET_ADDRSTRLEN] = {0};
    char current_wlan_ip[INET_ADDRSTRLEN] = {0};
    char last_wlan_ip[INET_ADDRSTRLEN] = {0};
    
    printf("start monitor  %s port IP address change...\n", INTERFACE);
    printf("IP address save by : %s\n", IP_FILE);
    
    // 无限循环，定期检查
    while (1) {
        // 获取当前IP
        if (get_interface_ip(INTERFACE, current_ip, INET_ADDRSTRLEN) & get_interface_ip(INTERFACE_WLAN,current_wlan_ip,INET_ADDRSTRLEN)) {
            // 如果IP有變化或是第一次檢查IP
            // if (strcmp(current_ip, last_ip) != 0) {
            //     // 更新文件
            //     write_ip_to_file(current_ip,0);
            //     // 更新暫存的IP
            //     strcpy(last_ip, current_ip);
            // }
            //wlan 如果有變化也要更新
            if (strcmp(current_wlan_ip,last_wlan_ip)!=0){
                write_ip_to_file(current_wlan_ip,1);
                strcpy(last_wlan_ip,current_wlan_ip);
            }
        } 
        // 等待間隔的時間
        sleep(CHECK_INTERVAL);
    }
    
    return 0;
}