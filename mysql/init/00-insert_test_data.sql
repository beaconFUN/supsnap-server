use flask;
-- MySQL dump 10.13  Distrib 8.0.2-dmr, for Linux (x86_64)
--
-- Host: localhost    Database: flask
-- ------------------------------------------------------
-- Server version	8.0.2-dmr

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `beacon`
--

DROP TABLE IF EXISTS `beacon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `beacon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(36) DEFAULT NULL,
  `major` int(11) DEFAULT NULL,
  `minor` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beacon`
--

LOCK TABLES `beacon` WRITE;
/*!40000 ALTER TABLE `beacon` DISABLE KEYS */;
INSERT INTO `beacon` VALUES (1,'4F215AA1-3904-47D5-AD5A-3B6AA89542AE',1,1),(2,'4F215AA1-3904-47D5-AD5A-3B6AA89542AE',1,2),(3,'4F215AA1-3904-47D5-AD5A-3B6AA89542AE',1,3),(4,'4F215AA1-3904-47D5-AD5A-3B6AA89542AE',2,1),(5,'4F215AA1-3904-47D5-AD5A-3B6AA89542AE',2,2),(6,'4F215AA1-3904-47D5-AD5A-3B6AA89542AE',2,3);
/*!40000 ALTER TABLE `beacon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `place`
--

DROP TABLE IF EXISTS `place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `place` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `beacon` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `beacon` (`beacon`),
  CONSTRAINT `place_ibfk_1` FOREIGN KEY (`beacon`) REFERENCES `beacon` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `place`
--

LOCK TABLES `place` WRITE;
/*!40000 ALTER TABLE `place` DISABLE KEYS */;
INSERT INTO `place` VALUES (1,'五稜郭-入り口',1),(2,'五稜郭-タワー売店',2),(3,'五稜郭-タワー展望台',3),(4,'赤レンガ倉庫-ホール',4),(5,'赤レンガ倉庫-ヒストリープラザ',5),(6,'赤レンガ倉庫-洋物館',6);
/*!40000 ALTER TABLE `place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `snap`
--

DROP TABLE IF EXISTS `snap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `snap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `src` varchar(255) DEFAULT NULL,
  `thum_src` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `snap`
--

LOCK TABLES `snap` WRITE;
/*!40000 ALTER TABLE `snap` DISABLE KEYS */;
INSERT INTO `snap` VALUES (1,'1.jpg','1_thum.jpg','2017-08-12 05:52:35'),(2,NULL,NULL,'2017-08-12 05:52:35');
/*!40000 ALTER TABLE `snap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visiter`
--

DROP TABLE IF EXISTS `visiter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `visiter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(255) DEFAULT NULL,
  `place` int(11) DEFAULT NULL,
  `pass_phrase` varchar(32) DEFAULT NULL,
  `snap` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `place` (`place`),
  KEY `snap` (`snap`),
  CONSTRAINT `visiter_ibfk_1` FOREIGN KEY (`place`) REFERENCES `place` (`id`),
  CONSTRAINT `visiter_ibfk_2` FOREIGN KEY (`snap`) REFERENCES `snap` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visiter`
--

LOCK TABLES `visiter` WRITE;
/*!40000 ALTER TABLE `visiter` DISABLE KEYS */;
INSERT INTO `visiter` VALUES (1,'user1',1,'f2315ced14ba0b55fe01c8c03fcc8e2e',1,'2017-08-12 05:52:35'),(2,'user2',1,'19f3b78b6bf5b548d0eb0147546b4244',1,'2017-08-12 05:52:35'),(3,'user1',1,'e49caacbe250f53d3775a1ada45965a7',2,'2017-08-12 05:52:35'),(4,'user2',1,'275b92992182d671a4d8146e1b3ad7c1',2,'2017-08-12 05:52:35');
/*!40000 ALTER TABLE `visiter` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-12  5:55:02
