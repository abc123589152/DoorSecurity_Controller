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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-12  3:58:27
