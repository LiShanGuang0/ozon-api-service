-- Ozon API service schema
-- Database: MySQL 5.7+/8.x compatible
-- Config reference: docs/ozon-api/config.md
--
-- Important credential rule:
-- The caller passes Client-Id and Api-Key on each request.
-- Persist Client-Id for tenant/data isolation, but do not persist plaintext Api-Key.
-- If async polling needs credentials, store Api-Key in Redis with a short TTL and save only credential_ref here.

CREATE DATABASE IF NOT EXISTS `ozon-service`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE `ozon-service`;

CREATE TABLE IF NOT EXISTS `ozon_products` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id，用于多店铺/多调用方数据隔离',
  `local_sku` VARCHAR(128) NULL COMMENT '本地系统 SKU',
  `offer_id` VARCHAR(50) NOT NULL COMMENT '卖家系统商品货号，Ozon 创建/更新核心标识',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id，创建成功后回写',
  `sku` BIGINT UNSIGNED NULL COMMENT 'Ozon SKU，如接口返回则回写',
  `name` VARCHAR(500) NULL COMMENT '商品名称',
  `description_category_id` BIGINT UNSIGNED NULL COMMENT '类目 ID',
  `type_id` BIGINT UNSIGNED NULL COMMENT '商品类型 ID',
  `currency_code` VARCHAR(16) NULL COMMENT '币种，例如 RUB、CNY、USD',
  `price` DECIMAL(18, 2) NULL COMMENT '当前售价',
  `old_price` DECIMAL(18, 2) NULL COMMENT '划线价',
  `vat` VARCHAR(16) NULL COMMENT '增值税税率',
  `barcode` VARCHAR(128) NULL COMMENT '商品条码',
  `sync_status` VARCHAR(32) NOT NULL DEFAULT 'draft' COMMENT '本地同步状态：draft/pending/imported/failed/skipped/archived',
  `ozon_status` VARCHAR(64) NULL COMMENT 'Ozon 商品状态',
  `last_task_id` BIGINT UNSIGNED NULL COMMENT '最近一次导入/更新任务 ID',
  `last_error` LONGTEXT NULL COMMENT '最近一次错误详情',
  `last_request_payload` LONGTEXT NULL COMMENT '最近一次提交给 Ozon 的商品 item 快照，不含 Api-Key',
  `last_response_payload` LONGTEXT NULL COMMENT '最近一次 Ozon 响应快照',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_products_client_offer` (`client_id`, `offer_id`),
  KEY `idx_ozon_products_client_product` (`client_id`, `product_id`),
  KEY `idx_ozon_products_client_sku` (`client_id`, `sku`),
  KEY `idx_ozon_products_category_type` (`description_category_id`, `type_id`),
  KEY `idx_ozon_products_sync_status` (`client_id`, `sync_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品本地映射表';

CREATE TABLE IF NOT EXISTS `ozon_product_attributes` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `offer_id` VARCHAR(50) NOT NULL COMMENT '商品货号',
  `attribute_id` BIGINT UNSIGNED NOT NULL COMMENT 'Ozon 属性 ID',
  `complex_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '复合属性 ID，普通属性为 0',
  `dictionary_value_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '字典值 ID，无字典时为 0',
  `value` TEXT NULL COMMENT '属性值',
  `value_json` LONGTEXT NULL COMMENT '复杂属性值原始结构',
  `is_required` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为该类目必填属性',
  `source` VARCHAR(32) NOT NULL DEFAULT 'local' COMMENT '来源：local/ozon/cache',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_product_attrs_value` (`client_id`, `offer_id`, `attribute_id`, `complex_id`, `dictionary_value_id`),
  KEY `idx_ozon_product_attrs_offer` (`client_id`, `offer_id`),
  KEY `idx_ozon_product_attrs_attr` (`attribute_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='商品属性本地快照';

CREATE TABLE IF NOT EXISTS `ozon_product_images` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `offer_id` VARCHAR(50) NOT NULL COMMENT '商品货号',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id',
  `url` VARCHAR(2048) NOT NULL COMMENT '公共可访问图片 URL',
  `image_type` VARCHAR(32) NOT NULL DEFAULT 'image' COMMENT 'image/primary/images360/color',
  `sort_order` INT NOT NULL DEFAULT 0 COMMENT '图片顺序',
  `is_primary` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否主图',
  `state` VARCHAR(32) NULL COMMENT 'Ozon 图片处理状态',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_product_images_url` (`client_id`, `offer_id`, `image_type`, `url`(255)),
  KEY `idx_ozon_product_images_offer` (`client_id`, `offer_id`),
  KEY `idx_ozon_product_images_product` (`client_id`, `product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='商品图片本地快照';

CREATE TABLE IF NOT EXISTS `ozon_import_tasks` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `task_id` BIGINT UNSIGNED NOT NULL COMMENT 'Ozon 异步任务 ID',
  `action_type` VARCHAR(32) NOT NULL COMMENT '任务类型：product_import/attribute_update/picture_import',
  `status` VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT '任务状态：pending/imported/failed/skipped/partial',
  `credential_ref` VARCHAR(128) NULL COMMENT 'Redis 中短期凭证引用，不保存明文 Api-Key',
  `request_payload` LONGTEXT NULL COMMENT '提交 Ozon 的请求体，不含 Api-Key',
  `response_payload` LONGTEXT NULL COMMENT 'Ozon 创建任务响应',
  `result_payload` LONGTEXT NULL COMMENT '轮询任务结果',
  `error_payload` LONGTEXT NULL COMMENT '错误详情',
  `submitted_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交任务时间',
  `last_polled_at` DATETIME NULL COMMENT '最近一次轮询时间',
  `finished_at` DATETIME NULL COMMENT '任务结束时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_import_tasks_client_task` (`client_id`, `task_id`),
  KEY `idx_ozon_import_tasks_status` (`client_id`, `status`, `last_polled_at`),
  KEY `idx_ozon_import_tasks_action` (`client_id`, `action_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 商品导入/更新异步任务';

CREATE TABLE IF NOT EXISTS `ozon_import_task_items` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `task_id` BIGINT UNSIGNED NOT NULL COMMENT 'Ozon 异步任务 ID',
  `offer_id` VARCHAR(50) NOT NULL COMMENT '商品货号',
  `product_id` BIGINT UNSIGNED NULL COMMENT 'Ozon product_id',
  `status` VARCHAR(32) NOT NULL DEFAULT 'pending' COMMENT '单商品任务状态',
  `errors` LONGTEXT NULL COMMENT 'Ozon 返回的单商品错误数组',
  `raw_item` LONGTEXT NULL COMMENT '单商品结果原文',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_task_items_offer` (`client_id`, `task_id`, `offer_id`),
  KEY `idx_ozon_task_items_status` (`client_id`, `status`),
  KEY `idx_ozon_task_items_offer` (`client_id`, `offer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 异步任务商品明细';

CREATE TABLE IF NOT EXISTS `ozon_category_tree_cache` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `language` VARCHAR(32) NOT NULL DEFAULT 'ZH_HANS' COMMENT '语言',
  `tree_json` LONGTEXT NOT NULL COMMENT '类目树响应 result',
  `source_hash` CHAR(64) NULL COMMENT '响应内容 hash，用于判断变化',
  `expired_at` DATETIME NULL COMMENT '缓存过期时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_category_tree_language` (`language`),
  KEY `idx_ozon_category_tree_expired` (`expired_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 类目树缓存，通常不按店铺区分';

CREATE TABLE IF NOT EXISTS `ozon_category_attributes_cache` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `description_category_id` BIGINT UNSIGNED NOT NULL COMMENT '类目 ID',
  `type_id` BIGINT UNSIGNED NOT NULL COMMENT '商品类型 ID',
  `language` VARCHAR(32) NOT NULL DEFAULT 'ZH_HANS' COMMENT '语言',
  `attributes_json` LONGTEXT NOT NULL COMMENT '类目属性响应 result',
  `source_hash` CHAR(64) NULL COMMENT '响应内容 hash，用于判断变化',
  `expired_at` DATETIME NULL COMMENT '缓存过期时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_category_attrs` (`description_category_id`, `type_id`, `language`),
  KEY `idx_ozon_category_attrs_expired` (`expired_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 类目属性缓存';

CREATE TABLE IF NOT EXISTS `ozon_attribute_values_cache` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `description_category_id` BIGINT UNSIGNED NOT NULL COMMENT '类目 ID',
  `type_id` BIGINT UNSIGNED NOT NULL COMMENT '商品类型 ID',
  `attribute_id` BIGINT UNSIGNED NOT NULL COMMENT '属性 ID',
  `language` VARCHAR(32) NOT NULL DEFAULT 'ZH_HANS' COMMENT '语言',
  `search_value` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '搜索关键词；空字符串表示分页/全量值缓存',
  `last_value_id` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '分页起点',
  `has_next` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Ozon 是否还有下一页',
  `values_json` LONGTEXT NOT NULL COMMENT '属性值响应 result',
  `source_hash` CHAR(64) NULL COMMENT '响应内容 hash，用于判断变化',
  `expired_at` DATETIME NULL COMMENT '缓存过期时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_ozon_attr_values` (`description_category_id`, `type_id`, `attribute_id`, `language`, `search_value`, `last_value_id`),
  KEY `idx_ozon_attr_values_attr` (`attribute_id`),
  KEY `idx_ozon_attr_values_expired` (`expired_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon 属性字典值缓存';

CREATE TABLE IF NOT EXISTS `ozon_api_call_logs` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '本地主键',
  `client_id` VARCHAR(64) NOT NULL COMMENT 'Ozon Client-Id',
  `api_key_fingerprint` CHAR(64) NULL COMMENT 'Api-Key 指纹，可选；不要保存明文 Api-Key',
  `request_id` VARCHAR(128) NULL COMMENT '调用方请求 ID 或链路 ID',
  `endpoint` VARCHAR(255) NOT NULL COMMENT 'Ozon API 路径',
  `http_method` VARCHAR(16) NOT NULL DEFAULT 'POST' COMMENT 'HTTP 方法',
  `http_status` INT NULL COMMENT 'HTTP 状态码',
  `success` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否成功',
  `duration_ms` INT UNSIGNED NULL COMMENT '耗时毫秒',
  `request_payload` LONGTEXT NULL COMMENT '请求体，不含 Api-Key',
  `response_payload` LONGTEXT NULL COMMENT '响应体',
  `error_message` TEXT NULL COMMENT '错误信息',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_ozon_api_logs_client_time` (`client_id`, `created_at`),
  KEY `idx_ozon_api_logs_endpoint` (`endpoint`),
  KEY `idx_ozon_api_logs_request_id` (`request_id`),
  KEY `idx_ozon_api_logs_success` (`success`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Ozon API 调用日志，敏感凭证脱敏';

