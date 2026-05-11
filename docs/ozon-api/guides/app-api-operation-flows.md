# APP 接口调用流程

本文面向外部调用方，说明三类常用业务该调用哪些本地接口、请求参数是什么、关键响应看什么。

通用请求头：

| Header | 必填 | 说明 |
| --- | --- | --- |
| `Client-Id` | 是 | Ozon 用户识别号，也是本地数据隔离字段 |
| `Api-Key` | 是 | Ozon API 密钥 |
| `Content-Type` | 是 | `application/json` |

当前对外商品操作统一使用 `Client-Id + offer_id`。调用方不需要传 `product_id` 或 `sku`。

类目、属性、属性值相关接口的 `language` 默认使用 `DEFAULT`，Ozon 会按默认俄语返回；也可以显式传 `RU`、`EN`、`TR`、`ZH_HANS`。

下文所有接口都需要携带以上请求头。

```http
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

统一响应格式：

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

说明：

| 字段 | 说明 |
| --- | --- |
| `code` | 业务响应码；成功为 `200`，失败通常为 HTTP 状态码 |
| `msg` | 响应消息；成功为 `success`，失败为错误说明 |
| `data` | 实际业务数据；下文“关键响应”字段默认都在 `data` 内 |

## 1. 创建或更新商品

### 调用顺序

| 步骤 | 接口 | 作用 |
| --- | --- | --- |
| 1 | `POST /api/ozon/categories/tree` | 查询类目树，获取 `description_category_id` 和 `type_id` |
| 2 | `POST /api/ozon/categories/attributes` | 查询该类目需要填写哪些属性 |
| 3 | `POST /api/ozon/categories/attribute-values` 或 `/attribute-values/search` | 字典属性需要查询可用字典值 |
| 4 | `POST /api/ozon/product/info/limit` | 可选，查询创建/更新额度 |
| 5 | `POST /api/ozon/products/import` | 创建或更新商品 |
| 6 | `GET /api/ozon/products/import-tasks/{task_id}` | 查询 Ozon 异步任务结果，并回写本地商品状态 |

### 查询类目树

```http
POST /api/ozon/categories/tree
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "language": "DEFAULT"
}
```

关键返回值：

| 字段 | 说明 |
| --- | --- |
| `result[].description_category_id` | 创建商品需要的类目 ID |
| `result[].type_id` | 创建商品需要的商品类型 ID |

### 查询类目属性

```http
POST /api/ozon/categories/attributes
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "description_category_id": 17028922,
  "type_id": 91565,
  "language": "DEFAULT"
}
```

关键返回值：

| 字段 | 说明 |
| --- | --- |
| `result[].id` | 属性 ID，用于商品 `attributes[].id` |
| `result[].is_required` | 是否必填 |
| `result[].dictionary_id` | 大于 0 时通常需要查询字典值 |

### 查询属性字典值

```http
POST /api/ozon/categories/attribute-values
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "description_category_id": 17028922,
  "type_id": 91565,
  "attribute_id": 85,
  "limit": 2000,
  "last_value_id": 0,
  "language": "DEFAULT"
}
```

也可以搜索：

```http
POST /api/ozon/categories/attribute-values/search
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

```json
{
  "description_category_id": 17028922,
  "type_id": 91565,
  "attribute_id": 85,
  "value": "Samsung",
  "limit": 100
}
```

### 创建或更新商品

```http
POST /api/ozon/products/import
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数示例：

```json
{
  "items": [
    {
      "offer_id": "LOCAL-SKU-001",
      "name": "商品名称",
      "description_category_id": 17028922,
      "type_id": 91565,
      "barcode": "112772873170",
      "currency_code": "RUB",
      "price": "1000",
      "old_price": "1100",
      "vat": "0.1",
      "depth": 10,
      "width": 150,
      "height": 250,
      "dimension_unit": "mm",
      "weight": 100,
      "weight_unit": "g",
      "images": ["https://example.com/image-1.jpg"],
      "primary_image": "https://example.com/image-1.jpg",
      "attributes": [
        {
          "complex_id": 0,
          "id": 85,
          "values": [
            {
              "dictionary_value_id": 5060050,
              "value": "Samsung"
            }
          ]
        }
      ],
      "complex_attributes": []
    }
  ]
}
```

主要请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `items` | 是 | 商品数组，最多 100 个 |
| `items[].offer_id` | 是 | 业务商品唯一标识，同一 `Client-Id` 下唯一 |
| `items[].name` | 否 | 商品名称 |
| `items[].description_category_id` | 通常必填 | 类目 ID，来自类目树 |
| `items[].type_id` | 通常必填 | 商品类型 ID，来自类目树 |
| `items[].price` | 通常必填 | 当前售价，字符串 |
| `items[].old_price` | 否 | 划线价，字符串 |
| `items[].vat` | 否 | 增值税税率 |
| `items[].depth/width/height` | 通常必填 | 包装尺寸 |
| `items[].dimension_unit` | 通常必填 | 尺寸单位 |
| `items[].weight` | 通常必填 | 包装重量 |
| `items[].weight_unit` | 通常必填 | 重量单位 |
| `items[].images` | 否 | 图片 URL 列表 |
| `items[].attributes` | 按类目要求 | 商品属性 |

关键响应：

| 字段 | 说明 |
| --- | --- |
| `task_id` | Ozon 异步任务 ID |
| `import_result` | Ozon 创建/更新原始响应 |
| `credential_ref_saved` | 是否已保存短期凭证用于轮询 |

### 查询创建结果

```http
GET /api/ozon/products/import-tasks/{task_id}
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
```

请求参数：

| 参数 | 位置 | 说明 |
| --- | --- | --- |
| `task_id` | path | 上一步返回的 Ozon 异步任务 ID |

关键响应：

| 字段 | 说明 |
| --- | --- |
| `status` | `pending`、`imported`、`failed`、`skipped`、`partial` |
| `data` | Ozon `/v1/product/import/info` 原始响应 |

本地会把结果回写到：

| 表 | 写入内容 |
| --- | --- |
| `ozon_products` | `product_id`、同步状态、错误信息、响应快照 |
| `ozon_import_tasks` | 任务状态、结果 payload |
| `ozon_import_task_items` | 单商品任务结果 |

## 2. 归档商品 / 从档案中还原商品

### 调用顺序

| 步骤 | 接口 | 作用 |
| --- | --- | --- |
| 1 | `POST /api/ozon/products/archive` | 按 `offer_id` 归档商品 |
| 2 | `POST /api/ozon/products/unarchive` | 按 `offer_id` 从档案中还原商品 |

归档和还原接口都已经整合了前置查询、过滤、分批调用和确认逻辑。调用方不需要先查 `product_id`。

### 归档商品

```http
POST /api/ozon/products/archive
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "offer_id": ["LOCAL-SKU-001", "LOCAL-SKU-002"],
  "confirm": true
}
```

请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `offer_id` | 是 | 要归档的商品货号列表，最多 1000 个 |
| `confirm` | 否 | 是否归档后再次查询确认，默认 `true` |

内部调用：

| 顺序 | Ozon API | 作用 |
| --- | --- | --- |
| 1 | `/v3/product/info/list` | 按 `offer_id` 查询商品，解析 `product_id` 和归档状态 |
| 2 | `/v1/product/archive` | 按 `product_id` 分批归档，每批最多 100 个 |
| 3 | `/v3/product/info/list` | 如果 `confirm=true`，再次查询确认 `is_archived=true` |

关键响应：

| 字段 | 说明 |
| --- | --- |
| `request_id` | 本地请求 ID |
| `archive_task_id` | 本地归档批次 ID |
| `status` | `success`、`partial`、`failed`、`skipped` |
| `success_count` | 成功数量 |
| `failed_count` | 失败数量 |
| `skipped_count` | 跳过数量 |
| `items[].status` | 单商品状态：`success`、`failed`、`skipped`、`not_found`、`already_archived` |
| `items[].skip_reason` | 跳过原因 |
| `items[].error_message` | 失败原因 |

本地会写入：

| 表 | 写入内容 |
| --- | --- |
| `ozon_archive_tasks` | 归档批次、请求参数、Ozon 响应、数量统计 |
| `ozon_archive_task_items` | 单商品归档结果 |
| `ozon_products` | 商品归档状态 |
| `ozon_product_archive_history` | 商品归档状态变更历史 |

### 从档案中还原商品

```http
POST /api/ozon/products/unarchive
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "offer_id": ["LOCAL-SKU-001", "LOCAL-SKU-002"],
  "confirm": true
}
```

请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `offer_id` | 是 | 要从档案中还原的商品货号列表，最多 1000 个 |
| `confirm` | 否 | 是否还原后再次查询确认，默认 `true` |

内部调用：

| 顺序 | Ozon API | 作用 |
| --- | --- | --- |
| 1 | `/v3/product/info/list` | 按 `offer_id` 查询商品，解析 `product_id` 和归档状态 |
| 2 | `/v1/product/unarchive` | 按 `product_id` 分批从档案中还原，每批最多 100 个 |
| 3 | `/v3/product/info/list` | 如果 `confirm=true`，再次查询确认 `is_archived=false`、`is_autoarchived=false` |

关键响应：

| 字段 | 说明 |
| --- | --- |
| `request_id` | 本地请求 ID |
| `archive_task_id` | 本地归档工作流批次 ID |
| `status` | `success`、`partial`、`failed`、`skipped` |
| `success_count` | 成功数量 |
| `failed_count` | 失败数量 |
| `skipped_count` | 跳过数量 |
| `items[].status` | 单商品状态：`success`、`failed`、`skipped`、`not_found`、`not_archived` |
| `items[].skip_reason` | 跳过原因 |
| `items[].error_message` | 失败原因 |

本地会写入：

| 表 | 写入内容 |
| --- | --- |
| `ozon_archive_tasks` | 还原批次、请求参数、Ozon 响应、数量统计 |
| `ozon_archive_task_items` | 单商品还原结果 |
| `ozon_products` | 商品归档状态 |
| `ozon_product_archive_history` | 商品归档状态变更历史 |

## 3. 修改商品仓库数量

### 调用顺序

| 步骤 | 接口 | 作用 |
| --- | --- | --- |
| 1 | `POST /api/ozon/warehouses/list` | 查询可用仓库，获取 `warehouse_id` |
| 2 | `POST /api/ozon/products/stocks/update` | 设置商品在指定仓库的可售库存 |

### 查询仓库列表

```http
POST /api/ozon/warehouses/list
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "cursor": "",
  "limit": 200,
  "warehouse_ids": []
}
```

请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `cursor` | 否 | 分页游标，首次请求留空 |
| `limit` | 否 | 返回数量，最大 200 |
| `warehouse_ids` | 否 | 按仓库 ID 过滤，最多 200 个 |

关键响应：

| 字段 | 说明 |
| --- | --- |
| `warehouses[].warehouse_id` | 库存更新需要的仓库 ID |
| `warehouses[].name` | 仓库名称 |
| `warehouses[].status` | 仓库状态 |
| `warehouses[].is_rfbs` | 是否 rFBS 仓库 |
| `warehouses[].is_kgt` | 是否支持大件 |
| `has_next` | 是否还有下一页 |
| `cursor` | 下一页游标 |

本地会更新 `ozon_warehouses`。

### 修改仓库库存

```http
POST /api/ozon/products/stocks/update
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

请求参数：

```json
{
  "stocks": [
    {
      "offer_id": "LOCAL-SKU-001",
      "warehouse_id": 20605650762000,
      "stock": 10
    }
  ],
  "check_reserved": false,
  "confirm": true
}
```

请求字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `stocks` | 是 | 库存更新列表，1 到 100 个 |
| `stocks[].offer_id` | 是 | 商品货号 |
| `stocks[].warehouse_id` | 是 | 仓库 ID，来自 `/api/ozon/warehouses/list` |
| `stocks[].stock` | 是 | 要设置的可售库存数量，不能小于 0 |
| `check_reserved` | 否 | 兼容旧参数，当前流程不再查询仓库维度预留库存，建议传 `false` |
| `confirm` | 否 | 是否更新后通过 `/v4/product/info/stocks` 做商品级确认，默认 `true` |

内部调用：

| 顺序 | Ozon API | 作用 |
| --- | --- | --- |
| 1 | `/v2/warehouse/list` | 校验仓库是否存在 |
| 2 | `/v3/product/info/list` | 按 `offer_id` 查询商品，解析 SKU 和 product_id |
| 3 | `/v2/products/stocks` | 设置可售库存 |
| 4 | `/v4/product/info/stocks` | 如果 `confirm=true`，做商品级库存确认 |

关键响应：

| 字段 | 说明 |
| --- | --- |
| `request_id` | 本地库存更新请求 ID |
| `stock_task_id` | 本地库存更新批次 ID |
| `status` | `success`、`partial`、`failed` |
| `success_count` | 成功数量 |
| `failed_count` | 失败数量 |
| `items[].status` | 单商品状态：`success` 或 `failed` |
| `items[].requested_stock` | 本次请求设置的可售库存 |
| `items[].present` | 当前流程不再查仓库维度库存，通常为 `null` |
| `items[].reserved` | 当前流程不再查仓库维度预留，通常为 `null` |
| `items[].error_message` | 失败原因 |

本地会写入：

| 表 | 写入内容 |
| --- | --- |
| `ozon_stock_update_tasks` | 库存更新批次 |
| `ozon_stock_update_task_items` | 单商品库存更新结果 |
| `ozon_product_stocks` | 商品仓库库存快照 |
| `ozon_warehouses` | 仓库缓存 |

