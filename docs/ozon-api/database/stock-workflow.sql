-- Ozon stock workflow schema extension
-- Database: MySQL 5.7+/8.x compatible
-- Run this file after docs/ozon-api/database/schema.sql.

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `ozon-service`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE `ozon-service`;

CREATE TABLE IF NOT EXISTS `ozon_warehouses` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `warehouse_id` BIGINT UNSIGNED NOT NULL COMMENT 'Ozon 仓库 ID',
  `name` VARCHAR(255) NULL COMMENT '仓库名称',
  `status` VARCHAR(64) NULL COMMENT '仓库状态',
  `is_rfbs` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否 rFBS 仓库',
  `is_kgt` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否支持大件商品',
  `raw_payload` LONGTEXT NULL COMMENT '仓库原始响应快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_warehouses_client_warehouse` (`client_id`, `warehouse_id`),
  KEY `idx_ozon_warehouses_status` (`client_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon FBS/rFBS 仓库缓存';

CREATE TABLE IF NOT EXISTS `ozon_product_stocks` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `offer_id` VARCHAR(50) NULL COMMENT '卖家系统商品货号',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id',
  `sku` BIGINT UNSIGNED NULL COMMENT 'Ozon SKU',
  `warehouse_id` BIGINT UNSIGNED NOT NULL COMMENT 'Ozon 仓库 ID',
  `stock` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '最近一次设置的可售库存数量',
  `present` INT UNSIGNED NULL COMMENT 'Ozon 查询返回的仓库库存总量',
  `reserved` INT UNSIGNED NULL COMMENT 'Ozon 查询返回的已预留数量',
  `last_stock_task_id` BIGINT UNSIGNED NULL COMMENT '最近一次本地库存更新批次 ID',
  `last_error` LONGTEXT NULL COMMENT '最近一次库存更新错误',
  `last_response_payload` LONGTEXT NULL COMMENT '最近一次库存响应或确认快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_product_stocks_offer` (`client_id`, `offer_id`, `warehouse_id`),
  UNIQUE KEY `uk_ozon_product_stocks_product` (`client_id`, `product_id`, `warehouse_id`),
  KEY `idx_ozon_product_stocks_sku` (`client_id`, `sku`, `warehouse_id`),
  KEY `idx_ozon_product_stocks_task` (`last_stock_task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品仓库库存快照';

CREATE TABLE IF NOT EXISTS `ozon_stock_update_tasks` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `request_id` VARCHAR(64) NOT NULL COMMENT '本地库存更新请求 ID，建议使用 UUID',
  `status` VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT '批次状态：pending/success/partial/failed',
  `request_payload` LONGTEXT NULL COMMENT '调用方原始请求，不含 Api-Key',
  `warehouse_payload` LONGTEXT NULL COMMENT '仓库列表响应快照',
  `product_payload` LONGTEXT NULL COMMENT '商品信息查询响应快照',
  `reserved_payload` LONGTEXT NULL COMMENT '预留库存查询响应快照',
  `response_payload` LONGTEXT NULL COMMENT 'Ozon 库存更新响应快照',
  `confirm_payload` LONGTEXT NULL COMMENT '库存更新后确认查询响应快照',
  `error_payload` LONGTEXT NULL COMMENT '批次级错误详情',
  `total_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '本次请求商品数量',
  `success_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '成功数量',
  `failed_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '失败数量',
  `submitted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  `finished_at` DATETIME NULL COMMENT '结束时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_stock_tasks_request` (`client_id`, `request_id`),
  KEY `idx_ozon_stock_tasks_status` (`client_id`, `status`, `submitted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品库存更新批次';

CREATE TABLE IF NOT EXISTS `ozon_stock_update_task_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `stock_task_id` BIGINT UNSIGNED NOT NULL COMMENT '本地库存更新批次 ID',
  `request_id` VARCHAR(64) NOT NULL COMMENT '本地库存更新请求 ID',
  `offer_id` VARCHAR(50) NULL COMMENT '卖家系统商品货号',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id',
  `sku` BIGINT UNSIGNED NULL COMMENT 'Ozon SKU',
  `warehouse_id` BIGINT UNSIGNED NOT NULL COMMENT 'Ozon 仓库 ID',
  `requested_stock` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '请求设置的可售库存数量',
  `present` INT UNSIGNED NULL COMMENT '确认查询返回的库存总量',
  `reserved` INT UNSIGNED NULL COMMENT '确认查询返回的已预留数量',
  `updated` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Ozon 是否返回更新成功',
  `status` VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT '单商品状态：pending/success/failed',
  `error_message` TEXT NULL COMMENT '单商品错误信息',
  `precheck_payload` LONGTEXT NULL COMMENT '商品信息查询快照',
  `reserved_payload` LONGTEXT NULL COMMENT '预留库存查询快照',
  `response_payload` LONGTEXT NULL COMMENT '库存更新响应快照',
  `confirm_payload` LONGTEXT NULL COMMENT '确认查询快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_stock_items_offer` (`client_id`, `request_id`, `offer_id`, `warehouse_id`),
  UNIQUE KEY `uk_ozon_stock_items_product` (`client_id`, `request_id`, `product_id`, `warehouse_id`),
  KEY `idx_ozon_stock_items_sku` (`client_id`, `sku`, `warehouse_id`),
  KEY `idx_ozon_stock_items_task` (`stock_task_id`),
  KEY `idx_ozon_stock_items_status` (`client_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品库存更新明细';
