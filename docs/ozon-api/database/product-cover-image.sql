-- Store product list cover image as a standalone column.
-- MySQL 5.7+/8.x compatible. Safe to run repeatedly.

SET NAMES utf8mb4;

USE `ozon-service`;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_products' AND COLUMN_NAME = 'cover_image_url') = 0,
  'ALTER TABLE `ozon_products` ADD COLUMN `cover_image_url` VARCHAR(2048) NULL COMMENT ''商品列表封面图 URL'' AFTER `name`',
  'SELECT ''skip ozon_products.cover_image_url'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
