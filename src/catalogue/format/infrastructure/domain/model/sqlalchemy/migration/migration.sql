CREATE TABLE IF NOT EXISTS `format` (
  `id` VARCHAR(36) NOT NULL,
  `product_id` VARCHAR(36) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `recipe_unit` VARCHAR(64) NOT NULL,
  `storage_unit` VARCHAR(64) NOT NULL,
  `storage_unit_equivalence` FLOAT NOT NULL DEFAULT 1.0,
  `purchase_unit` VARCHAR(64) NOT NULL,
  `purchase_unit_equivalence` FLOAT NOT NULL DEFAULT 1.0,
  `purchase_price` FLOAT NOT NULL DEFAULT 0.0,
  `is_enabled` TINYINT NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL,
  `updated_at` TIMESTAMP DEFAULT NULL,
  `enabled_at` TIMESTAMP NOT NULL,
  `disabled_at` TIMESTAMP DEFAULT NULL,
  PRIMARY KEY (`id`));
  CREATE INDEX index_product_id ON `format` (`product_id`);