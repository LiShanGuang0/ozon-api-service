# 查询商品列表并获取属性详情接口文档

## 接口概述

该接口用于查询 Ozon 商品列表，并自动补充商品属性详情。

服务内部会按顺序调用：

1. Ozon `/v3/product/list`：获取商品列表。
2. Ozon `/v4/product/info/attributes`：使用列表返回的 `product_id` 或 `offer_id` 获取商品属性、尺寸、重量、图片等详情。

最终返回本服务合并后的商品列表，同时保留两次 Ozon 原始响应，方便排查问题。

## 请求信息

| 项目 | 内容 |
| --- | --- |
| Method | `POST` |
| Path | `/api/ozon/products/list-with-attributes` |
| Content-Type | `application/json` |

## Header

| Header | 必填 | 说明 |
| --- | --- | --- |
| `Client-Id` | 是 | Ozon Seller API Client-Id |
| `Api-Key` | 是 | Ozon Seller API Api-Key |

## Request Body

| 字段 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `filter` | object | 否 | `{}` | `/v3/product/list` 查询过滤条件 |
| `filter.offer_id` | string[] | 否 | `[]` | 按卖家货号过滤，最多 1000 个 |
| `filter.product_id` | array | 否 | `[]` | 按 Ozon 商品 ID 过滤，最多 1000 个 |
| `filter.visibility` | string | 否 | `null` | Ozon 商品可见性过滤条件 |
| `last_id` | string | 否 | `""` | `/v3/product/list` 分页游标，首次查询传空字符串 |
| `limit` | integer | 否 | `100` | 本次列表查询数量，范围 1 到 1000 |
| `attributes_limit` | integer | 否 | `1000` | 详情查询数量，范围 1 到 1000 |

限制：

- `filter.offer_id` 和 `filter.product_id` 只能传其中一种。
- 如果 `filter.offer_id` 和 `filter.product_id` 都不传，则按 Ozon `/v3/product/list` 的普通分页逻辑查询。

## 请求示例

### 查询第一页商品

```json
{
  "filter": {
    "visibility": "ALL"
  },
  "last_id": "",
  "limit": 100,
  "attributes_limit": 1000
}
```

### 按 offer_id 查询

```json
{
  "filter": {
    "offer_id": ["LOCAL-SKU-001", "LOCAL-SKU-002"]
  },
  "last_id": "",
  "limit": 100,
  "attributes_limit": 1000
}
```

## Response Body

`/api` 下响应会被统一包装：

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

`data` 字段结构如下：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `items` | array | 合并后的商品列表和属性详情 |
| `items[].product_id` | integer/null | Ozon 商品 ID |
| `items[].offer_id` | string/null | 卖家系统商品货号 |
| `items[].list_item` | object | `/v3/product/list` 返回的单个商品列表项 |
| `items[].attributes` | object/null | `/v4/product/info/attributes` 返回的单个商品详情项；未匹配到时为 `null` |
| `total` | integer/null | `/v3/product/list` 返回的商品总数 |
| `last_id` | string | `/v3/product/list` 返回的下一页游标 |
| `attribute_total` | integer/string/null | `/v4/product/info/attributes` 返回的详情总数 |
| `attribute_last_id` | string | `/v4/product/info/attributes` 返回的详情下一页游标 |
| `product_list` | object | Ozon `/v3/product/list` 原始响应 |
| `attributes_result` | object | Ozon `/v4/product/info/attributes` 原始响应 |

## 响应示例

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "items": [
      {
        "product_id": 123456789,
        "offer_id": "LOCAL-SKU-001",
        "list_item": {
          "product_id": 123456789,
          "offer_id": "LOCAL-SKU-001",
          "archived": false,
          "has_fbo_stocks": false,
          "has_fbs_stocks": true
        },
        "attributes": {
          "id": 123456789,
          "offer_id": "LOCAL-SKU-001",
          "name": "商品名称",
          "description_category_id": 17028922,
          "type_id": 91565,
          "attributes": [],
          "complex_attributes": [],
          "images": [],
          "height": 250,
          "width": 150,
          "depth": 10,
          "dimension_unit": "mm",
          "weight": 100,
          "weight_unit": "g"
        }
      }
    ],
    "total": 1,
    "last_id": "",
    "attribute_total": 1,
    "attribute_last_id": "",
    "product_list": {
      "result": {
        "items": [],
        "total": 1,
        "last_id": ""
      }
    },
    "attributes_result": {
      "result": []
    }
  }
}
```

## 内部处理逻辑

1. 使用请求体中的 `filter`、`last_id`、`limit` 组装 Ozon `/v3/product/list` 请求。
2. 从商品列表中提取商品标识：
   - 优先使用 `product_id`。
   - 如果没有 `product_id`，则使用 `offer_id`。
3. 调用 Ozon `/v4/product/info/attributes` 获取详情。
4. 按 `product_id` 优先匹配详情，匹配不到时按 `offer_id` 匹配。
5. 返回合并后的 `items[]`，并附带 `product_list` 和 `attributes_result` 原始响应。

## 常见错误

| HTTP 状态码 | 场景 |
| --- | --- |
| `400` | 缺少 `Client-Id` 或 `Api-Key` Header |
| `422` | 请求体参数校验失败，例如 `limit` 超过 1000，或同时传了 `filter.offer_id` 和 `filter.product_id` |
| `4xx/5xx` | Ozon API 返回错误时，本服务会透传对应状态和 Ozon 错误详情 |

