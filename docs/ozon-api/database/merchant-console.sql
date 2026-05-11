-- Ozon merchant tablet console schema extension
-- Database: MySQL 5.7+/8.x compatible
-- Run this file after:
--   docs/ozon-api/database/schema.sql
--   docs/ozon-api/database/stock-workflow.sql
--   docs/ozon-api/database/archive-workflow.sql
--
-- Purpose:
--   Support merchant-facing H5/tablet console:
--   - merchant profile
--   - merchant user login
--   - rolling push/task event stream
--
-- Security:
--   Do not store plaintext Ozon Api-Key here.
--   If long-term credentials are needed, store them in a secret manager and save only secret_ref.

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `ozon-service`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE `ozon-service`;

CREATE TABLE IF NOT EXISTS `ozon_merchants` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `merchant_id` VARCHAR(64) NOT NULL COMMENT '运营平台商户 ID',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id，用于关联现有 Ozon 数据',
  `shop_name` VARCHAR(255) NOT NULL COMMENT '商户店铺名称',
  `display_name` VARCHAR(255) NULL COMMENT 'H5 展示名称，不填时使用 shop_name',
  `logo_url` VARCHAR(1024) NULL COMMENT '店铺头像或 Logo URL',
  `status` VARCHAR(32) NOT NULL DEFAULT 'active' COMMENT '商户状态：active/disabled/pending',
  `currency_code` VARCHAR(16) NULL COMMENT '店铺币种，例如 RUB/CNY/USD',
  `default_warehouse_id` BIGINT UNSIGNED NULL COMMENT '默认 Ozon 仓库 ID',
  `contact_name` VARCHAR(128) NULL COMMENT '联系人',
  `contact_phone` VARCHAR(64) NULL COMMENT '联系电话',
  `contact_email` VARCHAR(255) NULL COMMENT '联系邮箱',
  `api_key_fingerprint` CHAR(64) NULL COMMENT 'Ozon Api-Key SHA-256 指纹，不保存明文',
  `secret_ref` VARCHAR(255) NULL COMMENT '外部密钥系统引用，可选',
  `last_connected_at` DATETIME NULL COMMENT '最近一次成功连接 Ozon 时间',
  `last_error` TEXT NULL COMMENT '最近一次连接或推送错误',
  `remark` VARCHAR(500) NULL COMMENT '备注',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_merchants_merchant` (`merchant_id`),
  UNIQUE KEY `uk_ozon_merchants_client` (`client_id`),
  KEY `idx_ozon_merchants_status` (`status`, `updated_at`),
  KEY `idx_ozon_merchants_warehouse` (`client_id`, `default_warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='H5 商户信息表';

CREATE TABLE IF NOT EXISTS `ozon_merchant_users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `merchant_id` VARCHAR(64) NOT NULL COMMENT '运营平台商户 ID，对应 ozon_merchants.merchant_id',
  `username` VARCHAR(128) NOT NULL COMMENT '登录用户名',
  `phone` VARCHAR(64) NULL COMMENT '手机号，可用于登录',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '登录密码哈希',
  `role` VARCHAR(32) NOT NULL DEFAULT 'merchant_admin' COMMENT '角色：merchant_admin/operator/viewer',
  `status` VARCHAR(32) NOT NULL DEFAULT 'active' COMMENT '用户状态：active/disabled',
  `last_login_at` DATETIME NULL COMMENT '最近登录时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_merchant_users_username` (`username`),
  UNIQUE KEY `uk_ozon_merchant_users_phone` (`phone`),
  KEY `idx_ozon_merchant_users_merchant` (`merchant_id`, `status`),
  CONSTRAINT `fk_ozon_merchant_users_merchant`
    FOREIGN KEY (`merchant_id`) REFERENCES `ozon_merchants` (`merchant_id`)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='H5 商户登录用户表';

CREATE TABLE IF NOT EXISTS `ozon_task_events` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id；H5 按当前商户 client_id 隔离查询',
  `event_type` VARCHAR(32) NOT NULL COMMENT '事件类型：product_import/stock_update/archive/unarchive/api_call/system',
  `ref_type` VARCHAR(32) NULL COMMENT '关联对象类型：import_task/stock_task/archive_task/product/api_log',
  `ref_id` BIGINT UNSIGNED NULL COMMENT '关联本地表主键 ID',
  `ozon_task_id` BIGINT UNSIGNED NULL COMMENT 'Ozon 异步任务 ID，如 product import task_id',
  `request_id` VARCHAR(128) NULL COMMENT '本地请求 ID 或链路 ID',
  `offer_id` VARCHAR(50) NULL COMMENT '商品货号；流水框显示该字段',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id',
  `sku` BIGINT UNSIGNED NULL COMMENT 'Ozon SKU',
  `status` VARCHAR(32) NOT NULL COMMENT '状态：pending/running/success/failed/skipped/info',
  `message` VARCHAR(500) NOT NULL COMMENT 'H5 展示文案，不包含店铺名',
  `error_message` TEXT NULL COMMENT '失败原因',
  `payload` LONGTEXT NULL COMMENT '事件上下文快照，不含 Api-Key',
  `is_visible` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否在商户 H5 流水中展示',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_ozon_task_events_client_time` (`client_id`, `created_at`),
  KEY `idx_ozon_task_events_client_status` (`client_id`, `status`, `created_at`),
  KEY `idx_ozon_task_events_offer_time` (`client_id`, `offer_id`, `created_at`),
  KEY `idx_ozon_task_events_ozon_task` (`client_id`, `ozon_task_id`),
  KEY `idx_ozon_task_events_request` (`client_id`, `request_id`),
  KEY `idx_ozon_task_events_ref` (`ref_type`, `ref_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='H5 滚动推送流水事件表';

CREATE TABLE IF NOT EXISTS `ozon_merchant_action_logs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `user_id` BIGINT UNSIGNED NULL COMMENT '操作用户 ID，对应 ozon_merchant_users.id',
  `action_type` VARCHAR(64) NOT NULL COMMENT '操作类型：login/logout/view_task/retry_push/update_stock等',
  `target_type` VARCHAR(64) NULL COMMENT '操作对象类型',
  `target_id` VARCHAR(128) NULL COMMENT '操作对象 ID',
  `request_payload` LONGTEXT NULL COMMENT '请求快照，不含敏感凭证',
  `result_payload` LONGTEXT NULL COMMENT '结果快照',
  `ip_address` VARCHAR(64) NULL COMMENT '客户端 IP',
  `user_agent` VARCHAR(500) NULL COMMENT '客户端 UA',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_ozon_merchant_action_logs_client_time` (`client_id`, `created_at`),
  KEY `idx_ozon_merchant_action_logs_user_time` (`user_id`, `created_at`),
  KEY `idx_ozon_merchant_action_logs_action` (`client_id`, `action_type`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='H5 商户端操作日志';

