-- Store product import warehouse/stock as standalone columns.
-- MySQL 5.7+/8.x compatible. Safe to run repeatedly.

SET NAMES utf8mb4;

USE `ozon-service`;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_products' AND COLUMN_NAME = 'warehouse_id') = 0,
  'ALTER TABLE `ozon_products` ADD COLUMN `warehouse_id` BIGINT UNSIGNED NULL COMMENT ''导入成功后设置库存使用的 Ozon 仓库 ID'' AFTER `sku`',
  'SELECT ''skip ozon_products.warehouse_id'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_products' AND COLUMN_NAME = 'stock') = 0,
  'ALTER TABLE `ozon_products` ADD COLUMN `stock` INT UNSIGNED NULL COMMENT ''导入成功后设置的可售库存数量'' AFTER `warehouse_id`',
  'SELECT ''skip ozon_products.stock'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_import_tasks' AND COLUMN_NAME = 'default_warehouse_id') = 0,
  'ALTER TABLE `ozon_import_tasks` ADD COLUMN `default_warehouse_id` BIGINT UNSIGNED NULL COMMENT ''本次导入请求默认仓库 ID'' AFTER `credential_ref`',
  'SELECT ''skip ozon_import_tasks.default_warehouse_id'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_import_tasks' AND COLUMN_NAME = 'default_stock') = 0,
  'ALTER TABLE `ozon_import_tasks` ADD COLUMN `default_stock` INT UNSIGNED NULL COMMENT ''本次导入请求默认可售库存'' AFTER `default_warehouse_id`',
  'SELECT ''skip ozon_import_tasks.default_stock'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_import_task_items' AND COLUMN_NAME = 'warehouse_id') = 0,
  'ALTER TABLE `ozon_import_task_items` ADD COLUMN `warehouse_id` BIGINT UNSIGNED NULL COMMENT ''本次导入成功后设置库存使用的 Ozon 仓库 ID'' AFTER `product_id`',
  'SELECT ''skip ozon_import_task_items.warehouse_id'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_import_task_items' AND COLUMN_NAME = 'stock') = 0,
  'ALTER TABLE `ozon_import_task_items` ADD COLUMN `stock` INT UNSIGNED NULL COMMENT ''本次导入成功后设置的可售库存数量'' AFTER `warehouse_id`',
  'SELECT ''skip ozon_import_task_items.stock'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
