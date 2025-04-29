介紹:
這裡是用來執行門禁控制器所需要的程式，程式部分組成分成兩部分
1.ControllerInput
2.ControllerOutput
![截圖 2025-04-29 下午3 46 20](https://github.com/user-attachments/assets/a1068e25-b23d-40e5-af49-71b8376d4d21)
首先先Git下來整個庫，在db_connect資料夾裡面存放的會是連接資料庫所使用的函式庫。
mysql_config的資料夾裡面有個mysql_ip.conf的檔案，這裡可以設定目前連接的mysql ip 為多少，請先將這裡修改成目前連線的mysql server ip address，如未修改會有報錯。
permition裡面存放的是wiegand目前用來模擬是否有權限的conf檔案，當如果有需要進行測試的時候可以去修改裡面的conf檔案，1代表有權限,0代表沒有權限。
一切都準備好後就可以在樹梅派上啟動ControllerInput與ControllerOutput裡面的python檔案。
ControllerInput所會用到的是Input點位的偵測，目前是測試用版本所以開啟後如果有修改門禁相關的資訊，預設是會每10秒去重新更新一次暫存的資料庫資訊，未來這邊會改用LocalDB來去進行所以目前暫時會以這種方式更新。
![截圖 2025-04-29 下午3 59 34](https://github.com/user-attachments/assets/956df45b-3fc8-4c38-b35a-db8dacc71df6)
再來有一個重要的部份是樹梅派的IP，我這邊取得樹梅派的IP是自動抓取網卡eth0的ipaddress如果使用的是wifi的話可以將我的function裡面的eth0改為wlan0，這樣就會是抓取wlan0的ipaddress了。
![截圖 2025-04-29 下午4 01 04](https://github.com/user-attachments/assets/ba8f4143-db05-4bba-83fc-525ac5aa2603)
以上是大概的說明。
