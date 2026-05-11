-- Ozon archive workflow schema extension
-- Database: MySQL 5.7+/8.x compatible
-- Run this file after docs/ozon-api/database/schema.sql.
--
-- Credential rule:
-- The caller passes Client-Id and Api-Key on each request.
-- Persist Client-Id for tenant/data isolation, but do not persist plaintext Api-Key.
-- The archive API is synchronous today, so this extension stores workflow/audit data only.

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
  'is_archived',
  '`is_archived` TINYINT(1) NOT NULL DEFAULT 0 COMMENT ''是否手动归档'' AFTER `ozon_status`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'is_autoarchived',
  '`is_autoarchived` TINYINT(1) NOT NULL DEFAULT 0 COMMENT ''是否被 Ozon 自动归档'' AFTER `is_archived`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'archive_status',
  '`archive_status` VARCHAR(32) NULL COMMENT ''归档流程状态：active/archived/autoarchived/unarchived/delete_pending/deleted'' AFTER `is_autoarchived`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'archived_at',
  '`archived_at` DATETIME NULL COMMENT ''确认归档成功时间'' AFTER `archive_status`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'archive_checked_at',
  '`archive_checked_at` DATETIME NULL COMMENT ''最近一次查询 Ozon 归档状态时间'' AFTER `archived_at`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'last_archive_request_id',
  '`last_archive_request_id` VARCHAR(64) NULL COMMENT ''最近一次本地归档请求 ID'' AFTER `archive_checked_at`'
);

CALL `add_column_if_not_exists`(
  'ozon_products',
  'last_archive_error',
  '`last_archive_error` LONGTEXT NULL COMMENT ''最近一次归档错误详情'' AFTER `last_archive_request_id`'
);

CALL `add_index_if_not_exists`(
  'ozon_products',
  'idx_ozon_products_archived',
  'INDEX `idx_ozon_products_archived` (`client_id`, `is_archived`)'
);

CALL `add_index_if_not_exists`(
  'ozon_products',
  'idx_ozon_products_autoarchived',
  'INDEX `idx_ozon_products_autoarchived` (`client_id`, `is_autoarchived`)'
);

CALL `add_index_if_not_exists`(
  'ozon_products',
  'idx_ozon_products_archive_status',
  'INDEX `idx_ozon_products_archive_status` (`client_id`, `archive_status`)'
);

DROP PROCEDURE IF EXISTS `add_column_if_not_exists`;
DROP PROCEDURE IF EXISTS `add_index_if_not_exists`;

CREATE TABLE IF NOT EXISTS `ozon_archive_tasks` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id，用于多店铺/多调用方数据隔离',
  `request_id` VARCHAR(64) NOT NULL COMMENT '本地归档请求 ID，建议使用 UUID',
  `action_type` VARCHAR(32) NOT NULL DEFAULT 'archive' COMMENT '操作类型：archive/unarchive/delete_no_sku_archive',
  `status` VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT '批次状态：pending/success/partial/failed/skipped',
  `credential_ref` VARCHAR(128) NULL COMMENT 'Redis 中短期凭证引用；通常归档同步执行不需要保存',
  `input_identifiers` LONGTEXT NULL COMMENT '调用方传入的原始标识，如 offer_id/product_id/sku，不含 Api-Key',
  `precheck_payload` LONGTEXT NULL COMMENT '归档前商品查询响应快照',
  `request_payload` LONGTEXT NULL COMMENT '提交给 Ozon 归档/恢复/删除接口的请求体，不含 Api-Key',
  `response_payload` LONGTEXT NULL COMMENT 'Ozon 操作接口响应快照',
  `confirm_payload` LONGTEXT NULL COMMENT '操作后商品查询确认响应快照',
  `error_payload` LONGTEXT NULL COMMENT '批次级错误详情',
  `total_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '传入或解析出的商品总数',
  `success_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '成功数量',
  `failed_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '失败数量',
  `skipped_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '跳过数量，如已归档或未找到',
  `submitted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  `finished_at` DATETIME NULL COMMENT '结束时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_archive_tasks_request` (`client_id`, `request_id`),
  KEY `idx_ozon_archive_tasks_status` (`client_id`, `status`, `submitted_at`),
  KEY `idx_ozon_archive_tasks_action` (`client_id`, `action_type`, `submitted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品归档/恢复/删除归档商品批次';

CREATE TABLE IF NOT EXISTS `ozon_archive_task_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `archive_task_id` BIGINT UNSIGNED NOT NULL COMMENT '本地归档批次 ID，对应 ozon_archive_tasks.id',
  `request_id` VARCHAR(64) NOT NULL COMMENT '本地归档请求 ID，便于排查链路',
  `identifier_type` VARCHAR(32) NULL COMMENT '调用方原始标识类型：offer_id/product_id/sku/local_sku',
  `identifier_value` VARCHAR(128) NULL COMMENT '调用方原始标识值',
  `offer_id` VARCHAR(50) NULL COMMENT '卖家系统商品货号',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id，归档接口实际使用该字段',
  `sku` BIGINT UNSIGNED NULL COMMENT 'Ozon SKU',
  `before_is_archived` TINYINT(1) NULL COMMENT '操作前是否手动归档',
  `before_is_autoarchived` TINYINT(1) NULL COMMENT '操作前是否自动归档',
  `after_is_archived` TINYINT(1) NULL COMMENT '操作后是否手动归档',
  `after_is_autoarchived` TINYINT(1) NULL COMMENT '操作后是否自动归档',
  `status` VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT '单商品状态：pending/success/failed/skipped/not_found/already_archived',
  `skip_reason` VARCHAR(255) NULL COMMENT '跳过原因',
  `error_message` TEXT NULL COMMENT '单商品错误信息',
  `precheck_payload` LONGTEXT NULL COMMENT '归档前该商品查询快照',
  `operation_response_payload` LONGTEXT NULL COMMENT '归档/恢复/删除接口响应快照',
  `confirm_payload` LONGTEXT NULL COMMENT '操作后该商品确认快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_archive_items_product` (`client_id`, `request_id`, `product_id`),
  KEY `idx_ozon_archive_items_task` (`archive_task_id`),
  KEY `idx_ozon_archive_items_offer` (`client_id`, `offer_id`),
  KEY `idx_ozon_archive_items_sku` (`client_id`, `sku`),
  KEY `idx_ozon_archive_items_status` (`client_id`, `status`),
  KEY `idx_ozon_archive_items_identifier` (`client_id`, `identifier_type`, `identifier_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品归档批次明细';

CREATE TABLE IF NOT EXISTS `ozon_product_archive_history` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `archive_task_id` BIGINT UNSIGNED NULL COMMENT '关联本地归档批次 ID',
  `request_id` VARCHAR(64) NULL COMMENT '本地归档请求 ID',
  `action_type` VARCHAR(32) NOT NULL COMMENT '操作类型：archive/unarchive/delete_no_sku_archive/confirm_query',
  `source` VARCHAR(32) NOT NULL DEFAULT 'archive_workflow' COMMENT '来源：archive_workflow/confirm_query/manual/sync',
  `offer_id` VARCHAR(50) NULL COMMENT '卖家系统商品货号',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id',
  `sku` BIGINT UNSIGNED NULL COMMENT 'Ozon SKU',
  `from_is_archived` TINYINT(1) NULL COMMENT '变化前是否手动归档',
  `to_is_archived` TINYINT(1) NULL COMMENT '变化后是否手动归档',
  `from_is_autoarchived` TINYINT(1) NULL COMMENT '变化前是否自动归档',
  `to_is_autoarchived` TINYINT(1) NULL COMMENT '变化后是否自动归档',
  `payload` LONGTEXT NULL COMMENT '触发本次历史记录的响应或状态快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_ozon_archive_history_product` (`client_id`, `product_id`, `created_at`),
  KEY `idx_ozon_archive_history_offer` (`client_id`, `offer_id`, `created_at`),
  KEY `idx_ozon_archive_history_request` (`client_id`, `request_id`),
  KEY `idx_ozon_archive_history_action` (`client_id`, `action_type`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品归档状态变更历史';
