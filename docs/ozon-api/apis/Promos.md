# Promos

接口数量：8

## 接口列表

- [活动清单](#活动清单) - `GET /v1/actions`
- [可用的促销商品清单](#可用的促销商品清单) - `POST /v1/actions/candidates`
- [参与 活动的商品列表](#参与-活动的商品列表) - `POST /v1/actions/products`
- [在促销活动中增加一个商品](#在促销活动中增加一个商品) - `POST /v1/actions/products/activate`
- [从活动中删除商品](#从活动中删除商品) - `POST /v1/actions/products/deactivate`
- [申请折扣列表](#申请折扣列表) - `POST /v1/actions/discounts-task/list`
- [同意折扣申请](#同意折扣申请) - `POST /v1/actions/discounts-task/approve`
- [取消折扣申请](#取消折扣申请) - `POST /v1/actions/discounts-task/decline`

## 活动清单

### 接口说明

用于获取可参与的 Ozon 促销活动列表。
[了解更多关于 Ozon 促销活动的信息](https://docs.ozon.ru/global/zh/promotion/big-promotions/rasprodazha/)

### 接口标题

活动清单

### 接口地址

`GET https://api-seller.ozon.ru/v1/actions`

### 请求参数

暂无参数。


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | GetSellerActionsV1ResponseAction[] | 请求结果。 |
| result[] | GetSellerActionsV1ResponseAction[] | 请求结果。 |
| result[].id | number | 活动识别号。 |
| result[].title | string | 活动名称。 |
| result[].action_type | string | 活动类型。 |
| result[].description | string | 活动描述。 |
| result[].date_start | string | 活动开始日期。 |
| result[].date_end | string | 活动结束日期。 |
| result[].freeze_date | string | 活动暂停的日期。<br>如果该空白被填写，卖家就不能提高价格，改变商品清单或减少促销活动的单位数量。<br>卖方可以降低价格，增加促销的单位数量。 |
| result[].potential_products_count | number | 可供活动的商品数量。 |
| result[].participating_products_count | number | 参加促销的商品数量。 |
| result[].is_participating | boolean | 无论你是否参加这项活动。 |
| result[].is_voucher_action | boolean | 此迹象表明买家需要促销代码才能参加。 |
| result[].banned_products_count | number | 被封商品数量。 |
| result[].with_targeting | boolean | 此迹象表明该活动是与目标受众一起进行的。 |
| result[].order_amount | number | 预定金额。 |
| result[].discount_type | string | 折扣类型。 |
| result[].discount_value | number | 折扣力度。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

```json
{
  "result": [
    {
      "id": 71342,
      "title": "test voucher #2",
      "date_start": "2021-11-22T09:46:38Z",
      "date_end": "2021-11-30T20:59:59Z",
      "potential_products_count": 0,
      "is_participating": true,
      "participating_products_count": 5,
      "description": "",
      "action_type": "DISCOUNT",
      "banned_products_count": 0,
      "with_targeting": false,
      "discount_type": "UNKNOWN",
      "discount_value": 0,
      "order_amount": 0,
      "freeze_date": "",
      "is_voucher_action": true
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998342.md

---

## 可用的促销商品清单

### 接口说明

通过识别号获取可参与促销活动的商品清单的方法。
自2025年5月5日起，offset分页参数将被关闭。请切换到 last_id 参数。

### 接口标题

可用的促销商品清单

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/candidates`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | seller_apiGetSellerProductV1Request | 否 | 请求体。 |
| action_id | body | number | 否 | 活动识别号。可以使用方法 [/v1/actions](#operation/Promos)获取。 |
| limit | body | number | 否 | 每页的答复数量。在默认情况下 — 100。 |
| offset | body | number | 否 | 答案中要跳过的元素的数量。例如，如果`offset=10`，答案将从找到的第11个元素开始。 |
| last_id | body | number | 否 | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | seller_apiGetSellerProductV1ResponseResult | - |
| result.products | seller_apiProduct[] | 商品清单。 |
| result.products[] | seller_apiProduct[] | 商品清单。 |
| result.products[].id | number | 商品识别号。 |
| result.products[].price | number | 不含折扣的商品的当前价格。 |
| result.products[].action_price | number | 促销价格。 |
| result.products[].alert_max_action_price_failed | boolean | 如果商品价格高于建议价，则为`true`。商品被标记为红色，可能会被排除在促销活动之外。 |
| result.products[].alert_max_action_price | number | 促销商品建议价格。 |
| result.products[].max_action_price | number | 可能的最高促销价格。 |
| result.products[].add_mode | string | 添加到促销中的商品类型：自动或由卖家手动添加。 |
| result.products[].min_stock | number | 库存折扣促销中的最小商品数。 |
| result.products[].stock | number | 《库存折扣》促销中的商品单位数量。 |
| result.total | number | 可用于活动的商品总数。 |
| result.last_id | number | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。<br>要检索以下数值，请从上一个查询的响应中指定`last_id`。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

```json
{
  "result": {
    "products": [
      {
        "id": 226,
        "price": 250,
        "action_price": 0,
        "alert_max_action_price_failed": true,
        "alert_max_action_price": 31,
        "max_action_price": 175,
        "add_mode": "NOT_SET",
        "stock": 0,
        "min_stock": 0
      },
      {
        "id": 1366,
        "price": 2300,
        "action_price": 630,
        "alert_max_action_price_failed": true,
        "alert_max_action_price": 31,
        "max_action_price": 770,
        "add_mode": "MANUAL",
        "stock": 0,
        "min_stock": 0
      }
    ],
    "total": 2
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998343.md

---

## 参与 活动的商品列表

### 接口说明

一种按识别号检索参加促销活动的商品清单的方法。
自2025年5月5日起，offset分页参数将被关闭。请切换到 last_id 参数。

### 接口标题

参与 活动的商品列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/products`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | seller_apiGetSellerProductV1Request | 否 | 请求体。 |
| action_id | body | number | 否 | 活动识别号。可以使用方法 [/v1/actions](#operation/Promos)获取。 |
| limit | body | number | 否 | 每页的答复数量。在默认情况下 — 100。 |
| offset | body | number | 否 | 答案中要跳过的元素的数量。例如，如果`offset=10`，答案将从找到的第11个元素开始。 |
| last_id | body | number | 否 | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | seller_apiGetSellerProductV1ResponseResult | - |
| result.products | seller_apiProduct[] | 商品清单。 |
| result.products[] | seller_apiProduct[] | 商品清单。 |
| result.products[].id | number | 商品识别号。 |
| result.products[].price | number | 不含折扣的商品的当前价格。 |
| result.products[].action_price | number | 促销价格。 |
| result.products[].alert_max_action_price_failed | boolean | 如果商品价格高于建议价，则为`true`。商品被标记为红色，可能会被排除在促销活动之外。 |
| result.products[].alert_max_action_price | number | 促销商品建议价格。 |
| result.products[].max_action_price | number | 可能的最高促销价格。 |
| result.products[].add_mode | string | 添加到促销中的商品类型：自动或由卖家手动添加。 |
| result.products[].min_stock | number | 库存折扣促销中的最小商品数。 |
| result.products[].stock | number | 《库存折扣》促销中的商品单位数量。 |
| result.total | number | 可用于活动的商品总数。 |
| result.last_id | number | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。<br>要检索以下数值，请从上一个查询的响应中指定`last_id`。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

```json
{
  "result": {
    "products": [
      {
        "id": 28745,
        "price": 99,
        "action_price": 50,
        "alert_max_action_price_failed": true,
        "alert_max_action_price": 31,
        "max_action_price": 32,
        "add_mode": "MANUAL",
        "stock": 20,
        "min_stock": 0
      }
    ],
    "total": 263,
    "last_id": "bnVсbA=="
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998344.md

---

## 在促销活动中增加一个商品

### 接口说明

一种向现有促销活动添加商品的方法。

### 接口标题

在促销活动中增加一个商品

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/products/activate`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | seller_apiActivateProductV1Request | 否 | 请求体。 |
| action_id | body | number | 是 | 活动识别号。可以使用方法 [/v1/actions](#operation/Promos)获取。 |
| products | body | seller_apiProductPrice[] | 是 | 商品清单。 |
| products[] | body | seller_apiProductPrice[] | 否 | 商品清单。 |
| products[].product_id | body | number | 是 | 商品识别号。 |
| products[].action_price | body | number | 是 | 商品活动期间的价格。 |
| products[].stock | body | number | 否 | 《库存折扣》促销中的商品单位数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | seller_apiProductV1ResponseResult | - |
| result.product_ids | number[] | 已添加到促销活动中的商品ID列表。 |
| result.product_ids[] | number[] | 已添加到促销活动中的商品ID列表。 |
| result.rejected | seller_apiProductV1ResponseProduct[] | 无法添加到促销活动中的商品列表。 |
| result.rejected[] | seller_apiProductV1ResponseProduct[] | 无法添加到促销活动中的商品列表。 |
| result.rejected[].product_id | number | 商品识别号。 |
| result.rejected[].reason | string | 该商品未被加入促销活动的原因。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

```json
{
  "result": {
    "product_ids": [
      1389
    ],
    "rejected": []
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998345.md

---

## 从活动中删除商品

### 接口说明

一种从活动中移除商品的方法。

### 接口标题

从活动中删除商品

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/products/deactivate`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | seller_apiProductIDsV1Request | 否 | 请求体。 |
| action_id | body | number | 是 | 活动识别号。可以使用方法 [/v1/actions](#operation/Promos)获取。 |
| product_ids | body | number[] | 是 | 活动识别号清单。 |
| product_ids[] | body | number[] | 否 | 活动识别号清单。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | seller_apiProductV1ResponseResultDeactivate | - |
| result.product_ids | number[] | 已从促销活动中删除的商品ID列表。 |
| result.product_ids[] | number[] | 已从促销活动中删除的商品ID列表。 |
| result.rejected | seller_apiProductV1ResponseProductDeactivate[] | 不能从促销活动中删除的商品清单。 |
| result.rejected[] | seller_apiProductV1ResponseProductDeactivate[] | 不能从促销活动中删除的商品清单。 |
| result.rejected[].product_id | number | 商品识别号。 |
| result.rejected[].reason | string | 该商品未从促销活动中删除的原因。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

```json
{
  "result": {
    "product_ids": [
      14975
    ],
    "rejected": []
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998346.md

---

## 申请折扣列表

### 接口说明

获取买家希望从卖家那里获得折扣的商品列表方法。

### 接口标题

申请折扣列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/discounts-task/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetDiscountTaskListRequest | 否 | 请求体。 |
| status | body | v1DiscountTaskStatus | 是 | - |
| page | body | integer | 否 | 需要从中下载折扣申请列表的页面。 |
| limit | body | integer | 是 | 页面上申请最大数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetDiscountTaskListResponseTask[] | 申请列表。 |
| result[] | v1GetDiscountTaskListResponseTask[] | 申请列表。 |
| result[].id | integer | 申请ID。 |
| result[].created_at | string | 申请创建日期。 |
| result[].end_at | string | 申请到期时间。 |
| result[].edited_till | string | 决定改变时间。 |
| result[].status | string | 申请状态。 |
| result[].customer_name | string | 买家姓名。 |
| result[].sku | integer | Ozon系统中的商品ID —— SKU。 |
| result[].user_comment | string | 买家对申请的评论。 |
| result[].seller_comment | string | 卖家对申请的评论。 |
| result[].requested_price | number | 申请价格。 |
| result[].approved_price | number | 批准的价格。 |
| result[].original_price | number | 折扣前的商品价格。 |
| result[].discount | number | 卢布折扣。 |
| result[].discount_percent | number | 折扣百分比。 |
| result[].base_price | number | 如果不参与促销活动，商品在Ozon上销售的基础价。 |
| result[].min_auto_price | number | 自动应用折扣和促销后的最低价格值。 |
| result[].prev_task_id | integer | 该商品买家先前申请ID。 |
| result[].is_damaged | boolean | 商品是否打折。如果打折，`true`。 |
| result[].moderated_at | string | 审核日期：审核、批准或拒绝申请。 |
| result[].approved_discount | number | 卖家同意的以卢布显示的折扣。 如果卖家不批准订单，则传递值“0”。 |
| result[].approved_discount_percent | number | 卖家批准的折扣百分比。请传递值  `0`，如果卖家不批准申请。 |
| result[].is_purchased | boolean | 用户是否购买了商品。 `true`，如果购买。 |
| result[].is_auto_moderated | boolean | 申请是否自动审核。 `true`，如果自动审核。 |
| result[].offer_id | string | 卖家系统中的商品标识符是商品货号。 |
| result[].email | string | 处理请求的卖家员工电子邮件地址。 |
| result[].last_name | string | 处理申请的卖家员工姓氏。 |
| result[].first_name | string | 处理请求的卖家员工姓名。 |
| result[].patronymic | string | 处理请求的卖家员工父称。 |
| result[].approved_quantity_min | integer | 商品数量批准的最小值。 |
| result[].approved_quantity_max | integer | 商品数量批准的最大值。 |
| result[].requested_quantity_min | integer | 商品请求数量最小值。 |
| result[].requested_quantity_max | integer | 商品请求数量最大值。 |
| result[].requested_price_with_fee | number | 带有区域加价的价格申请。 |
| result[].approved_price_with_fee | number | 批准的含区域加价的价格。 |
| result[].approved_price_fee_percent | number | 按百分比显示的区域加价。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

根据响应参数结构生成的示例：

```json
{
  "result": [
    {
      "id": 0,
      "created_at": "2026-01-01T00:00:00Z",
      "end_at": "2026-01-01T00:00:00Z",
      "edited_till": "2026-01-01T00:00:00Z",
      "status": "string",
      "customer_name": "string",
      "sku": 0,
      "user_comment": "string",
      "seller_comment": "string",
      "requested_price": 0,
      "approved_price": 0,
      "original_price": 0,
      "discount": 0,
      "discount_percent": 0,
      "base_price": 0,
      "min_auto_price": 0,
      "prev_task_id": 0,
      "is_damaged": false,
      "moderated_at": "2026-01-01T00:00:00Z",
      "approved_discount": 0,
      "approved_discount_percent": 0,
      "is_purchased": false,
      "is_auto_moderated": false,
      "offer_id": "string",
      "email": "string",
      "last_name": "string",
      "first_name": "string",
      "patronymic": "string",
      "approved_quantity_min": 0,
      "approved_quantity_max": 0,
      "requested_quantity_min": 0,
      "requested_quantity_max": 0,
      "requested_price_with_fee": 0,
      "approved_price_with_fee": 0,
      "approved_price_fee_percent": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998351.md

---

## 同意折扣申请

### 接口说明

您可以同意处于以下状态的申请：`NEW` — 新的， `SEEN` — 已查看的。

### 接口标题

同意折扣申请

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/discounts-task/approve`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ApproveDiscountTasksRequest | 否 | 请求体。 |
| tasks | body | v1ApproveDiscountTasksRequestTask[] | 是 | 申请列表。 |
| tasks[] | body | v1ApproveDiscountTasksRequestTask[] | 否 | 申请列表。 |
| tasks[].id | body | integer | 是 | 申请ID。可以使用方法 [/v1/actions/discounts-task/list](#operation/promos_task_list)获取。 |
| tasks[].approved_price | body | number | 是 | 同意的价格。 |
| tasks[].seller_comment | body | string | 否 | 卖家对申请的评论。 |
| tasks[].approved_quantity_min | body | integer | 是 | 批准的最小商品数量。 |
| tasks[].approved_quantity_max | body | integer | 是 | 批准的最大商品数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1ApproveDeclineDiscountTasksResponseResult | - |
| result.fail_details | ApproveDeclineDiscountTasksResponseFailDetail[] | 创建申请时的错误。 |
| result.fail_details[] | ApproveDeclineDiscountTasksResponseFailDetail[] | 创建申请时的错误。 |
| result.fail_details[].task_id | integer | 申请ID。 |
| result.fail_details[].error_for_user | string | 错误文本。 |
| result.success_count | integer | 状态更改成功的申请数量。 |
| result.fail_count | integer | 未能更改状态的申请数量。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

根据响应参数结构生成的示例：

```json
{
  "result": {
    "fail_details": [
      {
        "task_id": null,
        "error_for_user": null
      }
    ],
    "success_count": 0,
    "fail_count": 0
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998352.md

---

## 取消折扣申请

### 接口说明

您可以取消处于以下状态的申请： `NEW` — 新的, `SEEN` — 已查看的。

### 接口标题

取消折扣申请

### 接口地址

`POST https://api-seller.ozon.ru/v1/actions/discounts-task/decline`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1DeclineDiscountTasksRequest | 否 | 请求体。 |
| tasks | body | v1DeclineDiscountTasksRequestTask[] | 是 | 申请列表。 |
| tasks[] | body | v1DeclineDiscountTasksRequestTask[] | 否 | 申请列表。 |
| tasks[].id | body | integer | 是 | 申请ID。 |
| tasks[].seller_comment | body | string | 否 | 卖家对申请的评价。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1ApproveDeclineDiscountTasksResponseResult | - |
| result.fail_details | ApproveDeclineDiscountTasksResponseFailDetail[] | 创建申请时的错误。 |
| result.fail_details[] | ApproveDeclineDiscountTasksResponseFailDetail[] | 创建申请时的错误。 |
| result.fail_details[].task_id | integer | 申请ID。 |
| result.fail_details[].error_for_user | string | 错误文本。 |
| result.success_count | integer | 状态更改成功的申请数量。 |
| result.fail_count | integer | 未能更改状态的申请数量。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


### 响应示例

根据响应参数结构生成的示例：

```json
{
  "result": {
    "fail_details": [
      {
        "task_id": null,
        "error_for_user": null
      }
    ],
    "success_count": 0,
    "fail_count": 0
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998353.md

---
