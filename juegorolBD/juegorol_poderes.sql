-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: juegorol
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `poderes`
--

DROP TABLE IF EXISTS `poderes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `poderes` (
  `ID_Poder` int NOT NULL AUTO_INCREMENT,
  `Nombre_Poder` varchar(50) DEFAULT NULL,
  `Detalle` varchar(255) DEFAULT NULL,
  `Raza` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Poder`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `poderes`
--

LOCK TABLES `poderes` WRITE;
/*!40000 ALTER TABLE `poderes` DISABLE KEYS */;
INSERT INTO `poderes` VALUES (1,'Curación','Cura al objetivo','Hada'),(2,'Telequinesis','Mueve objetos con la mente','Humano'),(3,'Invisibilidad','Permite volverse invisible','Elfo'),(4,'Berserk','Aumenta tu daño por un tiempo','Orco'),(5,'Bola de Fuego','sasa','Humano'),(6,'Cono de Frio','Gener un con de hielo que congela al enemigo','Yeti'),(7,'Muro de Hielo','Se genera un gran y resistente muro de hielo','Yeti'),(11,'Manipulacion de la luz','Los elfos pueden controlar la luz y crear efectos luminosos deslumbrantes o cegadores.','Elfo'),(12,'Protección divina','Los ángeles pueden invocar un escudo divino que los protege de daños y los vuelve prácticamente invulnerables. Este escudo también puede extenderse a otros seres aliados cercanos, brindándoles protección contra ataques y fuerzas malignas.','Angel'),(13,'Manifestación de alas',' Los ángeles pueden desplegar sus majestuosas alas, permitiéndoles volar y moverse con gracia celestial. Estas alas también pueden ser utilizadas para crear ráfagas de viento y generar corrientes que repelen a los enemigos.','Angel'),(14,'Teletransportación','Los ángeles pueden desaparecer de un lugar y aparecer instantáneamente en otro. Pueden viajar largas distancias en un abrir y cerrar de ojos, permitiéndoles intervenir rápidamente en situaciones críticas.','Angel');
/*!40000 ALTER TABLE `poderes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-17 12:49:52
