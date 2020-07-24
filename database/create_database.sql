-- Hôte : db
-- Base de données : `myDb`

CREATE DATABASE myDb;
USE myDb;

CREATE TABLE `substitute` (
  `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `product_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `category` varchar(255) NOT NULL,
  `nutrition_grades` varchar(1) NOT NULL,
  `stores` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Structure de la table `aliment`
CREATE TABLE `aliment` (
  `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `product_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `category` varchar(255) NOT NULL,
  `nutrition_grades` varchar(255) NOT NULL,
  `stores` varchar(255) NOT NULL,
  `substitute_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Contraintes pour la table `aliment`
ALTER TABLE `aliment`
  ADD CONSTRAINT `substitute` FOREIGN KEY (`substitute_id`) REFERENCES `substitute` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;