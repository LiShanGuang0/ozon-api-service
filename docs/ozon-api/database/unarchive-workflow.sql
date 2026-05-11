-- Ozon unarchive workflow schema extension
-- Database: MySQL 5.7+/8.x compatible
-- Run this file after docs/ozon-api/database/schema.sql and archive-workflow.sql.
--
-- The workflow reuses:
--   ozon_archive_tasks
--   ozon_archive_task_items
--   ozon_product_archive_history
-- with action_type = 'unarchive'.

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `ozon-service`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE `ozon-service`;

DELIMITER $$

DROP PROCEDURE IF EXISTS `add_column_if_not_exists` $$
CREATE PROCEDURE `add_column_if_not_exists`(
  IN p_table_name VARCHAR(64),
  IN p_column_name VARCHAR(64),
  IN p_column_definition TEXT
)
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = p_table_name
      AND COLUMN_NAME = p_column_name
  ) THEN
    SET @ddl = CONCAT('ALTER TABLE `', p_table_name, '` ADD COLUMN ', p_column_definition);
    PREPARE stmt FROM @ddl;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
  END IF;
END $$

DROP PROCEDURE IF EXISTS `add_index_if_not_exists` $$
CREATE PROCEDURE `add_index_if_not_exists`(
  IN p_table_name VARCHAR(64),
  IN p_index_name VARCHAR(64),
  IN p_index_definition TEXT
)
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = p_table_name
      AND INDEX_NAME = p_index_name
  ) THEN
    SET @ddl = CONCAT('ALTER TABLE `', p_table_name, '` ADD ', p_index_definition);
    PREPARE stmt FROM @ddl;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
  END IF;
END $$

DELIMITER ;

CALL `add_column_if_not_exists`(
  'ozon_products',
  'unarchived_at',
  '`unarchived_at` DATETIME NULL COMMENT ''确认从归档还原成功时间'' AFTER `archived_at`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'unarchive_checked_at',
  '`unarchive_checked_at` DATETIME NULL COMMENT ''最近一次查询 Ozon 还原状态时间'' AFTER `unarchived_at`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'last_unarchive_request_id',
  '`last_unarchive_request_id` VARCHAR(64) NULL COMMENT ''最近一次本地还原请求 ID'' AFTER `last_archive_request_id`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'last_unarchive_error',
  '`last_unarchive_error` LONGTEXT NULL COMMENT ''最近一次从归档还原错误详情'' AFTER `last_unarchive_request_id`'
);

CALL `add_index_if_not_exists`(
  'ozon_products',
  'idx_ozon_products_unarchived_at',
  'INDEX `idx_ozon_products_unarchived_at` (`client_id`, `unarchived_at`)'
);

DROP PROCEDURE IF EXISTS `add_column_if_not_exists`;
DROP PROCEDURE IF EXISTS `add_index_if_not_exists`;
