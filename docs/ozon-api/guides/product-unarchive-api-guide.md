# 从归档还原商品接口调用文档

本文档说明如果调用本地 FastAPI 服务从归档还原 Ozon 商品，需要调用哪些服务接口、传哪些请求头和参数，以及响应结构如何理解。

本地服务地址示例：

```text
http://127.0.0.1:8000
```

## 推荐调用接口

```http
POST /api/ozon/products/unarchive
```

该接口会在服务端自动完成：

1. 调用 Ozon `POST /v3/product/info/list` 查询商品信息。
2. 将 `offer_id`、`sku` 转换为 Ozon `product_id`。
3. 过滤未归档商品。
4. 按每批最多 100 个 `product_id` 调用 Ozon `POST /v1/product/unarchive`。
5. 再次调用 Ozon `POST /v3/product/info/list` 确认 `is_archived=false`、`is_autoarchived=false`。
6. 将还原批次、单商品结果、状态变化历史写入本地数据库。

## 请求地址

```http
POST http://127.0.0.1:8000/api/ozon/products/unarchive
```

## 请求头

| 请求头 | 必填 | 示例 | 说明 |
| --- | --- | --- | --- |
| `Client-Id` | 是 | `123456` | Ozon Seller API 的 Client-Id。本地服务会用它做店铺/调用方数据隔离。 |
| `Api-Key` | 是 | `xxxxx` | Ozon Seller API 的 Api-Key。本地服务不会把明文 Api-Key 写入 MySQL。 |
| `Content-Type` | 是 | `application/json` | 请求体格式。 |
| `X-Request-Id` | 否 | `unarchive-20260508-001` | 调用方链路 ID。当前整合接口会生成自己的 `request_id`。 |

## 请求参数

至少传 `offer_id`、`product_id`、`sku` 中的一种。

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `offer_id` | string[] | 否 | 卖家系统商品货号。服务会先查询商品信息并转换为 Ozon `product_id`。 |
| `product_id` | integer[] 或 string[] | 否 | Ozon 商品 ID。还原接口最终只接受该字段。 |
| `sku` | integer[] 或 string[] | 否 | Ozon SKU。服务会先查询商品信息并转换为 Ozon `product_id`。 |
| `confirm` | boolean | 否 | 是否还原后再次查询确认。默认 `true`，建议保持默认。 |

限制：

- `offer_id`、`product_id`、`sku` 的总数量不能超过 1000。
- Ozon 还原接口单次最多接收 100 个 `product_id`，本地服务会自动拆批。
- 未归档商品不会调用 Ozon 还原接口，会在结果中返回 `not_archived`。
- 自动归档商品每天最多恢复 10 件；手动归档商品无该限制。

## 请求示例

### 按 offer_id 还原

```bash
curl -X POST "http://127.0.0.1:8000/api/ozon/products/unarchive" ^
  -H "Client-Id: 123456" ^
  -H "Api-Key: xxxxx" ^
  -H "Content-Type: application/json" ^
  -d "{\"offer_id\":[\"LOCAL-SKU-001\",\"LOCAL-SKU-002\"],\"confirm\":true}"
```

请求体：

```json
{
  "offer_id": ["LOCAL-SKU-001", "LOCAL-SKU-002"],
  "confirm": true
}
```

### 按 product_id 还原

```json
{
  "product_id": [137285792, 137285793],
  "confirm": true
}
```

### 按 sku 还原

```json
{
  "sku": [123456789, 123456790],
  "confirm": true
}
```

### 混合标识还原

```json
{
  "offer_id": ["LOCAL-SKU-001"],
  "product_id": [137285793],
  "sku": [123456790],
  "confirm": true
}
```

## 响应参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `request_id` | string | 本地服务生成的还原请求 ID，用于排查日志、批次和明细。 |
| `archive_task_id` | integer | 本地数据库中的归档工作流批次 ID，对应 `ozon_archive_tasks.id`。 |
| `status` | string | 批次状态：`success`、`partial`、`failed`、`skipped`。 |
| `total_count` | integer | 本次解析出的商品数量。 |
| `success_count` | integer | 成功还原数量。 |
| `failed_count` | integer | 失败数量。 |
| `skipped_count` | integer | 跳过数量，例如商品未找到或未归档。 |
| `precheck` | object | 还原前查询商品信息的 Ozon 原始响应。 |
| `unarchive_result` | object | 调用 Ozon 还原接口的结果。超过 100 个商品时会按 `chunks[]` 保存每批请求和响应。 |
| `confirm` | object | 还原后确认查询的 Ozon 原始响应。 |
| `items[]` | array | 单商品处理结果。 |
| `items[].offer_id` | string | 卖家系统商品货号。 |
| `items[].product_id` | integer | Ozon 商品 ID。 |
| `items[].sku` | integer | Ozon SKU。 |
| `items[].before_is_archived` | boolean | 操作前是否手动归档。 |
| `items[].before_is_autoarchived` | boolean | 操作前是否自动归档。 |
| `items[].after_is_archived` | boolean | 操作后是否手动归档。 |
| `items[].after_is_autoarchived` | boolean | 操作后是否自动归档。 |
| `items[].status` | string | 单商品状态：`success`、`failed`、`skipped`、`not_found`、`not_archived`。 |
| `items[].skip_reason` | string | 跳过原因。 |
| `items[].error_message` | string | 失败原因。 |

## 响应示例

### 部分成功

```json
{
  "request_id": "15d98c71-c60e-44aa-bb7a-0f1386e27284",
  "archive_task_id": 21,
  "status": "partial",
  "total_count": 3,
  "success_count": 1,
  "failed_count": 0,
  "skipped_count": 2,
  "precheck": {
    "items": [
      {
        "id": 137285792,
        "offer_id": "LOCAL-SKU-001",
        "is_archived": true,
        "is_autoarchived": false,
        "sources": [{"sku": 123456789}]
      },
      {
        "id": 137285793,
        "offer_id": "LOCAL-SKU-002",
        "is_archived": false,
        "is_autoarchived": false,
        "sources": [{"sku": 123456790}]
      }
    ]
  },
  "unarchive_result": {
    "chunks": [
      {
        "request": {
          "product_id": [137285792]
        },
        "response": {
          "result": true
        }
      }
    ]
  },
  "confirm": {
    "items": [
      {
        "id": 137285792,
        "offer_id": "LOCAL-SKU-001",
        "is_archived": false,
        "is_autoarchived": false,
        "sources": [{"sku": 123456789}]
      }
    ]
  },
  "items": [
    {
      "offer_id": "LOCAL-SKU-001",
      "product_id": 137285792,
      "sku": 123456789,
      "before_is_archived": true,
      "before_is_autoarchived": false,
      "after_is_archived": false,
      "after_is_autoarchived": false,
      "status": "success",
      "skip_reason": null,
      "error_message": null
    },
    {
      "offer_id": "LOCAL-SKU-002",
      "product_id": 137285793,
      "sku": 123456790,
      "before_is_archived": false,
      "before_is_autoarchived": false,
      "after_is_archived": false,
      "after_is_autoarchived": false,
      "status": "not_archived",
      "skip_reason": "商品未归档，无需还原",
      "error_message": null
    },
    {
      "offer_id": null,
      "product_id": null,
      "sku": null,
      "before_is_archived": null,
      "before_is_autoarchived": null,
      "after_is_archived": null,
      "after_is_autoarchived": null,
      "status": "not_found",
      "skip_reason": "商品信息查询未返回该标识",
      "error_message": null
    }
  ]
}
```

### 全部成功

```json
{
  "request_id": "c67af996-2454-4ad8-906b-92e6c686abcf",
  "archive_task_id": 22,
  "status": "success",
  "total_count": 1,
  "success_count": 1,
  "failed_count": 0,
  "skipped_count": 0,
  "precheck": {},
  "unarchive_result": {
    "chunks": [
      {
        "request": {
          "product_id": [137285792]
        },
        "response": {
          "result": true
        }
      }
    ]
  },
  "confirm": {},
  "items": [
    {
      "offer_id": "LOCAL-SKU-001",
      "product_id": 137285792,
      "sku": 123456789,
      "before_is_archived": true,
      "before_is_autoarchived": false,
      "after_is_archived": false,
      "after_is_autoarchived": false,
      "status": "success",
      "skip_reason": null,
      "error_message": null
    }
  ]
}
```

## 错误响应

当请求参数不合法时，FastAPI 会返回 `422`。例如没有传任何商品标识：

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body"],
      "msg": "Value error, offer_id、product_id、sku 至少传一种"
    }
  ]
}
```

当 Ozon API 返回错误时，本地服务会返回统一错误格式：

```json
{
  "success": false,
  "message": "Ozon API request failed",
  "detail": {
    "code": 7,
    "message": "restore quota is exceeded",
    "details": []
  }
}
```

常见错误原因：

- `Client-Id` 或 `Api-Key` 不正确。
- 商品不存在，单商品结果会返回 `not_found`。
- 商品未归档，单商品结果会返回 `not_archived`。
- 自动归档商品超过每天 10 件恢复限额。
- `product_id` 不是当前店铺下的商品。

## 底层接口

如果调用方不想使用整合入口，也可以自行拆步调用。

### 1. 查询商品信息

```http
POST /api/ozon/products/info/list
```

请求体：

```json
{
  "offer_id": ["LOCAL-SKU-001"]
}
```

关键字段：

| 字段 | 说明 |
| --- | --- |
| `items[].id` | Ozon `product_id`，还原接口要使用它。 |
| `items[].offer_id` | 卖家系统商品货号。 |
| `items[].sources[].sku` | Ozon SKU。 |
| `items[].is_archived` | 是否手动归档。 |
| `items[].is_autoarchived` | 是否自动归档。 |

### 2. 调用还原

```http
POST /api/ozon/proxy/v1/product/unarchive
```

请求体：

```json
{
  "product_id": [137285792]
}
```

响应体：

```json
{
  "result": true
}
```

### 3. 确认还原结果

```http
POST /api/ozon/products/info/list
```

请求体：

```json
{
  "product_id": ["137285792"]
}
```

确认响应中的：

```json
{
  "is_archived": false,
  "is_autoarchived": false
}
```

## 本地落库说明

调用 `POST /api/ozon/products/unarchive` 后，本地服务会写入或更新：

| 表 | 作用 |
| --- | --- |
| `ozon_archive_tasks` | `action_type='unarchive'` 的还原批次记录。 |
| `ozon_archive_task_items` | 单商品还原结果。 |
| `ozon_product_archive_history` | 商品归档状态变更历史。 |
| `ozon_products` | 更新商品归档状态为未归档。 |

建议已执行：

```bash
mysql --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u ozonservice -p < docs/ozon-api/database/archive-workflow.sql
mysql --default-character-set=utf8mb4 -h 127.0.0.1 -P 3306 -u ozonservice -p < docs/ozon-api/database/unarchive-workflow.sql
```
