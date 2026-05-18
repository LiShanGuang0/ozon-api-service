# 后端接口清单

本文档整理当前 FastAPI 服务已挂载的后端接口。服务入口见 `app/main.py`，主接口统一挂载在 `/api` 前缀下；另外根路径保留一个独立健康检查 `/health`。

## 通用约定

- 主业务接口前缀：`/api`
- `/api` 下 JSON 响应会被统一包装为：

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

- Ozon 业务接口认证 Header：
  - `Client-Id`
  - `Api-Key`
- 商户端查询接口认证 Header：
  - 优先读取 `X-Merchant-Client-Id`
  - 兼容读取 `Client-Id`
- App 激活码管理接口认证 Header：
  - `X-Admin-Token`

## 健康检查

| 方法 | 路径 | 说明 | 请求参数/Body | 返回 |
| --- | --- | --- | --- | --- |
| GET | `/health` | 根路径健康检查，不走 `/api` 响应包装 | 无 | `{ status, service }` |
| GET | `/api/health` | API 健康检查，走统一响应包装 | 无 | `{ status, service }` |

## Ozon 通用转发

| 方法 | 路径 | 说明 | 请求参数/Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/ozon/proxy/{endpoint}` | 通用 Ozon API 转发，将请求体原样转发到指定 Ozon endpoint，并记录调用日志 | Path：`endpoint`；Header：`Client-Id`, `Api-Key`；Body：任意 JSON | Ozon 原始响应对象 |

示例：`POST /api/ozon/proxy/v1/description-category/tree`

## Ozon 类目接口

| 方法 | 路径 | 说明 | 请求 Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/ozon/categories/tree` | 查询 Ozon 类目树，用于获取 `description_category_id` 和 `type_id` | `CategoryTreeRequest`，可为空；字段：`language` | Ozon `/v1/description-category/tree` 原始响应 |
| POST | `/api/ozon/categories/attributes` | 查询指定类目和类型下的属性、必填属性、字典属性等 | `CategoryAttributesRequest`：`description_category_id`, `type_id`, `language` | Ozon `/v1/description-category/attribute` 原始响应 |
| POST | `/api/ozon/categories/attribute-values` | 查询属性字典值 | `AttributeValuesRequest`：`description_category_id`, `type_id`, `attribute_id`, `limit`, `last_value_id`, `language` | Ozon `/v1/description-category/attribute/values` 原始响应 |
| POST | `/api/ozon/categories/attribute-values/search` | 按关键词搜索属性字典值 | `AttributeValuesSearchRequest`：`description_category_id`, `type_id`, `attribute_id`, `value`, `limit` | Ozon `/v1/description-category/attribute/values/search` 原始响应 |

## Ozon 商品接口

| 方法 | 路径 | 说明 | 请求 Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/ozon/product/info/limit` | 查询商品创建/更新额度 | 无 | Ozon `/v4/product/info/limit` 原始响应 |
| POST | `/api/ozon/products/list-with-attributes` | 查询 Ozon 商品列表后，再批量查询商品属性详情，并返回合并结果 | `ProductListWithAttributesRequest`：`filter`, `last_id`, `limit`, `attributes_limit` | `ProductListWithAttributesResponse`：`items[]`, `total`, `last_id`, `attribute_total`, `attribute_last_id`, `product_list`, `attributes_result` |
| POST | `/api/ozon/products/import` | 创建或更新商品；先查额度，再提交导入任务，并保存本地商品快照和任务信息 | `ProductImportRequest`：`items[]`；单次最多 100 个商品 | `ProductImportResponse`：`limit`, `import_result`, `task_id`, `credential_ref_saved` |
| POST | `/api/ozon/products/attributes/update` | 仅更新商品属性 | `ProductAttributesUpdateRequest`：`items[]`，每项需包含 `offer_id` 和 `attributes` | `ProductAttributesUpdateResponse`：`task_id`, `data` |
| POST | `/api/ozon/products/pictures/import` | 按 `offer_id` 上传或更新商品图片；会先解析 Ozon `product_id` | `ProductPicturesImportRequest`：`offer_id`, `images`, `images360`, `color_image` | Ozon `/v1/product/pictures/import` 原始响应 |
| POST | `/api/ozon/products/info/list` | 根据 `offer_id` 查询商品基础信息、状态、图片等 | `ProductInfoListRequest`：`offer_id[]`，最多 1000 个 | Ozon `/v3/product/info/list` 原始响应 |
| POST | `/api/ozon/products/info/attributes` | 查询商品已填写属性、尺寸、重量、图片等 | `ProductInfoAttributesRequest`：`offer_id` | Ozon `/v4/product/info/attributes` 原始响应 |

### `ProductListWithAttributesRequest` 字段

- `filter.offer_id`：按卖家货号过滤，最多 1000 个。
- `filter.product_id`：按 Ozon 商品 ID 过滤，最多 1000 个。
- `filter.visibility`：Ozon 商品可见性过滤条件。
- `last_id`：分页游标，首次查询传空字符串。
- `limit`：本次列表查询数量，默认 100，最大 1000。
- `attributes_limit`：详情查询数量，默认 1000，最大 1000。

`filter.offer_id` 和 `filter.product_id` 只能传其中一种。接口内部先调用 Ozon `/v3/product/list`，再用返回列表里的 `product_id` 优先调用 `/v4/product/info/attributes`；如果列表项没有 `product_id`，则回退使用 `offer_id` 查询详情。

请求示例：

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

### `ProductImportRequest.items[]` 常用字段

`offer_id`, `name`, `description_category_id`, `type_id`, `barcode`, `currency_code`, `price`, `old_price`, `vat`, `depth`, `width`, `height`, `dimension_unit`, `weight`, `weight_unit`, `images`, `primary_image`, `images360`, `color_image`, `pdf_list`, `attributes`, `complex_attributes`, `warehouse_id`, `stock`。

注意：该服务对外只允许用 `offer_id` 标识商品，请求里不允许传 `product_id` 或 `sku`。

## Ozon 导入任务接口

| 方法 | 路径 | 说明 | 请求参数 | 返回 |
| --- | --- | --- | --- | --- |
| GET | `/api/ozon/products/import-tasks/{task_id}` | 查询商品创建/更新任务状态，并回写本地数据库 | Path：`task_id`；Header：`Client-Id`, `Api-Key` | `ImportTaskStatusResponse`：`task_id`, `status`, `workflow_status`, `data` |

## Ozon 归档接口

| 方法 | 路径 | 说明 | 请求 Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/ozon/products/archive` | 按 `offer_id` 归档商品；内部先转换为 `product_id`，再调用 Ozon 归档接口，可选确认结果 | `ProductArchiveRequest`：`offer_id[]`, `confirm` | `ProductArchiveResponse`：`request_id`, `archive_task_id`, `status`, 统计字段、`precheck`, `archive_result`, `confirm`, `items[]` |
| POST | `/api/ozon/products/unarchive` | 按 `offer_id` 从归档还原商品；内部先转换为 `product_id`，再调用 Ozon 还原接口，可选确认结果 | `ProductUnarchiveRequest`：`offer_id[]`, `confirm` | `ProductUnarchiveResponse`：`request_id`, `archive_task_id`, `status`, 统计字段、`precheck`, `unarchive_result`, `confirm`, `items[]` |

归档和还原接口的 `offer_id[]` 至少 1 个，最多 1000 个。

## Ozon 库存接口

| 方法 | 路径 | 说明 | 请求 Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/ozon/warehouses/list` | 查询当前 `Client-Id` 下的仓库列表，并缓存到本地 | `WarehouseListRequest`：`cursor`, `limit`, `warehouse_ids[]` | Ozon `/v2/warehouse/list` 原始响应 |
| POST | `/api/ozon/products/stocks` | 直接转发设置单个商品库存 | `ProductsStocksRequest`：`offer_id`, `warehouse_id`, `stock` | Ozon `/v2/products/stocks` 原始响应 |
| POST | `/api/ozon/products/stocks/update` | 批量设置商品上架数量；内部校验仓库、查询商品、调用库存更新，并可选确认 | `ProductStockUpdateRequest`：`stocks[]`, `check_reserved`, `confirm` | `ProductStockUpdateResponse`：`request_id`, `stock_task_id`, `status`, 统计字段、各阶段原始响应、`items[]` |

`ProductStockUpdateRequest.stocks[]` 字段：`offer_id`, `warehouse_id`, `stock`。单次最多 100 个商品。

## 商户端接口

| 方法 | 路径 | 说明 | 请求参数/Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/merchant/bootstrap` | H5 首次进入时提交 Ozon 凭证，校验并初始化商户资料 | Body：`MerchantBootstrapRequest`：`client_id`, `api_key` | `MerchantBootstrapResponse`：`profile`, `initialized_from_ozon`, `credential_valid` |
| GET | `/api/merchant/profile` | 查询当前商户店铺信息 | Header：`X-Merchant-Client-Id` 或 `Client-Id` | `MerchantProfileResponse` |
| GET | `/api/merchant/dashboard` | 查询商户端工作台统计和最近推送流水 | Header：`X-Merchant-Client-Id` 或 `Client-Id` | `MerchantDashboardResponse` |
| GET | `/api/merchant/products` | 查询商户商品列表 | Query：`page`, `size`, `keyword`, `status`；Header：商户 Client-Id | `PageResponse` |
| GET | `/api/merchant/push-tasks` | 查询商户 Ozon 商品导入任务列表 | Query：`page`, `size`, `status`；Header：商户 Client-Id | `PageResponse` |
| GET | `/api/merchant/push-tasks/{task_id}` | 查询某个推送任务详情和单商品结果 | Path：`task_id`；Header：商户 Client-Id | `MerchantTaskDetailResponse`：`task`, `items[]` |
| GET | `/api/merchant/task-events` | 查询商户最新推送流水，可用于滚动加载 | Query：`limit`, `before_id`, `status`, `event_type`；Header：商户 Client-Id | `MerchantTaskEventsResponse`：`items[]`, `next_before_id`, `today_count` |
| POST | `/api/merchant/translate` | 翻译商品名称、Ozon 错误信息等动态文案 | Body：`TranslateRequest`：`texts[]`, `target_language`, `source_language` | `TranslateResponse`：`items[]` |

### 商户端常用查询默认值

- `/api/merchant/products`：`page=1`，`size=20`，`size` 范围 1 到 100。
- `/api/merchant/push-tasks`：`page=1`，`size=20`，`size` 范围 1 到 100。
- `/api/merchant/task-events`：`limit=30`，范围 1 到 100。

## App 激活接口

| 方法 | 路径 | 说明 | 请求参数/Body | 返回 |
| --- | --- | --- | --- | --- |
| POST | `/api/app-activations/codes` | 管理员为指定设备、Client-Id 和 Api-Key 生成激活码；Api-Key 只保存 SHA-256 指纹 | Header：`X-Admin-Token`；Body：`AppActivationCodeCreateRequest` | `AppActivationCodeCreateResponse` |
| GET | `/api/app-activations/codes` | 管理员查看激活码列表、设备绑定状态和有效期 | Header：`X-Admin-Token` | `AppActivationListResponse` |
| POST | `/api/app-activations/check` | App 启动时根据设备标识检查是否已绑定且未过期 | Body：`AppActivationCheckRequest`：`device_id`, `mac_address` | `AppActivationCheckResponse` |
| POST | `/api/app-activations/bind` | App 首次激活时绑定设备、Client-Id、Api-Key 和激活码 | Body：`AppActivationBindRequest`：`device_id`, `mac_address`, `client_id`, `api_key`, `activation_code` | `AppActivationBindResponse` |

### App 激活模型字段

- `AppActivationCodeCreateRequest`：`device_id`, `mac_address`, `client_id`, `api_key`, `activation_code`, `expires_at`, `valid_days`。
- `AppActivationCheckResponse`：`bound`, `expired`, `activation_required`, `status`, `reason`, `client_id`, `expires_at`。
- `AppActivationBindResponse`：`bound`, `client_id`, `expires_at`, `profile`。

## 已挂载接口数量

- 根路径健康检查：1 个
- `/api` 健康检查：1 个
- `/api/ozon` 相关接口：18 个
- `/api/merchant` 商户端接口：8 个
- `/api/app-activations` App 激活接口：4 个

总计：32 个已挂载后端接口。
