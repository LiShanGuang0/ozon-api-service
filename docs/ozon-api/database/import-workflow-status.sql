-- Store end-to-end import workflow status as a standalone task column.
-- MySQL 5.7+/8.x compatible. Safe to run repeatedly.

SET NAMES utf8mb4;

USE `ozon-service`;

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_import_tasks' AND COLUMN_NAME = 'workflow_status') = 0,
  'ALTER TABLE `ozon_import_tasks` ADD COLUMN `workflow_status` VARCHAR(32) NOT NULL DEFAULT ''import_pending'' COMMENT ''完整链路状态：import_pending/imported/stock_updated/attributes_synced/stock_synced/completed/failed'' AFTER `status`',
  'SELECT ''skip ozon_import_tasks.workflow_status'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

UPDATE `ozon_import_tasks`
SET `workflow_status` = CASE
  WHEN `status` = 'pending' THEN 'import_pending'
  WHEN `status` = 'imported' THEN 'imported'
  ELSE 'failed'
END
WHERE `workflow_status` = 'import_pending';

SET @ddl = IF(
  (SELECT COUNT(*) FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'ozon_import_tasks' AND INDEX_NAME = 'idx_ozon_import_tasks_workflow_status') = 0,
  'ALTER TABLE `ozon_import_tasks` ADD INDEX `idx_ozon_import_tasks_workflow_status` (`client_id`, `workflow_status`, `submitted_at`)',
  'SELECT ''skip idx_ozon_import_tasks_workflow_status'''
);
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
