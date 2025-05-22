# 日誌文件路徑
LOG_FILE="./DoorSecurity_Install_log.log"

# 日誌函數
log() {
    local level=$1
    local message=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    # 輸出到標準輸出
    echo "[$timestamp] [$level] $message"
    
    # 同時寫入日誌文件
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

#安裝Docker與Docker-Compose
read -p "請輸入資料庫IP位址:" database_ipaddress
log "INFO" "寫入資料庫Config設定檔案"
echo $database_ipaddress > ./mysql_config/mysql_ip.conf
log "INFO" "安裝DoorSecurity System腳本開始執行"
cd docker-packget
sudo tar -xvf docker-27.5.1.tgz
sudo cp docker/* /usr/bin/
sudo cp docker.service /etc/systemd/system/
sudo chmod +x /etc/systemd/system/docker.service
sudo systemctl daemon-reload
docker_service_info=$(sudo systemctl status docker.service)
log "INFO" "$docker_service_info"
log "INFO" "檢查Docker是否正常啟動"
# 嘗試執行 docker 命令確認是否正常
if command -v docker --version &> /dev/null; then
    log "INFO" "Docker安裝成功"
    log "INFO" "開始安裝docker-compose engine"
    sudo cp docker-compose-linux-aarch64 /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    log "INFO" "檢查docker-compose 是否安裝成功"
    if command -v docker-compose &> /dev/null && docker-compose --version &> /dev/null; then
        log "INFO" "安裝完畢"
    else
        log "FAIL" "Docker-compose安裝失敗請檢查原因"
    fi
else
    log "FAIL" "Docker啟動失敗，詳情請見Error Log"
    exit
fi