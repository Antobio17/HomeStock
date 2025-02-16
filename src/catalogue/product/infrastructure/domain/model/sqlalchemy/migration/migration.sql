CREATE TABLE IF NOT EXISTS `product` (
  `id` VARCHAR(36) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `price` FLOAT NOT NULL,
  `calories` FLOAT NOT NULL,
  `carbohydrates` FLOAT NOT NULL,
  `proteins` FLOAT NOT NULL,
  `fats` FLOAT NOT NULL,
  `sugar` FLOAT NOT NULL,
  `is_enabled` TINYINT NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL,
  `updated_at` TIMESTAMP DEFAULT NULL,
  `enabled_at` TIMESTAMP NOT NULL,
  `disabled_at` TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (`id`));