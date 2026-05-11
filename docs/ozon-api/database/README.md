# Ozon API Service 数据库

数据库配置来自 [config.md](../config.md)：

- MySQL：`127.0.0.1:3306`
- 库名：`ozon-service`
- Redis：`127.0.0.1:6379`，库 `0`

## 文件

- [schema.sql](./schema.sql)：基础建库和建表语句，覆盖商品创建、更新、图片、类目属性缓存、异步任务和 API 调用日志。
- [archive-workflow.sql](./archive-workflow.sql)：归档工作流扩展表结构，覆盖商品归档、恢复归档、删除无 SKU 归档商品的批次、明细和状态历史。
- [unarchive-workflow.sql](./unarchive-workflow.sql)：从归档还原商品的可选状态字段扩展，批次、明细和历史继续复用归档工作流表。
- [stock-workflow.sql](./stock-workflow.sql)：设置商品上架数量/可售库存的仓库缓存、库存快照、批次和明细表。

## 初始化

先执行基础表：

```bash
mysql --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u ozonservice -p < docs/ozon-api/database/schema.sql
```

如果服务需要整合 [商品归档调用手册](../guides/product-archive-workflow.md) 中的接口，再执行归档扩展：

```bash
mysql --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u ozonservice -p < docs/ozon-api/database/archive-workflow.sql
```

如果服务还需要整合从归档还原商品接口，再执行还原扩展：

```bash
mysql --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u ozonservice -p < docs/ozon-api/database/unarchive-workflow.sql
```

如果服务需要整合设置上架数量接口，再执行库存扩展：

```bash
mysql --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u ozonservice -p < docs/ozon-api/database/stock-workflow.sql
```

## 设置上架数量扩展表说明

库存更新流程需要先确认仓库 ID，再查询商品信息，必要时查询预留库存，最后调用 Ozon 库存更新接口。因此建议保存：

- `ozon_warehouses`：仓库缓存，来自 `/v2/warehouse/list`。
- `ozon_product_stocks`：商品在仓库维度的库存快照。
- `ozon_stock_update_tasks`：一次库存更新批次。
- `ozon_stock_update_task_items`：批次中的单商品库存更新结果。

## 归档扩展表说明

归档流程需要先查商品信息，将 `offer_id`、`sku` 或本地 SKU 转成 Ozon `product_id`，再调用归档接口，最后再次查询确认 `is_archived=true`。因此建议保存三类数据：

- `ozon_products` 增加归档状态字段：`is_archived`、`is_autoarchived`、`archive_status`、`archived_at`、`archive_checked_at`、`last_archive_request_id`、`last_archive_error`。
- `ozon_archive_tasks`：一次归档/恢复/删除归档商品请求的批次记录，保存原始入参、Ozon 请求体、响应、确认结果和统计数量。
- `ozon_archive_task_items`：批次中的单商品明细，记录每个商品的 `offer_id`、`product_id`、`sku`、操作前后归档状态、成功/失败/跳过原因。
- `ozon_product_archive_history`：商品归档状态变更历史，用于审计和排查。

## 从归档还原扩展说明

从归档还原商品不需要新建独立批次表，继续复用归档工作流表：

- `ozon_archive_tasks.action_type = 'unarchive'`：记录一次还原批次。
- `ozon_archive_task_items.status`：记录单商品结果，例如 `success`、`failed`、`not_found`、`not_archived`。
- `ozon_product_archive_history.action_type = 'unarchive'`：记录归档状态从 true 到 false 的变化。
- `ozon_products` 可选增加 `unarchived_at`、`unarchive_checked_at`、`last_unarchive_request_id`、`last_unarchive_error`，便于后续报表和排查。

## 兼容性说明

SQL 使用 MySQL 5.7+/8.x 兼容写法：

- 排序规则使用 `utf8mb4_general_ci`，避免低版本 MySQL 不支持 `utf8mb4_0900_ai_ci`。
- 请求、响应、错误、缓存等结构化字段使用 `LONGTEXT` 存 JSON 字符串，避免部分 MySQL/MariaDB 环境不支持原生 `JSON` 类型。
- `archive-workflow.sql` 中的 `ALTER TABLE` 使用临时存储过程判断字段和索引是否存在，方便重复执行。

## 凭证处理规则

前端或调用方每次请求服务时传入 `Client-Id`、`Api-Key`。

- `Client-Id`：可以入库，用于区分店铺/调用方数据。
- `Api-Key`：不要明文入库。
- 如果异步轮询 Ozon `task_id` 需要继续使用 `Api-Key`，建议将 `Api-Key` 写入 Redis 短 TTL 缓存，然后只把 Redis key 保存到任务表的 `credential_ref`。
- API 调用日志如需定位凭证差异，可以保存 `Api-Key` 的 SHA-256 指纹到 `ozon_api_call_logs.api_key_fingerprint`，不要保存原文。
