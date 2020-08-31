--
-- Base de données : `myDb`
--
CREATE DATABASE IF NOT EXISTS `myDb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `myDb`;

CREATE TABLE `aliment` (
  `id` int NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `category` int DEFAULT NULL,
  `nutrition_grades` varchar(255) DEFAULT NULL,
  `stores` varchar(255) DEFAULT NULL,
  `substitute_id` int DEFAULT NULL
);

CREATE TABLE `category` (
  `id` int NOT NULL,
  `name` varchar(128) NOT NULL,
  `url` varchar(255) NOT NULL
);

CREATE TABLE `substitute` (
  `id` int NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `category` int DEFAULT NULL,
  `nutrition_grades` varchar(1) DEFAULT NULL,
  `stores` varchar(255) DEFAULT NULL
);

ALTER TABLE `aliment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `substitute` (`substitute_id`),
  ADD KEY `category` (`category`);

ALTER TABLE `category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `substitute`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category`);

ALTER TABLE `aliment`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `substitute`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `aliment`
  ADD CONSTRAINT `category` FOREIGN KEY (`category`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `substitute` FOREIGN KEY (`substitute_id`) REFERENCES `substitute` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `substitute`
  ADD CONSTRAINT `category_id` FOREIGN KEY (`category`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;