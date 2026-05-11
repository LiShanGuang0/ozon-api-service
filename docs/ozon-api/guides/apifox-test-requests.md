# Apifox 测试请求参数

本文用于在 Apifox 中模拟测试：

- 创建或更新商品
- 归档商品
- 从档案中还原商品
- 查询仓库
- 修改商品仓库数量

本文字段按当前运行服务实际返回的 `GET /openapi.json` 整理。创建、归档、库存更新都是写接口，请优先使用测试商品和测试仓库。

服务地址：

```text
http://127.0.0.1:8000
```

通用请求头：

| Header | 示例值 | 必填 | 说明 |
| --- | --- | --- | --- |
| `Client-Id` | `3915226` | 是 | Ozon Client-Id |
| `Api-Key` | `<你的 Ozon Api-Key>` | 是 | Ozon Api-Key |
| `Content-Type` | `application/json` | POST 请求必填 | JSON 请求体 |
| `Accept` | `*/*` | 否 | Apifox 默认即可 |

重要规则：

- 商品业务对外统一使用 `offer_id`。
- 请求参数不要传 `product_id` 或 `sku`，服务内部会按 `Client-Id + offer_id` 查询并转换。
- 类目相关 `language` 默认用 `DEFAULT`，即 Ozon 默认俄语；可选值：`DEFAULT`、`RU`、`EN`、`TR`、`ZH_HANS`。
- 类目树接口是 `POST /api/ozon/categories/tree`，不是 GET；URL 不要写成 `//api/...`。

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
| `code` | 业务响应码；成功为 `200`，失败通常为 HTTP 状态码，例如 `400`、`404`、`422` |
| `msg` | 响应消息；成功为 `success`，失败为错误说明 |
| `data` | 实际业务数据；本文下面的“关键返回字段”默认都在 `data` 内 |

## 1. 创建或更新商品

### 1.1 查询类目树

用于获取创建商品需要的 `description_category_id` 和 `type_id`。

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/categories/tree` |
| 转发 Ozon | `/v1/description-category/tree` |

Body：

```json
{
  "language": "DEFAULT"
}
```

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `language` | 否 | string | 默认 `DEFAULT`；可选 `DEFAULT`、`RU`、`EN`、`TR`、`ZH_HANS` |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `result[].description_category_id` | 创建商品用的类目 ID |
| `result[].children[].type_id` | 创建商品用的商品类型 ID |

笔记本电脑支架本次实际取值：

| 字段 | 值 |
| --- | --- |
| `description_category_id` | `17028922` |
| `type_id` | `99383` |
| 类目路径 | `Электроника > Кронштейны, держатели, подставки > Подставка для ноутбука` |

### 1.2 查询类目属性

用于确认该类目下哪些属性必填，以及属性 ID 是什么。

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/categories/attributes` |
| 转发 Ozon | `/v1/description-category/attribute` |

Body：

```json
{
  "description_category_id": 17028922,
  "type_id": 99383,
  "language": "DEFAULT"
}
```

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `description_category_id` | 是 | integer | 来自类目树 |
| `type_id` | 是 | integer | 来自类目树 |
| `language` | 否 | string | 默认 `DEFAULT` |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `result[].id` | 属性 ID，创建商品 `attributes[].id` 要用 |
| `result[].name` | 属性名称 |
| `result[].is_required` | 是否必填 |
| `result[].dictionary_id` | 是否有字典值；大于 0 时通常要查属性字典 |

### 1.3 查询属性字典值

用于获取 `dictionary_value_id`。品牌、类型、颜色等字典属性建议先查这个接口。

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/categories/attribute-values` |
| 转发 Ozon | `/v1/description-category/attribute/values` |

Body：

```json
{
  "description_category_id": 17028922,
  "type_id": 99383,
  "attribute_id": 8229,
  "limit": 2000,
  "last_value_id": 0,
  "language": "DEFAULT"
}
```

笔记本电脑支架的类型字典值本次实际取值：

| 字段 | 值 |
| --- | --- |
| `attribute_id` | `8229` |
| `dictionary_value_id` | `99383` |
| `value` | `Подставка для ноутбука` |

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `description_category_id` | 是 | integer | 类目 ID |
| `type_id` | 是 | integer | 商品类型 ID |
| `attribute_id` | 是 | integer | 属性 ID |
| `limit` | 否 | integer | 默认 `2000`，范围 1-2000 |
| `last_value_id` | 否 | integer | 默认 `0`；分页时用 |
| `language` | 否 | string | 默认 `DEFAULT` |

### 1.4 搜索属性字典值

如果字典值太多，用关键词搜索。

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/categories/attribute-values/search` |
| 转发 Ozon | `/v1/description-category/attribute/values/search` |

Body：

```json
{
  "description_category_id": 17028922,
  "type_id": 99383,
  "attribute_id": 85,
  "value": "Havit",
  "limit": 100
}
```

笔记本电脑支架的品牌字典值本次示例取值：

| 字段 | 值 |
| --- | --- |
| `attribute_id` | `85` |
| `dictionary_value_id` | `5064554` |
| `value` | `Havit` |

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `description_category_id` | 是 | integer | 类目 ID |
| `type_id` | 是 | integer | 商品类型 ID |
| `attribute_id` | 是 | integer | 属性 ID |
| `value` | 是 | string | 搜索关键词，至少 2 个字符 |
| `limit` | 否 | integer | 默认 `100`，范围 1-100 |

### 1.5 创建或更新商品

以下创建商品请求体以“笔记本电脑支架”为例，类目、必填属性、字典值来自实际调用上面 3 个接口后的结果。

实际查询结果：

| 来源接口 | 查询条件 | 取到的值 |
| --- | --- | --- |
| `/api/ozon/categories/tree` | 搜索“Подставка для ноутбука” | `description_category_id=17028922`，`type_id=99383` |
| `/api/ozon/categories/attributes` | `description_category_id=17028922`，`type_id=99383` | 必填属性：`9048` 型号名称、`8229` 类型、`85` 品牌 |
| `/api/ozon/categories/attribute-values` | `attribute_id=8229` | `dictionary_value_id=99383`，`value=Подставка для ноутбука` |
| `/api/ozon/categories/attribute-values/search` | `attribute_id=85`，`value=Havit` | `dictionary_value_id=5064554`，`value=Havit` |

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/products/import` |
| 转发 Ozon | 先查 `/v4/product/info/limit`，再提交 `/v3/product/import` |
| 是否写库 | 是；保存本地商品快照、导入任务、请求日志 |

Body 示例：

```json
{
  "items": [
    {
      "offer_id": "LAPTOP-STAND-001",
      "name": "Подставка для ноутбука Havit, алюминиевая, регулируемая",
      "description_category_id": 17028922,
      "type_id": 99383,
      "currency_code": "CNY",
      "price": "1000",
      "old_price": "1100",
      "vat": "0",
      "depth": 10,
      "width": 150,
      "height": 250,
      "dimension_unit": "mm",
      "weight": 100,
      "weight_unit": "g",
      "images": [
        "https://your-domain.com/images/laptop-stand-1.jpg"
      ],
      "primary_image": "https://your-domain.com/images/laptop-stand-1.jpg",
      "attributes": [
        {
          "complex_id": 0,
          "id": 9048,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "LAPTOP-STAND-HAVIT-ALU-01"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 8229,
          "values": [
            {
              "dictionary_value_id": 99383,
              "value": "Подставка для ноутбука"
            }
          ]
        },
        {
          "complex_id": 0,
          "id": 85,
          "values": [
            {
              "dictionary_value_id": 5064554,
              "value": "Havit"
            }
          ]
        }
      ],
      "complex_attributes": []
    }
  ]
}
```

注意：上面 `description_category_id`、`type_id`、`attributes[].id`、`dictionary_value_id` 是我通过当前接口实际查到的真实值；`offer_id`、图片 URL、价格、尺寸、重量需要替换成你的真实商品数据。图片 URL 必须是 Ozon 能公网访问的真实商品图片。

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `items` | 是 | array | 商品数组，最多 100 个 |
| `items[].offer_id` | 是 | string | 本地业务货号；同一个 `Client-Id` 下应唯一 |
| `items[].name` | 按类目要求 | string | 商品名称，最多 500 字符 |
| `items[].description_category_id` | 按类目要求 | integer | 来自类目树 |
| `items[].type_id` | 按类目要求 | integer | 来自类目树 |
| `items[].barcode` | 否 | string | 商品条码 |
| `items[].currency_code` | 是 | string | 必须与 Ozon 合同/个人中心币种一致；当前示例用 `CNY` |
| `items[].price` | 是 | string | 当前售价，字符串 |
| `items[].old_price` | 否 | string | 划线价，字符串 |
| `items[].vat` | 是 | string | 当前测试账号要求 `0` |
| `items[].depth` | 是 | integer | 包装深度/厚度，不要传 0 |
| `items[].width` | 是 | integer | 包装宽度，不要传 0 |
| `items[].height` | 是 | integer | 包装高度，不要传 0 |
| `items[].dimension_unit` | 是 | string | 常用 `mm`、`cm`、`in` |
| `items[].weight` | 是 | integer | 含包装重量，不要传 0 |
| `items[].weight_unit` | 是 | string | 常用 `g`、`kg`、`lb` |
| `items[].images` | 是 | array | 商品图片 URL，公共可访问 |
| `items[].primary_image` | 否 | string | 主图 URL |
| `items[].attributes` | 是 | array | 类目属性；必填属性来自属性接口 `is_required=true` |
| `items[].attributes[].id` | 是 | integer | 属性 ID |
| `items[].attributes[].complex_id` | 否 | integer | 普通属性传 `0` |
| `items[].attributes[].values[].dictionary_value_id` | 按属性类型 | integer | 字典值 ID；无字典属性通常传 `0` |
| `items[].attributes[].values[].value` | 按属性类型 | string/number/boolean | 属性值 |
| `items[].complex_attributes` | 否 | array | 复合属性 |

已覆盖的常见 Ozon 错误：

| 错误 code | 处理方式 |
| --- | --- |
| `currency_differs_from_contract` | `currency_code` 要改成账号合同/个人中心币种；当前测试示例使用 `CNY` |
| `vat_not_zero_banned_in_country` | `vat` 改成 `"0"` |
| `error_attribute_values_empty`，`attribute_id=9048` | 补充属性 `9048`，即“Название модели (для объединения в одну карточку)” |
| `desc_type_invalid_value_autoreplaced`，`attribute_id=8229` | “类型”属性用了已删除或无效值，重新调用属性字典接口取最新值 |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `task_id` | Ozon 导入异步任务 ID，下一步查询任务结果用 |

### 1.6 查询创建/更新任务结果

| 配置 | 值 |
| --- | --- |
| Method | `GET` |
| URL | `http://127.0.0.1:8000/api/ozon/products/import-tasks/{task_id}` |
| 转发 Ozon | `/v1/product/import/info` |
| 是否写库 | 是；回写任务状态、`product_id`、错误信息、本地商品标识 |

示例：

```text
http://127.0.0.1:8000/api/ozon/products/import-tasks/4399903997
```

Body：无。

路径参数：

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `task_id` | 是 | integer | `/api/ozon/products/import` 返回的任务 ID |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `task_id` | 任务 ID |
| `status` | 本地归一化状态，例如 `pending`、`imported`、`failed`、`partial` |
| `data.result.items[].offer_id` | 商品货号 |
| `data.result.items[].product_id` | Ozon 商品 ID，服务内部保存，不需要对外传 |
| `data.result.items[].errors[]` | Ozon 返回的错误或警告 |

## 2. 归档商品

归档商品只传 `offer_id`，不传 `product_id`。

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/products/archive` |
| 转发 Ozon | 先查 `/v3/product/info/list`，再调用 `/v1/product/archive` |
| 是否写库 | 是；保存归档任务、商品归档状态、请求日志 |

Body：

```json
{
  "offer_id": [
    "LOCAL-SKU-001"
  ],
  "confirm": true
}
```

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `offer_id` | 是 | array[string] | 要归档的本地商品货号列表，至少 1 个 |
| `confirm` | 否 | boolean | 默认 `true`；归档后再次查询确认 `is_archived=true` |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `request_id` | 本地请求 ID |
| `archive_task_id` | 本地归档批次 ID |
| `status` | `success`、`partial`、`failed`、`skipped` |
| `items[].offer_id` | 商品货号 |
| `items[].product_id` | 服务内部转换得到的 Ozon 商品 ID |
| `items[].status` | 单商品处理状态 |
| `items[].error_message` | 失败原因 |

## 3. 从档案中还原商品

还原商品只传 `offer_id`，不传 `product_id`。

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/products/unarchive` |
| 转发 Ozon | 先查 `/v3/product/info/list`，再调用 `/v1/product/unarchive` |
| 是否写库 | 是；保存还原任务、商品归档状态、请求日志 |

Body：

```json
{
  "offer_id": [
    "LOCAL-SKU-001"
  ],
  "confirm": true
}
```

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `offer_id` | 是 | array[string] | 要从档案中还原的本地商品货号列表，至少 1 个，最多 1000 个 |
| `confirm` | 否 | boolean | 默认 `true`；还原后再次查询确认 `is_archived=false`、`is_autoarchived=false` |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `request_id` | 本地请求 ID |
| `archive_task_id` | 本地归档工作流批次 ID |
| `status` | `success`、`partial`、`failed`、`skipped` |
| `items[].offer_id` | 商品货号 |
| `items[].product_id` | 服务内部转换得到的 Ozon 商品 ID |
| `items[].status` | 单商品处理状态：`success`、`failed`、`skipped`、`not_found`、`not_archived` |
| `items[].skip_reason` | 跳过原因 |
| `items[].error_message` | 失败原因 |

## 4. 修改商品仓库数量

推荐 Apifox 测试顺序：

1. 先查询仓库列表，拿到 `warehouse_id`。
2. 调用库存更新接口设置库存。

### 4.1 查询仓库列表

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/warehouses/list` |
| 转发 Ozon | `/v2/warehouse/list` |
| 是否写库 | 是；缓存到 `ozon_warehouses` |

Body：

```json
{
  "cursor": "",
  "limit": 200,
  "warehouse_ids": []
}
```

请求字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `cursor` | 否 | string | 默认空字符串；下一页用响应里的 `cursor` |
| `limit` | 否 | integer | 默认 `200`，范围 1-200 |
| `warehouse_ids` | 否 | array[integer/string] | 指定仓库 ID 过滤，最多 200 个；查全部传空数组 |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `warehouses[].warehouse_id` | 更新库存要用的仓库 ID |
| `warehouses[].name` | 仓库名称 |
| `warehouses[].status` | 仓库状态 |
| `warehouses[].is_rfbs` | 是否 rFBS 仓库 |
| `has_next` | 是否还有下一页 |
| `cursor` | 下一页游标 |

### 4.2 修改商品仓库库存

| 配置 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/ozon/products/stocks/update` |
| 转发 Ozon | 先查 `/v2/warehouse/list`、`/v3/product/info/list`，再调用 `/v2/products/stocks`；不再调用 `/v1/product/info/stocks-by-warehouse/fbs` |
| 是否写库 | 是；保存库存更新任务、明细、库存快照、请求日志 |

Body：

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

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `stocks` | 是 | array | 库存更新列表，1-100 个 |
| `stocks[].offer_id` | 是 | string | 本地商品货号 |
| `stocks[].warehouse_id` | 是 | integer | 仓库 ID，来自 `/api/ozon/warehouses/list` |
| `stocks[].stock` | 是 | integer | 要设置的可售库存，不能小于 0 |
| `check_reserved` | 否 | boolean | 兼容旧参数，当前流程不再查询预留库存，建议传 `false` |
| `confirm` | 否 | boolean | 默认 `true`；更新后通过 `/v4/product/info/stocks` 做商品级确认 |

关键返回字段：

| 字段 | 说明 |
| --- | --- |
| `stock_task_id` | 本地库存更新任务 ID |
| `status` | `success`、`partial`、`failed` |
| `success_count` | 成功数量 |
| `failed_count` | 失败数量 |
| `items[].offer_id` | 商品货号 |
| `items[].warehouse_id` | 仓库 ID |
| `items[].status` | 单条处理状态 |
| `items[].present` | 当前更新流程不再查仓库维度库存，通常为 `null` |
| `items[].reserved` | 当前更新流程不再查仓库维度预留，通常为 `null` |
| `items[].error_message` | 失败原因 |

## 5. Apifox 快速检查

创建商品最小链路：

1. `POST /api/ozon/categories/tree`
2. `POST /api/ozon/categories/attributes`
3. 按需要调用 `POST /api/ozon/categories/attribute-values` 或 `/search`
4. `POST /api/ozon/products/import`
5. `GET /api/ozon/products/import-tasks/{task_id}`

归档商品最小链路：

1. `POST /api/ozon/products/archive`

从档案中还原商品最小链路：

1. `POST /api/ozon/products/unarchive`

修改库存最小链路：

1. `POST /api/ozon/warehouses/list`
2. `POST /api/ozon/products/stocks/update`
