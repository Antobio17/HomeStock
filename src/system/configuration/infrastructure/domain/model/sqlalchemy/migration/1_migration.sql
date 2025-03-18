CREATE TABLE IF NOT EXISTS `configuration` (
    `id` VARCHAR(36) NOT NULL,
    `code` VARCHAR(32) NOT NULL,
    `payload` JSON NOT NULL,
    `created_at` TIMESTAMP NOT NULL,
    `updated_at` TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (`id`)
);