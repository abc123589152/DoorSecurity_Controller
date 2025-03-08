-- MySQL dump 10.13  Distrib 9.1.0, for Linux (aarch64)
--
-- Host: localhost    Database: DoorSecurity
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `permitionGroup` varchar(45) DEFAULT NULL,
  `userPassword` text,
  `remark` varchar(45) DEFAULT NULL,
  `creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'root','admin','$2b$12$1DOwbobZzZhHtOgL9flb3uPvLdfZHf/Inr7G9leX9cyv0hTpMc3NG','系統管理員','2024-09-23 16:18:55','2024-09-29 14:29:06'),(2,'customer','customer','$2b$12$c9fvZ1f6SaVa7q/O4UBK4eiTwTc.X2kMDTVKqwcnNZwJcYCWv4wb2','來賓帳號','2024-09-29 10:28:33','2024-09-30 11:27:39'),(6,'stsb1','admin','$2b$12$3JWACmM3c0OsaMZujsE6JezGUI21MDdY8TKdshlxh7suRSYiwtwn.','系統管理員_stsb1_測試修改','2024-09-29 10:51:41','2024-10-01 09:50:53'),(7,'stsb2','admin','$2b$12$82XDUIfYaW4LPYfcHc8CZ.S/PW0mwV/5OJgxDJ0KKyrsLB6JKOVNC','系統管理員_stsb2','2024-09-29 10:52:17','2024-09-29 14:31:34'),(10,'test','admin','$2b$12$Yu89KHO/WWrQ5ObOTe4.3evX9anK8.2AOw.1BXEW62kS7UtH6kid.','測試用','2024-10-04 14:53:03',NULL);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `checkGpioOutput`
--

DROP TABLE IF EXISTS `checkGpioOutput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `checkGpioOutput` (
  `id` int NOT NULL AUTO_INCREMENT,
  `control` varchar(45) DEFAULT NULL,
  `wiegand` varchar(45) DEFAULT NULL,
  `gpioOutputPort` varchar(45) DEFAULT NULL,
  `eventActionStatus` varchar(45) DEFAULT NULL,
  `Creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `checkGpioOutput`
--

LOCK TABLES `checkGpioOutput` WRITE;
/*!40000 ALTER TABLE `checkGpioOutput` DISABLE KEYS */;
INSERT INTO `checkGpioOutput` VALUES (1,'172.16.1.186','uart2','18','InUse','2024-08-16 00:00:00',NULL),(2,'172.16.1.186','uart4','25','InUse','2024-08-16 00:00:00',NULL);
/*!40000 ALTER TABLE `checkGpioOutput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controllerInput`
--

DROP TABLE IF EXISTS `controllerInput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `controllerInput` (
  `id` int NOT NULL AUTO_INCREMENT,
  `controller` varchar(45) DEFAULT NULL,
  `inputType` varchar(45) DEFAULT NULL,
  `inputName` varchar(45) DEFAULT NULL,
  `inputPort` varchar(45) DEFAULT NULL,
  `inputStat` varchar(45) DEFAULT NULL,
  `remark` varchar(45) DEFAULT NULL,
  `creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controllerInput`
--

LOCK TABLES `controllerInput` WRITE;
/*!40000 ALTER TABLE `controllerInput` DISABLE KEYS */;
INSERT INTO `controllerInput` VALUES (1,'172.16.1.181','Input_Terminal','Input2','2','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(2,'172.16.1.181','Doorrelease_button','D534_Button','3','inactive','D534開門按鈕','2024-12-01 17:54:26','2025-02-07 11:32:29'),(3,'172.16.1.181','Doorrelease_button','Input4','4','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(4,'172.16.1.181','Input_Terminal','Input5','5','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(5,'172.16.1.181','Doorrelease_button','Input6','6','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(6,'172.16.1.181','Reedswitch_Terminal','Input7','7','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(7,'172.16.1.181','Reedswitch_Terminal','Input8','8','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(8,'172.16.1.181','Reedswitch_Terminal','Input9','9','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(9,'172.16.1.181','Reedswitch_Terminal','Input10','10','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(10,'172.16.1.181','Reedswitch_Terminal','Input11','11','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(11,'172.16.1.181','Input_Terminal','Input12','12','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(12,'172.16.1.181','Input_Terminal','Input13','13','inactive','None','2024-12-01 17:54:26','2025-02-07 11:32:29'),(35,'172.16.1.195','Reedswitch_Terminal','Input2','2','inactive','D702_磁磺接點','2025-02-05 17:50:47','2025-02-23 08:33:09'),(36,'172.16.1.195','Doorrelease_button','Input3','3','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(37,'172.16.1.195','Reedswitch_Terminal','Input4','4','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(38,'172.16.1.195','Reedswitch_Terminal','Input5','5','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(39,'172.16.1.195','Reedswitch_Terminal','Input6','6','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(40,'172.16.1.195','Doorrelease_button','Input7','7','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(41,'172.16.1.195','Doorrelease_button','Input8','8','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(42,'172.16.1.195','Input_Terminal','Input9','9','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(43,'172.16.1.195','Input_Terminal','Input10','10','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(44,'172.16.1.195','Input_Terminal','Input11','11','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(45,'172.16.1.195','Input_Terminal','Input12','12','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09');
/*!40000 ALTER TABLE `controllerInput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controllerOutput`
--

DROP TABLE IF EXISTS `controllerOutput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `controllerOutput` (
  `id` int NOT NULL AUTO_INCREMENT,
  `controller` varchar(45) DEFAULT NULL,
  `outputType` varchar(45) DEFAULT NULL,
  `outputName` varchar(45) DEFAULT NULL,
  `outputPort` varchar(45) DEFAULT NULL,
  `outputStat` varchar(45) DEFAULT NULL,
  `remark` varchar(45) DEFAULT NULL,
  `creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=178 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controllerOutput`
--

LOCK TABLES `controllerOutput` WRITE;
/*!40000 ALTER TABLE `controllerOutput` DISABLE KEYS */;
INSERT INTO `controllerOutput` VALUES (133,'172.16.1.181','Magneticlock_Terminal','Output14s','14','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:48'),(134,'172.16.1.181','Speaker_Terminal','D701_BZ','15','inactive','D534門禁喇叭','2024-12-01 17:54:26','2025-02-12 08:43:47'),(135,'172.16.1.181','Speaker_Terminal','D535_BZ','16','inactive','D535門禁喇叭','2024-12-01 17:54:26','2025-01-24 17:39:48'),(136,'172.16.1.181','Magneticlock_Terminal','Output19','19','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:48'),(137,'172.16.1.181','Speaker_Terminal','Output20','20','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:48'),(138,'172.16.1.181','Speaker_Terminal','Output21_181','21','inactive','','2024-12-01 17:54:26','2025-02-15 16:47:14'),(139,'172.16.1.181','Speaker_Terminal','Output22','22','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:49'),(140,'172.16.1.181','Speaker_Terminal','Output23','23','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:49'),(141,'172.16.1.181','Output_Terminal','Output24','24','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:49'),(142,'172.16.1.181','Output_Terminal','Output25','25','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:49'),(143,'172.16.1.181','Output_Terminal','Output26','26','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:49'),(144,'172.16.1.181','Output_Terminal','Output27','27','inactive','','2024-12-01 17:54:26','2025-01-24 17:39:49'),(167,'172.16.1.195','Speaker_Terminal','Output13','13','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(168,'172.16.1.195','Magneticlock_Terminal','Output14','14','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(169,'172.16.1.195','Output_Terminal','D892_BZ','15','inactive','D892 喇叭點位','2025-02-05 17:50:47','2025-02-23 08:33:09'),(170,'172.16.1.195','Output_Terminal','D892_BZ2','16','inactive','D892 第二組喇叭點位','2025-02-05 17:50:47','2025-02-23 08:33:09'),(171,'172.16.1.195','Magneticlock_Terminal','Output19','19','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(172,'172.16.1.195','Speaker_Terminal','Output20','20','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(173,'172.16.1.195','Magneticlock_Terminal','Output21','21','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(174,'172.16.1.195','Magneticlock_Terminal','Output24','24','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(175,'172.16.1.195','Output_Terminal','Output25','25','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(176,'172.16.1.195','Output_Terminal','Output26','26','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09'),(177,'172.16.1.195','Output_Terminal','Output27','27','inactive','None','2025-02-05 17:50:47','2025-02-23 08:33:09');
/*!40000 ALTER TABLE `controllerOutput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `door_status`
--

DROP TABLE IF EXISTS `door_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `door_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `doorname` varchar(255) DEFAULT NULL,
  `doorstatus` varchar(45) DEFAULT NULL,
  `quickOpen` varchar(45) DEFAULT NULL,
  `keepDoorOpen` varchar(45) DEFAULT NULL,
  `checkDoorPermition` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `door_status`
--

LOCK TABLES `door_status` WRITE;
/*!40000 ALTER TABLE `door_status` DISABLE KEYS */;
INSERT INTO `door_status` VALUES (25,'D701','close','0','0',NULL),(26,'D566','close','0','0',NULL),(28,'D892','close','0','0',NULL),(35,'D378','close','0','0',NULL);
/*!40000 ALTER TABLE `door_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doorControl`
--

DROP TABLE IF EXISTS `doorControl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doorControl` (
  `id` int NOT NULL AUTO_INCREMENT,
  `controlip` varchar(45) NOT NULL,
  `device_type` varchar(255) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `modification_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doorControl`
--

LOCK TABLES `doorControl` WRITE;
/*!40000 ALTER TABLE `doorControl` DISABLE KEYS */;
INSERT INTO `doorControl` VALUES (1,'192.168.1.186',NULL,'test','在中央走到旁機櫃','2024-07-15 02:24:04','2024-07-15 02:24:04'),(2,'192.168.1.187',NULL,'未知','中央走道','2024-07-15 02:30:46','2024-07-16 02:30:46');
/*!40000 ALTER TABLE `doorControl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doorgroup`
--

DROP TABLE IF EXISTS `doorgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doorgroup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `groupname` mediumtext NOT NULL,
  `doorname` varchar(45) NOT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `creation_time` varchar(255) DEFAULT NULL,
  `modification_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doorgroup`
--

LOCK TABLES `doorgroup` WRITE;
/*!40000 ALTER TABLE `doorgroup` DISABLE KEYS */;
INSERT INTO `doorgroup` VALUES (20,'40005','D701,D566,D892,D378','','2024-07-24 12:34:28','2025-03-08 14:17:00');
/*!40000 ALTER TABLE `doorgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doorsetting`
--

DROP TABLE IF EXISTS `doorsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doorsetting` (
  `id` int NOT NULL AUTO_INCREMENT,
  `control` varchar(45) DEFAULT NULL,
  `wiegand` varchar(45) DEFAULT NULL,
  `fingerprint_mode` varchar(45) DEFAULT NULL,
  `door` varchar(45) DEFAULT NULL,
  `door_sensor` varchar(45) DEFAULT NULL,
  `door_lock` varchar(45) DEFAULT NULL,
  `doorRelease_button` varchar(45) DEFAULT NULL,
  `reset_time` varchar(45) DEFAULT NULL,
  `openTimeLimit` varchar(45) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `creation_time` varchar(255) DEFAULT NULL,
  `modification_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doorsetting`
--

LOCK TABLES `doorsetting` WRITE;
/*!40000 ALTER TABLE `doorsetting` DISABLE KEYS */;
INSERT INTO `doorsetting` VALUES (54,'172.16.1.181','Wiegand1','disable','D701','8','19','4','5','15','D701_188第二個測試門禁','2025-02-03 17:01:07','2025-02-06 14:17:22'),(55,'172.16.1.181','Wiegand2','disable','D566','9','14','6','5','15','test','2025-02-07 11:37:19',NULL),(57,'172.16.1.195','Wiegand2','enable','D892','4','14','3','10','180','用來作測試可不可以同步','2025-02-08 14:26:46','2025-02-22 22:29:15'),(64,'172.16.1.195','Wiegand1','enable','D378','5','21','8','5','15','機房大門','2025-02-23 10:59:58',NULL);
/*!40000 ALTER TABLE `doorsetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employ`
--

DROP TABLE IF EXISTS `employ`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employ` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `cardnumber` varchar(45) NOT NULL,
  `doorgroup` mediumtext,
  `status` varchar(45) NOT NULL,
  `activation` varchar(100) NOT NULL,
  `expiration` varchar(100) NOT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `creation_time` varchar(100) NOT NULL,
  `modification_time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employ`
--

LOCK TABLES `employ` WRITE;
/*!40000 ALTER TABLE `employ` DISABLE KEYS */;
INSERT INTO `employ` VALUES (8,'楊扶恩','2291941972','40005','啟用','2024-07-17T00:00','2031-07-08T00:00',NULL,'2024-07-23 02:30:08','2024-12-22 13:11:59'),(10,'測試用卡片','289002787','40005','啟用','2024-07-17 00:00:00','2031-07-18 00:00:00','測試用','2024-07-24 13:12:57','2024-08-08 09:34:46'),(12,'PN532_測試用號碼','8466156136','40005','啟用','2024-07-17 00:00:00','2031-07-08 00:00:00','公司測試用','2024-08-01 14:30:10',NULL),(13,'王大明','17923167250','40005','啟用','2024-07-17 00:00:00','2031-07-08 00:00:00','測試用','2024-10-04 22:05:48',NULL);
/*!40000 ALTER TABLE `employ` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventAction`
--

DROP TABLE IF EXISTS `eventAction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventAction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `eventName` varchar(45) NOT NULL,
  `doorName` text,
  `eventClass` varchar(45) DEFAULT NULL,
  `outputPort` varchar(45) DEFAULT NULL,
  `remark` varchar(45) DEFAULT NULL,
  `eventStat` varchar(45) DEFAULT NULL,
  `creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventAction`
--

LOCK TABLES `eventAction` WRITE;
/*!40000 ALTER TABLE `eventAction` DISABLE KEYS */;
INSERT INTO `eventAction` VALUES (1,'門鎖隔離','D787,D532,D706','DoorOpen','','測試用事件','inactive','2024-08-11 13:00:00','2024-10-20 13:20:58'),(7,'P1 化學房門禁鎖隔離','D706','DoorOpen',NULL,'','inactive','2024-08-16 10:48:19','2024-09-02 16:31:03'),(8,'D867_隔離開門','D867','DoorOpen',NULL,'D867 新建立的測試隔離開門','inactive','2024-08-24 18:27:04',NULL),(18,'D701_強迫開門','D701','ForceOpen','D701_BZ,D535_BZ','D701發生強迫開門時會進行觸發','inactive','2025-02-12 08:44:04','2025-02-14 08:45:17'),(19,'D892_強迫開門','D892','ForceOpen','D892_BZ,D892_BZ2','D892兩的喇叭點位的測試','inactive','2025-02-14 09:05:34','2025-02-15 16:53:11');
/*!40000 ALTER TABLE `eventAction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventLog`
--

DROP TABLE IF EXISTS `eventLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventLog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `eventName` varchar(45) DEFAULT NULL,
  `eventClass` varchar(45) DEFAULT NULL,
  `eventCause` text,
  `timeToEvent` varchar(45) DEFAULT NULL,
  `remark` text,
  `eventStatus` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventLog`
--

LOCK TABLES `eventLog` WRITE;
/*!40000 ALTER TABLE `eventLog` DISABLE KEYS */;
INSERT INTO `eventLog` VALUES (53,'D532_開門過久','HaltOpen','systemAction','2024-09-22 22:36:48','測試用開門過久','confirmed'),(54,'D532_開門過久','HaltOpen','systemAction','2024-10-04 22:08:48','測試用','confirmed'),(55,'D532_開門過久','HaltOpen','systemAction','2024-10-04 22:22:04','None','confirmed'),(56,'門鎖隔離','DoorOpen','Manual','2024-10-11 15:14:05','手動觸發','confirmed'),(57,'TEST','ForceOpen','systemAction','2024-10-21 02:54:49','None','confirmed'),(58,'TEST','ForceOpen','systemAction','2024-10-22 23:09:32','None','confirmed'),(59,'TEST','ForceOpen','systemAction','2024-10-22 23:47:51','None','confirmed'),(60,'TEST','ForceOpen','systemAction','2024-10-23 00:40:08','None','confirmed'),(61,'TEST','ForceOpen','systemAction','2024-10-23 00:58:55','None','confirmed'),(62,'TEST','ForceOpen','systemAction','2024-10-24 00:20:02','None','confirmed'),(63,'TEST','ForceOpen','systemAction','2024-10-24 01:25:29','None','confirmed'),(64,'D787_強迫開門','ForceOpen','systemAction','2024-10-24 01:27:14','已確認沒有問題','confirmed'),(65,'D787_強迫開門','ForceOpen','systemAction','2024-10-24 22:40:03','已確認事測試','confirmed'),(66,'D787_強迫開門','ForceOpen','systemAction','2024-10-24 22:59:45','已確認事測試','confirmed'),(67,'D787_強迫開門','ForceOpen','systemAction','2024-11-04 14:31:43','正在進行測試可以不用理會','confirmed'),(77,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 15:59:57','TEST','confirmed'),(78,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:00:00','TEST2','confirmed'),(79,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:00:03','asdasd','confirmed'),(80,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:00:07','sdsadd','confirmed'),(81,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:00:10','123123123','confirmed'),(82,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:00:13','測試用','confirmed'),(83,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:00:17','None','confirmed'),(84,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:40:11','dsadsdsdsd','confirmed'),(85,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:40:52','asdsadasd','confirmed'),(86,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:45:28','assadds','confirmed'),(87,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 16:46:29','None','confirmed'),(88,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:27:22','None','confirmed'),(89,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:27:24','None','confirmed'),(90,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:27:26','None','confirmed'),(91,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:27:28','None','confirmed'),(92,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:27:30','None','confirmed'),(93,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:27:32','sdadasdas','confirmed'),(94,'D892_強迫開門','ForceOpen','systemAction','2025-02-19 21:44:52','已確認是測試','confirmed'),(96,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:14:52','手動觸發','confirmed'),(97,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:15:53','手動觸發','confirmed'),(98,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:20:47','手動觸發','confirmed'),(99,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:23:19','手動觸發','confirmed'),(100,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:25:01','手動觸發','confirmed'),(101,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:30:49','手動觸發','confirmed'),(102,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:33:43','手動觸發','confirmed'),(103,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:42:14','手動觸發','confirmed'),(104,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:49:11','手動觸發','confirmed'),(105,'D892_強迫開門','ForceOpen','Manual','2025-02-20 10:49:26','手動觸發','confirmed'),(106,'D892_強迫開門','ForceOpen','Manual','2025-02-20 11:12:41','手動觸發','confirmed'),(107,'D892_強迫開門','ForceOpen','Manual','2025-02-20 11:22:45','手動觸發','confirmed'),(108,'D892_強迫開門','ForceOpen','Manual','2025-02-20 11:45:41','手動觸發','confirmed'),(109,'D892_強迫開門','ForceOpen','Manual','2025-02-20 11:47:02','手動觸發','confirmed'),(110,'D892_強迫開門','ForceOpen','Manual','2025-02-20 11:49:55','手動觸發','confirmed'),(111,'D892_強迫開門','ForceOpen','Manual','2025-02-20 11:51:57','手動觸發','confirmed'),(112,'D892_強迫開門','ForceOpen','Manual','2025-02-20 13:54:49','手動觸發','confirmed'),(113,'D892_強迫開門','ForceOpen','Manual','2025-02-20 14:19:14','手動觸發','confirmed'),(114,'D892_強迫開門','ForceOpen','Manual','2025-02-20 15:42:57','手動觸發','confirmed'),(115,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:22:49',NULL,'unconfirmed'),(116,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:22:52',NULL,'unconfirmed'),(117,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:22:55',NULL,'unconfirmed'),(118,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:22:58',NULL,'unconfirmed'),(119,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:23:01',NULL,'unconfirmed'),(120,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:23:07',NULL,'unconfirmed'),(121,'D892_強迫開門','ForceOpen','systemAction','2025-02-21 15:23:12',NULL,'unconfirmed'),(122,'D892_強迫開門','ForceOpen','systemAction','2025-02-22 03:12:06',NULL,'unconfirmed'),(123,'D892_強迫開門','ForceOpen','systemAction','2025-02-22 03:12:17','測試用','confirmed');
/*!40000 ALTER TABLE `eventLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mainController`
--

DROP TABLE IF EXISTS `mainController`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mainController` (
  `id` int NOT NULL AUTO_INCREMENT,
  `IP` varchar(45) DEFAULT NULL,
  `controllerName` varchar(45) DEFAULT NULL,
  `device_type` varchar(45) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `connectionStatus` varchar(45) DEFAULT NULL,
  `outputName` varchar(45) DEFAULT NULL,
  `outputPort` varchar(45) DEFAULT NULL,
  `outputRemark` varchar(45) DEFAULT NULL,
  `creation_time` varchar(255) DEFAULT NULL,
  `modification_time` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mainController`
--

LOCK TABLES `mainController` WRITE;
/*!40000 ALTER TABLE `mainController` DISABLE KEYS */;
INSERT INTO `mainController` VALUES (24,'172.16.1.181','Zero_test_controller','raspberry_pi_zero_2w','Test with raspberry pi zero','failed',NULL,NULL,NULL,'2024-12-01 17:54:26','2025-02-09 14:59:56'),(29,'172.16.1.195','測試用控制器195','raspberry_pi_3b','test','normal',NULL,NULL,NULL,'2025-02-05 17:50:47','2025-02-23 08:33:09');
/*!40000 ALTER TABLE `mainController` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outPutPort`
--

DROP TABLE IF EXISTS `outPutPort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `outPutPort` (
  `id` int NOT NULL AUTO_INCREMENT,
  `control` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `outPutNumber` varchar(45) DEFAULT NULL,
  `outPutName` varchar(45) DEFAULT NULL,
  `outPutStat` varchar(45) DEFAULT NULL,
  `creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outPutPort`
--

LOCK TABLES `outPutPort` WRITE;
/*!40000 ALTER TABLE `outPutPort` DISABLE KEYS */;
/*!40000 ALTER TABLE `outPutPort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permitionGroup`
--

DROP TABLE IF EXISTS `permitionGroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permitionGroup` (
  `id` int NOT NULL AUTO_INCREMENT,
  `groupName` varchar(45) DEFAULT NULL,
  `swipeCardLog` varchar(45) DEFAULT NULL,
  `doorsetting` varchar(45) DEFAULT NULL,
  `doorgroup` varchar(45) DEFAULT NULL,
  `door_status` varchar(45) DEFAULT NULL,
  `employ` varchar(45) DEFAULT NULL,
  `eventAction` varchar(45) DEFAULT NULL,
  `eventLog` varchar(45) DEFAULT NULL,
  `mainController` varchar(45) DEFAULT NULL,
  `controllerInput` varchar(45) DEFAULT NULL,
  `controllerOutput` varchar(45) DEFAULT NULL,
  `account` varchar(45) DEFAULT NULL,
  `permitionGroup` varchar(45) DEFAULT NULL,
  `remark` varchar(45) DEFAULT NULL,
  `creation_time` varchar(45) DEFAULT NULL,
  `modification_time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permitionGroup`
--

LOCK TABLES `permitionGroup` WRITE;
/*!40000 ALTER TABLE `permitionGroup` DISABLE KEYS */;
INSERT INTO `permitionGroup` VALUES (10,'admin','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','Read/Write','系統管理群組','2024-09-27 16:00:30','2025-01-23 10:54:25'),(14,'customer','None','Read','None','None','None','None','Read','None','None','None','None','None','','2024-09-29 13:24:37','2025-01-23 14:15:03'),(15,'一般權限','Read','None','None','None','None','None','Read','None',NULL,'None','Read','Read/Write','測試用一般權限','2024-09-29 13:24:54','2024-09-30 13:58:46');
/*!40000 ALTER TABLE `permitionGroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `swipeCardLog`
--

DROP TABLE IF EXISTS `swipeCardLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `swipeCardLog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `cardnumber` varchar(45) DEFAULT NULL,
  `doorname` varchar(45) DEFAULT NULL,
  `doorstatus` varchar(45) DEFAULT NULL,
  `authorization` varchar(45) DEFAULT NULL,
  `swipetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=656 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `swipeCardLog`
--

LOCK TABLES `swipeCardLog` WRITE;
/*!40000 ALTER TABLE `swipeCardLog` DISABLE KEYS */;
INSERT INTO `swipeCardLog` VALUES (1,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 13:49:54'),(2,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 13:50:16'),(3,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 13:50:30'),(4,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 13:50:47'),(5,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 13:50:51'),(6,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 13:51:52'),(7,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 13:51:56'),(8,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 13:52:00'),(9,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 14:22:10'),(10,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 14:22:15'),(11,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 14:22:22'),(12,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 14:22:27'),(13,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 14:22:31'),(14,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 14:22:33'),(15,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 14:22:35'),(16,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 14:22:37'),(17,'測試卡號2','8466156136','D532','測試用門禁','Pemit','2024-07-26 14:22:38'),(18,'Unknown Card','671158927','D532','測試用門禁','deny','2024-07-26 14:22:40'),(19,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 10:50:55'),(20,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 10:55:37'),(21,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 10:57:30'),(22,'測試用卡片','289002787','D532','測試用門禁','deny','2024-07-28 11:12:21'),(23,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 11:58:27'),(24,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 11:58:56'),(25,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 11:59:06'),(26,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 11:59:21'),(27,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 14:17:55'),(28,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 14:19:06'),(29,'楊扶恩','2291941972','D532','測試用門禁','Permit','2024-07-28 14:46:18'),(30,'測試用卡片','289002787','D532','測試用門禁','deny','2024-07-28 14:47:17'),(31,'Unknown Card','8466156136','D532','測試用門禁','deny','2024-07-31 06:26:24'),(32,'Unknown Card','8466156136','D532','測試用門禁','deny','2024-07-31 06:26:32'),(33,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:27:19'),(34,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:27:55'),(35,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:39:36'),(36,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:44:30'),(37,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:47:15'),(38,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:59:15'),(39,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 06:59:40'),(40,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 07:05:49'),(41,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 07:06:18'),(42,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 07:07:39'),(43,'PN532_測試用號碼','8466156136','D532','測試用門禁','Permit','2024-07-31 07:07:54'),(44,'PN532_測試用號碼','8466156136','D532','有權限的測試大門','deny','2024-07-31 07:54:32'),(45,'PN532_測試用號碼','8466156136','D532','有權限的測試大門','Permit','2024-07-31 07:55:07'),(46,'Unknown Card','','D532','有權限的測試大門','deny','2024-07-31 08:06:24'),(47,'Unknown Card','','D532','有權限的測試大門','deny','2024-07-31 08:06:36'),(48,'PN532_測試用號碼','8466156136','D532','有權限的測試大門','Permit','2024-07-31 09:14:39'),(49,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 10:10:47'),(50,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 10:30:59'),(51,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 10:33:44'),(52,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 10:35:58'),(53,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 10:50:38'),(54,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:00:13'),(55,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:11:53'),(56,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:12:00'),(57,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:14:19'),(58,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:15:25'),(59,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:19:41'),(60,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:19:48'),(61,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:19:49'),(62,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:19:51'),(63,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:20:32'),(64,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:20:37'),(65,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:25:34'),(66,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:26:13'),(67,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:26:56'),(68,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:27:04'),(69,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:27:56'),(70,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:28:02'),(71,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:29:27'),(72,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:29:55'),(73,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:30:42'),(74,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:31:27'),(75,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:32:23'),(76,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:32:39'),(77,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:33:28'),(78,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:33:35'),(79,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:33:51'),(80,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:34:17'),(81,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:34:44'),(82,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:35:41'),(83,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:36:31'),(84,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:37:12'),(85,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:39:16'),(86,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:39:59'),(87,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:40:26'),(88,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:42:41'),(89,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:46:28'),(90,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:47:20'),(91,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:48:12'),(92,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:48:21'),(93,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:49:59'),(94,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:50:54'),(95,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:52:16'),(96,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:52:24'),(97,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:52:31'),(98,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:53:29'),(99,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:54:37'),(100,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:55:19'),(101,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:55:58'),(102,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:57:48'),(103,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:58:49'),(104,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:59:15'),(105,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:59:26'),(106,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 11:59:51'),(107,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 12:00:00'),(108,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 12:01:26'),(109,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 12:01:34'),(110,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:30:16'),(111,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:31:13'),(112,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:31:23'),(113,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:34:09'),(114,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:34:28'),(115,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:42:12'),(116,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:42:19'),(117,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:43:57'),(118,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:43:59'),(119,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:02'),(120,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:03'),(121,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:05'),(122,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:14'),(123,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:17'),(124,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:18'),(125,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:44:20'),(126,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:45:06'),(127,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:45:08'),(128,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:45:12'),(129,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:45:20'),(130,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:50:52'),(131,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:51:37'),(132,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:51:38'),(133,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:51:40'),(134,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:51:42'),(135,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:51:43'),(136,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:52:21'),(137,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:54:12'),(138,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:55:40'),(139,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:55:49'),(140,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:55:51'),(141,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:55:52'),(142,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:55:54'),(143,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:56:32'),(144,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:56:35'),(145,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:56:37'),(146,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 13:56:53'),(147,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:26:23'),(148,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:26:32'),(149,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:26:33'),(150,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:26:35'),(151,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:26:37'),(152,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:27:13'),(153,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:27:15'),(154,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:27:17'),(155,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 14:27:20'),(156,'PN532_測試用號碼','8466156136','D656','Test door two','deny','2024-08-02 16:56:09'),(157,'PN532_測試用號碼','8466156136','D656','Test door two','deny','2024-08-02 16:56:17'),(158,'PN532_測試用號碼','8466156136','D702','測試用的門編號','Permit','2024-08-02 16:57:25'),(159,'PN532_測試用號碼','8466156136','D706','another door','deny','2024-08-02 16:58:20'),(160,'PN532_測試用號碼','8466156136','D706','another door','deny','2024-08-02 16:58:22'),(161,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-02 16:59:09'),(162,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','deny','2024-08-04 23:26:14'),(163,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','deny','2024-08-04 23:26:20'),(164,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','Permit','2024-08-04 23:26:44'),(165,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','Permit','2024-08-04 23:27:01'),(166,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','Permit','2024-08-04 23:29:26'),(167,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','Permit','2024-08-04 23:33:37'),(168,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','Permit','2024-08-04 23:34:26'),(169,'PN532_測試用號碼','8466156136','D656','測試第三道門禁','Permit','2024-08-04 23:36:10'),(170,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-08 05:42:09'),(171,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-08-16 14:16:10'),(172,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:17:21'),(173,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:17:37'),(174,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:20:09'),(175,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:28:28'),(176,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:28:38'),(177,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:28:47'),(178,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:28:50'),(179,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:35:42'),(180,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:35:49'),(181,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:35:58'),(182,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:36:54'),(183,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:37:03'),(184,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:37:15'),(185,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:37:23'),(186,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:38:48'),(187,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:39:16'),(188,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:39:22'),(189,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:39:24'),(190,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:39:27'),(191,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:40:14'),(192,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-16 14:47:30'),(193,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-18 16:54:15'),(194,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-18 16:54:26'),(195,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-18 16:54:49'),(196,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-18 17:00:27'),(197,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-18 17:00:47'),(198,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-18 17:03:16'),(199,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-19 23:59:03'),(200,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-19 23:59:19'),(201,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:01:16'),(202,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:02:52'),(203,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:03:11'),(204,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:03:22'),(205,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:03:26'),(206,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:03:29'),(207,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:04:20'),(208,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:04:39'),(209,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:14:53'),(210,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:16:15'),(211,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:19:20'),(212,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:19:55'),(213,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:20:13'),(214,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:20:35'),(215,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:22:41'),(216,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:23:02'),(217,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:23:49'),(218,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:24:30'),(219,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:27:05'),(220,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 00:27:18'),(221,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:16:15'),(222,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:16:42'),(223,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:17:02'),(224,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:26:55'),(225,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:28:43'),(226,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:33:17'),(227,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 01:33:39'),(228,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:06:44'),(229,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:08:25'),(230,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:09:00'),(231,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:10:02'),(232,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:10:44'),(233,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:11:46'),(234,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:11:55'),(235,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:12:16'),(236,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:13:27'),(237,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:13:44'),(238,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:15:50'),(239,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 14:22:45'),(240,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:12:55'),(241,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:13:11'),(242,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:13:48'),(243,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:14:21'),(244,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:15:02'),(245,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:15:50'),(246,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:16:30'),(247,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:17:28'),(248,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:17:50'),(249,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:18:01'),(250,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:18:23'),(251,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:18:43'),(252,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:19:07'),(253,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:21:32'),(254,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:22:16'),(255,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:22:25'),(256,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:25:15'),(257,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:25:26'),(258,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:25:52'),(259,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:27:49'),(260,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:29:01'),(261,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:29:51'),(262,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:31:34'),(263,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:31:54'),(264,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:33:58'),(265,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:37:32'),(266,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:37:51'),(267,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 15:41:56'),(268,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:26:30'),(269,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:27:29'),(270,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:27:38'),(271,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:29:19'),(272,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:29:40'),(273,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:31:49'),(274,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:32:10'),(275,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:32:23'),(276,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:33:26'),(277,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:35:24'),(278,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-20 16:35:56'),(279,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 14:22:33'),(280,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 14:22:44'),(281,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 14:26:11'),(282,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 14:26:35'),(283,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-23 14:28:17'),(284,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-23 14:28:19'),(285,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-23 14:28:40'),(286,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:37:59'),(287,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:38:12'),(288,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:40:59'),(289,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:41:29'),(290,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:42:16'),(291,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:42:27'),(292,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 15:42:52'),(293,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 16:33:21'),(294,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-23 16:34:06'),(295,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:37:35'),(296,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:37:55'),(297,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:38:06'),(298,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:38:19'),(299,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:38:28'),(300,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:39:06'),(301,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:39:18'),(302,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:39:26'),(303,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:39:34'),(304,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:02'),(305,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:10'),(306,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:30'),(307,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:38'),(308,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:46'),(309,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:48'),(310,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:50'),(311,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:52'),(312,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:40:54'),(313,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:02'),(314,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:35'),(315,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:43'),(316,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:44'),(317,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:46'),(318,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:51'),(319,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:53'),(320,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:54'),(321,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:56'),(322,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:41:58'),(323,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:42:00'),(324,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:42:01'),(325,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:42:03'),(326,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:42:05'),(327,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:42:06'),(328,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:42:08'),(329,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:43:02'),(330,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:43:51'),(331,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:44:03'),(332,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:44:29'),(333,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:44:49'),(334,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:44:59'),(335,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:45:07'),(336,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:45:29'),(337,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:45:39'),(338,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:50:58'),(339,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:51:16'),(340,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:52:06'),(341,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:53:08'),(342,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:53:28'),(343,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:53:57'),(344,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:54:57'),(345,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:56:43'),(346,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:56:46'),(347,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 09:57:02'),(348,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:11:04'),(349,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:26:36'),(350,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:26:45'),(351,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:27:16'),(352,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:37:21'),(353,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:38:02'),(354,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:38:14'),(355,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:38:28'),(356,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:38:40'),(357,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 10:55:16'),(358,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:08:24'),(359,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:08:30'),(360,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:08:37'),(361,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:08:44'),(362,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:08:50'),(363,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:22:50'),(364,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:24:11'),(365,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-25 11:24:29'),(366,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-08-25 18:10:55'),(367,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:44:21'),(368,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:45:14'),(369,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:45:27'),(370,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:55:45'),(371,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:56:05'),(372,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:57:46'),(373,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:57:56'),(374,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 15:58:10'),(375,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 16:40:40'),(376,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 16:41:26'),(377,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:19:27'),(378,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:19:37'),(379,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:20:44'),(380,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:20:57'),(381,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:21:24'),(382,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:21:33'),(383,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:22:26'),(384,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:22:35'),(385,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:22:51'),(386,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:22:59'),(387,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:06'),(388,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:21'),(389,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:22'),(390,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:24'),(391,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:26'),(392,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:27'),(393,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 17:28:28'),(394,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:18:50'),(395,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:39:23'),(396,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:42:24'),(397,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:35'),(398,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:44'),(399,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:45'),(400,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:47'),(401,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:49'),(402,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:50'),(403,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:43:51'),(404,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-26 18:48:00'),(405,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-27 15:30:27'),(406,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-27 15:31:48'),(407,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-27 15:32:18'),(408,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-27 15:37:00'),(409,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-27 15:37:13'),(410,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-27 15:42:38'),(411,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-27 15:43:59'),(412,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-27 15:44:16'),(413,'Unknown Card','\0','D532','測試用多一個門禁','deny','2024-08-27 15:48:43'),(414,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-08-27 15:54:22'),(415,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-27 16:03:09'),(416,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-08-27 16:03:30'),(417,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','deny','2024-08-27 16:04:11'),(418,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-08-27 16:06:52'),(419,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-08-27 16:07:15'),(420,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-08-27 16:12:55'),(421,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','deny','2024-08-27 16:13:16'),(422,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-08-27 16:13:26'),(423,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','deny','2024-08-27 16:13:36'),(424,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 02:04:38'),(425,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 02:07:37'),(426,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 02:07:46'),(427,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 02:08:35'),(428,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 02:08:47'),(429,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 02:30:18'),(430,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-09-02 02:33:32'),(431,'PN532_測試用號碼','8466156136','D706','another door','Permit','2024-09-02 02:40:25'),(432,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-09-02 07:42:34'),(433,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','deny','2024-09-02 07:44:29'),(434,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-02 07:44:47'),(435,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-02 07:44:56'),(436,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-02 07:45:10'),(437,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 07:58:15'),(438,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:02:16'),(439,'Unknown Card','\0\0','D867','測試用第二個門禁','deny','2024-09-02 08:11:57'),(440,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-09-02 08:12:04'),(441,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-02 08:12:31'),(442,'Unknown Card','\0\0\0','D532','測試用多一個門禁','deny','2024-09-02 08:13:16'),(443,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:13:27'),(444,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:38:14'),(445,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:38:43'),(446,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:39:01'),(447,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-09-02 08:39:49'),(448,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-09-02 08:39:56'),(449,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:40:09'),(450,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:40:23'),(451,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:40:41'),(452,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:41:12'),(453,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:41:20'),(454,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-09-02 08:41:43'),(455,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 08:41:51'),(456,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-09-02 08:42:04'),(457,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-09-02 09:01:16'),(458,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 09:02:03'),(459,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 09:02:11'),(460,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-02 09:02:18'),(461,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 19:12:48'),(462,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 19:14:26'),(463,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:45:14'),(464,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:46:04'),(465,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:46:37'),(466,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:50:39'),(467,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:51:23'),(468,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:52:28'),(469,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:53:06'),(470,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:53:59'),(471,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:54:59'),(472,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:57:12'),(473,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:57:21'),(474,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 21:58:02'),(475,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:04:22'),(476,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:04:29'),(477,'Unknown Card','\0','D867','測試用第二個門禁','deny','2024-09-03 22:10:10'),(478,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:12:04'),(479,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:13:58'),(480,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:14:01'),(481,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:14:03'),(482,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:17:38'),(483,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:17:49'),(484,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:17:51'),(485,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:22:21'),(486,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:22:31'),(487,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:22:32'),(488,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:22:34'),(489,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:23:25'),(490,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:37:32'),(491,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:38:52'),(492,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:39:01'),(493,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:39:04'),(494,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:39:27'),(495,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:42:05'),(496,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:42:08'),(497,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:43:17'),(498,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:43:25'),(499,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 22:43:33'),(500,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 22:43:36'),(501,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:01:32'),(502,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:01:44'),(503,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:01:54'),(504,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:01:58'),(505,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:02:38'),(506,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:02:47'),(507,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:02:49'),(508,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:03:01'),(509,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:03:03'),(510,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:04:07'),(511,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:04:09'),(512,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:05:03'),(513,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:05:04'),(514,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:38:08'),(515,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:38:15'),(516,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:38:23'),(517,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:38:24'),(518,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:51:34'),(519,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:51:41'),(520,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:51:49'),(521,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:51:50'),(522,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:51:58'),(523,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:51:59'),(524,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:01'),(525,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:52:02'),(526,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:25'),(527,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:26'),(528,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:28'),(529,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:29'),(530,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:54'),(531,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:55'),(532,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:56'),(533,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:58'),(534,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:52:59'),(535,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:57:03'),(536,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:57:05'),(537,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:57:07'),(538,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:57:15'),(539,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:57:17'),(540,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:58:05'),(541,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:58:06'),(542,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:58:15'),(543,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:58:22'),(544,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:58:31'),(545,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:58:33'),(546,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:59:28'),(547,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:59:37'),(548,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-03 23:59:39'),(549,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-03 23:59:49'),(550,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:03:44'),(551,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:04:20'),(552,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:04:33'),(553,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:04:35'),(554,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:04:37'),(555,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:26:41'),(556,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:26:48'),(557,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:26:50'),(558,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 00:26:58'),(559,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 00:27:00'),(560,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:27:26'),(561,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 00:27:28'),(562,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:28:27'),(563,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 00:28:28'),(564,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:55:20'),(565,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:55:28'),(566,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 00:55:29'),(567,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:57:41'),(568,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:57:48'),(569,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 00:57:49'),(570,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 00:57:55'),(571,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 13:52:11'),(572,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-04 13:52:13'),(573,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 13:52:21'),(574,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 13:52:24'),(575,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-04 13:52:45'),(576,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:14:11'),(577,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:14:20'),(578,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:14:28'),(579,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:14:30'),(580,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:14:32'),(581,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:15:11'),(582,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:15:14'),(583,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:17:18'),(584,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-06 22:25:19'),(585,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:13:29'),(586,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:25:17'),(587,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:25:25'),(588,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:26:24'),(589,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:26:33'),(590,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:28:33'),(591,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:28:38'),(592,'Unknown Card','0\0\0\0\0\0','D532','測試用多一個門禁','deny','2024-09-11 16:31:35'),(593,'Unknown Card','\00\0\rHC\0','D532','測試用多一個門禁','deny','2024-09-11 16:31:54'),(594,'Unknown Card','\0\0\0\0\0','D532','測試用多一個門禁','deny','2024-09-11 16:32:28'),(595,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:34:11'),(596,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:34:26'),(597,'Unknown Card','0\0\0','D532','測試用多一個門禁','deny','2024-09-11 16:34:34'),(598,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:34:36'),(599,'Unknown Card','\0\0\0 \0\0','D532','測試用多一個門禁','deny','2024-09-11 16:34:38'),(600,'Unknown Card','846&05612&','D532','測試用多一個門禁','deny','2024-09-11 16:35:22'),(601,'Unknown Card','84661%&136','D532','測試用多一個門禁','deny','2024-09-11 16:35:27'),(602,'Unknown Card','84&&1%6136\r','D532','測試用多一個門禁','deny','2024-09-11 16:35:29'),(603,'Unknown Card','8466106136','D532','測試用多一個門禁','deny','2024-09-11 16:36:23'),(604,'Unknown Card','8464154126','D532','測試用多一個門禁','deny','2024-09-11 16:36:27'),(605,'Unknown Card','846615&134\r','D532','測試用多一個門禁','deny','2024-09-11 16:36:34'),(606,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:36:37'),(607,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:36:56'),(608,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:36:57'),(609,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:36:58'),(610,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:40:17'),(611,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:40:20'),(612,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:40:24'),(613,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:40:26'),(614,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:40:28'),(615,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:40:30'),(616,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:41:31'),(617,'PN532_測試用號碼','8466156136','D867','測試用第二個門禁','Permit','2024-09-11 16:41:35'),(618,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:41:51'),(619,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:41:53'),(620,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-11 16:41:55'),(621,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','deny','2024-09-22 21:46:26'),(622,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:46:54'),(623,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:52:39'),(624,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:55:02'),(625,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:55:21'),(626,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:56:34'),(627,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:57:27'),(628,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 21:59:50'),(629,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:00:58'),(630,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:01:22'),(631,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:01:50'),(632,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:03:16'),(633,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:21:23'),(634,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:26:08'),(635,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:30:37'),(636,'PN532_測試用號碼','8466156136','D532','測試用多一個門禁','Permit','2024-09-22 22:36:30'),(637,'王大明','17923167250','D532','測試用多一個門禁','Permit','2024-10-04 22:07:25'),(638,'王大明','17923167250','D532','測試用多一個門禁','Permit','2024-10-04 22:08:29'),(639,'王大明','17923167250','D532','測試用多一個門禁','Permit','2024-10-04 22:21:43'),(640,'Unknown Card','\0','D787','測試用多一個門禁','deny','2024-10-22 23:58:25'),(641,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:01:37'),(642,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:01:39'),(643,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:01:42'),(644,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:03:04'),(645,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:03:13'),(646,'Unknown Card','\0','D787','測試用多一個門禁','deny','2024-10-23 00:03:50'),(647,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:18:01'),(648,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:23:24'),(649,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:31:53'),(650,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:37:49'),(651,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:38:43'),(652,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:39:38'),(653,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:40:49'),(654,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 00:44:15'),(655,'PN532_測試用號碼','8466156136','D787','測試用多一個門禁','Permit','2024-10-23 01:00:31');
/*!40000 ALTER TABLE `swipeCardLog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-08  6:44:18
