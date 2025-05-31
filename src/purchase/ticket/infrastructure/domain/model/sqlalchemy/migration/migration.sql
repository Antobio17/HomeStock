CREATE TABLE IF NOT EXISTS `ticket` (
    `id` VARCHAR(36) NOT NULL,
    `supermarket` VARCHAR(64) NOT NULL,
    `reference` VARCHAR(64) NOT NULL,
    `status` VARCHAR(32) NOT NULL,
    `subtotal`  FLOAT NOT NULL,
    `discount_amount`  FLOAT NOT NULL,
    `taxes` JSON NOT NULL,
    `tax_amount`  FLOAT NOT NULL,
    `total`  FLOAT NOT NULL,
    `purchased_at` TIMESTAMP NOT NULL,
    `created_at` TIMESTAMP NOT NULL,
    `updated_at` TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `ticket_item` (
    `id` VARCHAR(36) NOT NULL,
    `ticket_id` VARCHAR(36) NOT NULL,
    `description` VARCHAR(64) NOT NULL,
    `quantity`  FLOAT NOT NULL,
    `unit_price`  FLOAT NOT NULL,
    `amount`  FLOAT NOT NULL,
    `format_id` VARCHAR(36) DEFAULT NULL,
    `product_id` VARCHAR(36) DEFAULT NULL,
    PRIMARY KEY (`id`)
);

CREATE INDEX index_ticket_id ON `ticket_item` (`ticket_id`);
CREATE INDEX index_format_id ON `ticket_item` (`format_id`);
CREATE INDEX index_product_id ON `ticket_item` (`product_id`);