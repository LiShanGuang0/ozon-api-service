# BetaMethod

接口数量：10

## 接口列表

- [将订单拆分为不带备货的货件](#将订单拆分为不带备货的货件) - `POST /v1/posting/fbs/split`
- [获取商品搜索查询信息](#获取商品搜索查询信息) - `POST /v1/analytics/product-queries`
- [有关特定商品查询的信息](#有关特定商品查询的信息) - `POST /v1/analytics/product-queries/details`
- [每日商品销售报告](#每日商品销售报告) - `POST /v1/finance/realization/by-day`
- [赔偿报告](#赔偿报告) - `POST /v1/finance/compensation`
- [赔偿返还报告](#赔偿返还报告) - `POST /v1/finance/decompensation`
- [传递 rFBS  退货的可用操作](#传递-rfbs-退货的可用操作) - `POST /v1/returns/rfbs/action/set`
- [获取平均配送时间的分析数据](#获取平均配送时间的分析数据) - `POST /v1/analytics/average-delivery-time`
- [获取平均配送时间的详细分析](#获取平均配送时间的详细分析) - `POST /v1/analytics/average-delivery-time/details`
- [体积重量特征不正确的商品列表](#体积重量特征不正确的商品列表) - `POST /v1/product/info/wrong-volume`

## 将订单拆分为不带备货的货件

### 接口说明

您可以在 [讨论](https://dev.ozon.ru/community/1068-Razdelenie-otpravleniia-na-neskolko) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

将订单拆分为不带备货的货件

### 接口地址

`POST https://api-seller.ozon.ru/v1/posting/fbs/split`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1PostingFbsSplitRequest | 否 | 请求体。 |
| posting_number | body | string | 是 | 货件编号。 |
| postings | body | v1PostingFbsSplitRequestPosting[] | 是 | 要拆分订单的货件项列表。每个请求只能拆分一个订单。 |
| postings[] | body | v1PostingFbsSplitRequestPosting[] | 否 | 要拆分订单的货件项列表。每个请求只能拆分一个订单。 |
| postings[].products | body | v1ProductFbsSplit[] | 是 | 订单中的商品列表。 |
| postings[].products[] | body | v1ProductFbsSplit[] | 否 | 订单中的商品列表。 |
| postings[].products[].product_id | body | integer | 是 | Ozon系统中的商品标识符 — SKU。 |
| postings[].products[].quantity | body | integer | 是 | 数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| parent_posting | v1PostingFbsSplitResponsePostingParent | - |
| parent_posting.posting_number | string | 原始货件编号。 |
| parent_posting.products | v1ProductFbsSplit[] | 货件中的商品列表。 |
| parent_posting.products[] | v1ProductFbsSplit[] | 货件中的商品列表。 |
| parent_posting.products[].product_id | integer | Ozon系统中的商品标识符 — SKU。 |
| parent_posting.products[].quantity | integer | 数量。 |
| postings | v1PostingFbsSplitResponsePosting[] | 订单被拆分后的货件列表。 |
| postings[] | v1PostingFbsSplitResponsePosting[] | 订单被拆分后的货件列表。 |
| postings[].posting_number | string | 货件编号。 |
| postings[].products | v1ProductFbsSplit[] | 货件中的商品列表。 |
| postings[].products[] | v1ProductFbsSplit[] | 货件中的商品列表。 |
| postings[].products[].product_id | integer | Ozon系统中的商品标识符 — SKU。 |
| postings[].products[].quantity | integer | 数量。 |


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
  "parent_posting": {
    "posting_number": "string",
    "products": [
      {
        "product_id": null,
        "quantity": null
      }
    ]
  },
  "postings": [
    {
      "posting_number": "string",
      "products": [
        null
      ]
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863082.md

---

## 获取商品搜索查询信息

### 接口说明

使用该方法可以获取您的商品在 Ozon 平台上的搜索查询信息。完整分析数据仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 和 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus)订阅用户。未订阅的用户可以查看部分指标。该方法类似于个人中心的 **搜索中的商品 → 我的商品的查询** 选项卡。
可以按指定日期范围获取分析数据。为此，需在请求中指定 `date_from` 和 `date_to` 参数。最近 1 个月的数据可随时查询，但不包括距离当前日期 3 天内的数据（此时间段的数据仍在计算中）。超过 1 个月前的数据仅适用于 [Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 及 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅用户，并且只能按周查询，需在请求中指定 `date_from` 参数。
您可以在 Ozon for Dev 开发者社区的[讨论区](https://dev.ozon.ru/community/1115-Metod-polucheniia-informatsii-o-zaprosakh-tovara)留下反馈。

### 接口标题

获取商品搜索查询信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/analytics/product-queries`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1AnalyticsProductQueriesRequest | 否 | 请求体。 |
| date_from | body | string | 是 | 分析数据的起始日期。 |
| date_to | body | string | 否 | 分析数据的结束日期。 |
| page | body | integer | 否 | 请求返回的页码。 |
| page_size | body | integer | 是 | 每页包含的商品数量。 |
| skus | body | string[] | 是 | SKU 列表，即 Ozon 系统中的商品标识符。根据这些 SKU 返回搜索查询的分析数据。最多可查询 1000 个 SKU。 |
| skus[] | body | string[] | 否 | SKU 列表，即 Ozon 系统中的商品标识符。根据这些 SKU 返回搜索查询的分析数据。最多可查询 1000 个 SKU。 |
| sort_by | body | AnalyticsProductQueriesRequestSortBy | 否 | - |
| sort_dir | body | AnalyticsProductQueriesRequestSortDir | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| analytics_period | AnalyticsProductQueriesResponseAnalyticsPeriod | - |
| analytics_period.date_from | string | 分析数据的起始日期。 |
| analytics_period.date_to | string | 分析数据的结束日期。 |
| items | v1AnalyticsProductQueriesResponseItem[] | 商品列表。 |
| items[] | v1AnalyticsProductQueriesResponseItem[] | 商品列表。 |
| items[].category | string | 类目名称。 |
| items[].currency | string | 货币单位。 |
| items[].gmv | number | 搜索查询的销售额。 |
| items[].name | string | 商品名称。 |
| items[].offer_id | string | 卖家系统中的商品标识符（商品编号）。 |
| items[].position | number | 商品的平均排名。仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，否则该字段为空。 |
| items[].sku | integer | Ozon 系统中的商品标识符（SKU）。 |
| items[].unique_search_users | integer | 在 Ozon 平台上搜索该商品的买家数量。 |
| items[].unique_view_users | integer | 在 Ozon 平台上看到该商品的买家数量。仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，否则该字段为空。 |
| items[].view_conversion | number | 商品的转化率。 仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，否则该字段为空。 |
| page_count | integer | 总页数。 |
| total | integer | 搜索请求的总数。 |


#### 400 请求有误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 403 禁止访问

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 404 记录不存在

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 409 409

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


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
  "analytics_period": {
    "date_from": "string",
    "date_to": "string"
  },
  "items": [
    {
      "category": "string",
      "currency": "string",
      "gmv": 0,
      "name": "string",
      "offer_id": "string",
      "position": 0,
      "sku": 0,
      "unique_search_users": 0,
      "unique_view_users": 0,
      "view_conversion": 0
    }
  ],
  "page_count": 0,
  "total": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863083.md

---

## 有关特定商品查询的信息

### 接口说明

使用该方法获取特定商品的查询数据。只有 [Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，才能查看完整分析数据。未订阅的用户可以查看部分指标。该方法与在个人中心的 **搜索中的商品 → 我的商品查询** 选项卡查看商品数据类似。
可以按指定日期范围获取分析数据。为此，需在请求中指定 `date_from` 和 `date_to` 参数。最近 1 个月的数据可随时查询，但不包括距离当前日期 3 天内的数据（此时间段的数据仍在计算中）。超过 1 个月前的数据仅适用于 [Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 及 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅用户，并且只能按周查询，需在请求中指定 `date_from` 参数。
您可以在 Ozon for Dev 开发者社区的[讨论区](https://dev.ozon.ru/community/1306-Metod-polucheniia-informatsii-o-zaprosakh-tovara-po-odnomu-tovaru)留下反馈。

### 接口标题

有关特定商品查询的信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/analytics/product-queries/details`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1AnalyticsProductQueriesDetailsRequest | 否 | 请求体。 |
| date_from | body | string | 是 | 分析数据的起始日期。 |
| date_to | body | string | 否 | 分析数据的结束日期。 |
| limit_by_sku | body | integer | 是 | 单个SKU的查询数量限制。最大值为15次查询。 |
| page | body | integer | 否 | 请求返回的页码。最小值为0。 |
| page_size | body | integer | 是 | 每页包含的商品数量。最大值为100。 |
| skus | body | string[] | 是 | SKU 列表，即 Ozon 系统中的商品标识符。根据这些 SKU 返回搜索查询的分析数据。最多可查询 1000 个 SKU。 |
| skus[] | body | string[] | 否 | SKU 列表，即 Ozon 系统中的商品标识符。根据这些 SKU 返回搜索查询的分析数据。最多可查询 1000 个 SKU。 |
| sort_by | body | v1AnalyticsProductQueriesDetailsRequestSortBy | 否 | - |
| sort_dir | body | v1AnalyticsProductQueriesDetailsRequestSortDir | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| analytics_period | v1AnalyticsProductQueriesDetailsResponseAnalyticsPeriod | - |
| analytics_period.date_from | string | 分析数据的起始日期。 |
| analytics_period.date_to | string | 分析数据的结束日期。 |
| page_count | integer | 总页数。 |
| queries | AnalyticsProductQueriesDetailsResponseQuery[] | 查询列表。 |
| queries[] | AnalyticsProductQueriesDetailsResponseQuery[] | 查询列表。 |
| queries[].currency | string | 货币单位。 |
| queries[].gmv | number | 搜索查询的销售额。 |
| queries[].order_count | integer | 根据查询的订单数量。 |
| queries[].position | number | 商品的平均排名。仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，否则该字段为空。 |
| queries[].query | string | 请求文本。 |
| queries[].query_index | integer | 查询序号。 |
| queries[].sku | integer | Ozon 系统中的商品标识符（SKU）。 |
| queries[].unique_search_users | integer | 在 Ozon 平台上搜索该商品的买家数量。 |
| queries[].unique_view_users | integer | 在 Ozon 平台上看到该商品的买家数量。仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，否则该字段为空。 |
| queries[].view_conversion | number | 商品的转化率。 仅适用于[Premium](https://seller-edu.ozon.ru/seller-rating/about-rating/premium-program) 或 [Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus) 订阅，否则该字段为空。 |
| total | integer | 搜索请求的总数。 |


#### 400 请求有误

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
  "analytics_period": {
    "date_from": "string",
    "date_to": "string"
  },
  "page_count": 0,
  "queries": [
    {
      "currency": "string",
      "gmv": 0,
      "order_count": 0,
      "position": 0,
      "query": "string",
      "query_index": 0,
      "sku": 0,
      "unique_search_users": 0,
      "unique_view_users": 0,
      "view_conversion": 0
    }
  ],
  "total": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863084.md

---

## 每日商品销售报告

### 接口说明

该方法返回每日[商品销售报告](#operation/FinanceAPI_GetRealizationReportV2)中的销售金额数据。不包括取消和无人认领的订单。数据仅可获取从当前日期起最多32个自然日之内的记录。此方法仅对[Premium Plus](https://seller-edu.ozon.ru/seller-rating/about-rating/subscription-premium-plus)订阅的用户开放。
您可以在Ozon for Dev开发者社区的[讨论区](https://dev.ozon.ru/community/1344-Metod-dlia-poluchenie-otcheta-o-realizatsii-za-den)对该方法留下反馈。

### 接口标题

每日商品销售报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/finance/realization/by-day`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetRealizationReportByDayRequest | 否 | 请求体。 |
| day | body | integer | 是 | 日。 |
| month | body | integer | 是 | 月。 |
| year | body | integer | 是 | 年。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| rows | GetRealizationReportByDayResponseRow[] | 报告表格。 |
| rows[] | GetRealizationReportByDayResponseRow[] | 报告表格。 |
| rows[].commission_ratio | number | 按类目划分的销售佣金比例。 |
| rows[].delivery_commission | RowItemCommission | - |
| rows[].delivery_commission.amount | number | 金额。 |
| rows[].delivery_commission.bonus | number | 折扣积分。 |
| rows[].delivery_commission.commission | number | 将折扣和加价考虑在内的总佣金。 |
| rows[].delivery_commission.compensation | number | Ozon负责的补付额。 |
| rows[].delivery_commission.price_per_instance | number | 每件价格。 |
| rows[].delivery_commission.quantity | integer | 商品数量。 |
| rows[].delivery_commission.standard_fee | number | Ozon基础奖励。 |
| rows[].delivery_commission.bank_coinvestment | number | 合作伙伴忠诚机制付款：绿色价格。 |
| rows[].delivery_commission.stars | number | 合作伙伴忠诚度机制付款：星星。 |
| rows[].delivery_commission.total | number | 应计总额。 |
| rows[].item | RowItem | - |
| rows[].item.barcode | string | 商品条形码。 |
| rows[].item.name | string | 商品名称。 |
| rows[].item.offer_id | string | 卖家系统中的商品标识符是商品货号。 |
| rows[].item.sku | integer | Ozon系统中的商品识别码是SKU。 |
| rows[].return_commission | RowItemCommissionReturn | - |
| rows[].return_commission.amount | number | 金额。 |
| rows[].return_commission.bonus | number | 折扣积分。 |
| rows[].return_commission.commission | number | 将折扣和加价考虑在内的总佣金。 |
| rows[].return_commission.compensation | number | Ozon负责的补付额。 |
| rows[].return_commission.price_per_instance | number | 每件价格。 |
| rows[].return_commission.quantity | integer | 商品数量。 |
| rows[].return_commission.standard_fee | number | Ozon基础奖励。 |
| rows[].return_commission.bank_coinvestment | number | 合作伙伴忠诚机制付款：绿色价格。 |
| rows[].return_commission.stars | number | 合作伙伴忠诚度机制付款：星星。 |
| rows[].return_commission.total | number | 应计总额。 |
| rows[].rowNumber | integer | 报告中的行号。 |
| rows[].seller_price_per_instance | number | 考虑折扣后的卖家价格。 |


#### 400 请求有误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 403 禁止访问

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 404 记录不存在

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 409 409

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


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
  "rows": [
    {
      "commission_ratio": 0,
      "delivery_commission": {
        "amount": null,
        "bonus": null,
        "commission": null,
        "compensation": null,
        "price_per_instance": null,
        "quantity": null,
        "standard_fee": null,
        "bank_coinvestment": null,
        "stars": null,
        "total": null
      },
      "item": {
        "barcode": null,
        "name": null,
        "offer_id": null,
        "sku": null
      },
      "return_commission": {
        "amount": null,
        "bonus": null,
        "commission": null,
        "compensation": null,
        "price_per_instance": null,
        "quantity": null,
        "standard_fee": null,
        "bank_coinvestment": null,
        "stars": null,
        "total": null
      },
      "rowNumber": 0,
      "seller_price_per_instance": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863085.md

---

## 赔偿报告

### 接口说明

用于获取赔偿报告的方法。与卖家个人中心中 **财务 → 文件 → 赔偿及其他应计费用** 部分的报告一致。
您可以在Ozon for Dev开发者社区的[讨论区](https://dev.ozon.ru/community/1352-Metody-polucheniia-otchetov-o-kompensatsiiakh-i-dekompesatsiiakh)对该方法留下反馈。

### 接口标题

赔偿报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/finance/compensation`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetCompensationReportRequest | 否 | 请求体。 |
| date | body | string | 是 | 报告周期格式为 `YYYY-MM`。 |
| language | body | compensationReportLanguage | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | CreateReportResponseCodeNoDeadline | - |
| result.code | string | 报告的唯一标识符。要获取报告，请将该值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |


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
    "code": "string"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863086.md

---

## 赔偿返还报告

### 接口说明

用于获取赔偿返还报告的方法。与卖家个人中心中 **财务 → 文件 → 赔偿及其他应计费用** 部分的报告一致。
您可以在Ozon for Dev开发者社区的[讨论区](https://dev.ozon.ru/community/1352-Metody-polucheniia-otchetov-o-kompensatsiiakh-i-dekompesatsiiakh)对该方法留下反馈。

### 接口标题

赔偿返还报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/finance/decompensation`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetDecompensationReportRequest | 否 | 请求体。 |
| date | body | string | 是 | 报告周期格式为 `YYYY-MM`。 |
| language | body | compensationReportLanguage | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | CreateReportResponseCodeNoDeadline | - |
| result.code | string | 报告的唯一标识符。要获取报告，请将该值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |


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
    "code": "string"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863087.md

---

## 传递 rFBS  退货的可用操作

### 接口说明

用于传递  rFBS 退货操作的方法。
您可以在 [讨论](https://dev.ozon.ru/community/1355-Metod-dlia-peredachi-dostupnykh-sobytii-dlia-rFBS-vozvratov) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

传递 rFBS  退货的可用操作

### 接口地址

`POST https://api-seller.ozon.ru/v1/returns/rfbs/action/set`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ReturnsRfbsActionSetRequest | 否 | 请求体。 |
| comment | body | string | 否 | 卖家评论。<br>对于 `id: -1` 和 `id: -10`，备注为必填项。 |
| compensation_amount | body | number | 否 | 赔偿金额。<br>对于 `id: 1020`，备注也为必填项。 |
| id | body | integer | 否 | 操作标识符。<br>获取可用操作 `returns.available_actions` ，请使用方法 [/v2/returns/rfbs/get](#operation/RFBSReturnsAPI_ReturnsRfbsGetV2)。 |
| rejection_reason_id | body | integer | 否 | 取消原因的标识符。<br>对于 `id: -1` 和 `id: -10`，备注为必填项。<br>获取可用取消原因 `returns.rejection_reason`，请使用方法 [/v2/returns/rfbs/get](#operation/RFBSReturnsAPI_ReturnsRfbsGetV2)。 |
| return_for_back_way | body | number | 否 | 退还给买家的商品运费金额。<br>负值将被视为 `0`。 |
| return_id | body | integer | 否 | 退货申请的标识符。 |


### 响应参数

#### 200 成功

暂无参数。


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
null
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863088.md

---

## 获取平均配送时间的分析数据

### 接口说明

该方法可获取商品配送到买家的平均时间分析。对应卖家个人中心**分析→ 销售地理→ 平均配送时间**模块。每个集群的详细分析可通过方法[/v1/analytics/average-delivery-time/details](#operation/AnalyticsAPI_AverageDeliveryTimeDetails)获取。
您可以在 [讨论](https://dev.ozon.ru/community/1421-Novye-metody-dlia-polucheniia-analitiki-po-srednemu-vremeni-dostavki) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

获取平均配送时间的分析数据

### 接口地址

`POST https://api-seller.ozon.ru/v1/analytics/average-delivery-time`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1AverageDeliveryTimeRequest | 否 | 请求体。 |
| delivery_schema | body | v1AverageDeliveryTimeRequestDeliverySchema | 是 | - |
| sku | body | string[] | 否 | 商品在 Ozon 系统中的标识符 — SKU。 |
| sku[] | body | string[] | 否 | 商品在 Ozon 系统中的标识符 — SKU。 |
| supply_period | body | v1AverageDeliveryTimeRequestSupplyPeriod | 是 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | v1AverageDeliveryTimeResponseData[] | 集群信息。 |
| data[] | v1AverageDeliveryTimeResponseData[] | 集群信息。 |
| data[].clusters_data | v1AverageDeliveryTimeResponseClustersData[] | 运输集群数据。 |
| data[].clusters_data[] | v1AverageDeliveryTimeResponseClustersData[] | 运输集群数据。 |
| data[].clusters_data[].another_delivery_time | v1AverageDeliveryTimeResponseClustersDataAmnesty[] | 已合并到另一配送时间。 |
| data[].clusters_data[].another_delivery_time[] | v1AverageDeliveryTimeResponseClustersDataAmnesty[] | 已合并到另一配送时间。 |
| data[].clusters_data[].cluster_id | integer | 集群标识码。 |
| data[].clusters_data[].delivery_time_FBO | integer | FBO模式下的规定配送时间（小时）。 |
| data[].clusters_data[].delivery_time_FBS | number | FBS模式下的规定配送时间（小时）。 |
| data[].clusters_data[].delivery_time_status | v1AverageDeliveryTimeResponseDeliveryTimeStatus | - |
| data[].clusters_data[].orders_count | integer | 从运输集群订购的商品数量。 |
| data[].clusters_data[].orders_percent | integer | 该集群订单数量占所有运输集群订单总数的百分比。 |
| data[].delivery_cluster_id | integer | 配送集群标识码。 |
| data[].metrics | v1AverageDeliveryTimeResponseMetrics | - |
| data[].metrics.attention_level | AttentionLevelEnum | - |
| data[].metrics.average_delivery_time | integer | 配送至买家的平均时间。 |
| data[].metrics.average_delivery_time_status | v1AverageDeliveryTimeResponseDeliveryTimeStatus | - |
| data[].metrics.impact_share | integer | 集群对总体指标的影响占比（百分比）。 |
| data[].metrics.lost_profit | integer | 物流额外支出。 |
| data[].metrics.orders_count | v1AverageDeliveryTimeResponseMetricsOrdersCount | - |
| data[].metrics.orders_count.fast | v1AverageDeliveryTimeResponseMetricsOrdersCountValueFast | - |
| data[].metrics.orders_count.long | v1AverageDeliveryTimeResponseMetricsOrdersCountValueLong | - |
| data[].metrics.orders_count.medium | v1AverageDeliveryTimeResponseMetricsOrdersCountValueMedium | - |
| data[].metrics.orders_count.total | integer | 合计。 |
| data[].metrics.recommended_supply | integer | 建议交货量（件）。 |
| total | AverageDeliveryTimeResponseTotal | - |
| total.attention_level | AttentionLevelEnum | - |
| total.average_delivery_time | integer | 配送至买家的平均时间。 |
| total.average_delivery_time_status | v1AverageDeliveryTimeResponseDeliveryTimeStatus | - |
| total.impact_share | integer | 集群对总体指标的影响占比（百分比）。 |
| total.lost_profit | integer | 物流额外支出。 |
| total.orders_count | v1AverageDeliveryTimeResponseOrdersCount | - |
| total.orders_count.fast | v1AverageDeliveryTimeResponseOrdersCountValueFast | - |
| total.orders_count.fast.percent | integer | 以百分比表示的数值。 |
| total.orders_count.fast.value | integer | 以件数表示的数值。 |
| total.orders_count.long | v1AverageDeliveryTimeResponseOrdersCountValueLong | - |
| total.orders_count.long.percent | integer | 以百分比表示的数值。 |
| total.orders_count.long.value | integer | 以件数表示的数值。 |
| total.orders_count.medium | v1AverageDeliveryTimeResponseOrdersCountValueMedium | - |
| total.orders_count.medium.percent | integer | 以百分比表示的数值。 |
| total.orders_count.medium.value | integer | 以件数表示的数值。 |
| total.orders_count.total | integer | 合计。 |
| total.recommended_supply | integer | 建议交货量（件）。 |


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
  "data": [
    {
      "clusters_data": [
        {
          "another_delivery_time": [],
          "cluster_id": 147,
          "delivery_time_FBO": 60,
          "delivery_time_FBS": 60,
          "delivery_time_status": "Medium",
          "orders_count": 1,
          "orders_percent": 2
        },
        {
          "another_delivery_time": [
            {
              "delivery_time": 28,
              "orders_count": 30,
              "orders_percent": 76,
              "delivery_time_status": "Fast"
            }
          ],
          "cluster_id": 154,
          "delivery_time_FBO": 60,
          "delivery_time_FBS": 60,
          "delivery_time_status": "Medium",
          "orders_count": 39,
          "orders_percent": 84
        }
      ],
      "delivery_cluster_id": 150,
      "metrics": {
        "average_delivery_time": 46,
        "average_delivery_time_status": "Medium",
        "recommended_supply": 957,
        "orders_count": {
          "total": 46,
          "fast": {
            "value": 12,
            "percent": 26
          },
          "medium": {
            "value": 34,
            "percent": 73
          },
          "long": {
            "value": 0,
            "percent": 0
          }
        },
        "impact_share": 30,
        "attention_level": "ATTENTION_HI",
        "lost_profit": 1763110
      }
    }
  ],
  "total": {
    "average_delivery_time": 45,
    "average_delivery_time_status": "Medium",
    "recommended_supply": 18579,
    "orders_count": {
      "total": 201,
      "fast": {
        "value": 105,
        "percent": 52
      },
      "medium": {
        "value": 78,
        "percent": 38
      },
      "long": {
        "value": 18,
        "percent": 8
      }
    },
    "impact_share": 100,
    "attention_level": "ATTENTION_LOW",
    "lost_profit": 5877036
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863089.md

---

## 获取平均配送时间的详细分析

### 接口说明

本方法对应卖家个人中心的**分析 → 配送范围 → 平均配送时间**模块。
如需获取各集群的总体分析，请使用方法/v1/analytics/average-delivery-time。
您可以在 [讨论](https://dev.ozon.ru/community/1421-Novye-metody-dlia-polucheniia-analitiki-po-srednemu-vremeni-dostavki) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

获取平均配送时间的详细分析

### 接口地址

`POST https://api-seller.ozon.ru/v1/analytics/average-delivery-time/details`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1AverageDeliveryTimeDetailsRequest | 否 | 请求体。 |
| cluster_id | body | integer | 是 | 集群标识码。 |
| filters | body | AverageDeliveryTimeDetailsRequestFilters | 否 | - |
| filters.delivery_schema | body | AverageDeliveryTimeDetailsRequestFiltersDeliverySchema | 否 | - |
| filters.supply_period | body | AverageDeliveryTimeDetailsRequestFiltersSupplyPeriod | 否 | - |
| limit | body | integer | 是 | 回答中的元素数量。 |
| offset | body | integer | 是 | 回答中会被略过的元素数量。例如，如果`offset = 10`，回答将从发现的第11个元素开始。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | v1AverageDeliveryTimeDetailsResponseData[] | 集群信息。 |
| data[] | v1AverageDeliveryTimeDetailsResponseData[] | 集群信息。 |
| data[].clusters_data | v1AverageDeliveryTimeDetailsResponseClustersData[] | Данные по кластерам отгрузки. |
| data[].clusters_data[] | v1AverageDeliveryTimeDetailsResponseClustersData[] | Данные по кластерам отгрузки. |
| data[].clusters_data[].another_delivery_time | v1AverageDeliveryTimeDetailsResponseClustersDataAmnesty[] | 已合并到另一配送时间。 |
| data[].clusters_data[].another_delivery_time[] | v1AverageDeliveryTimeDetailsResponseClustersDataAmnesty[] | 已合并到另一配送时间。 |
| data[].clusters_data[].cluster_id | integer | 集群标识码。 |
| data[].clusters_data[].delivery_time_FBO | integer | FBO模式下的规定配送时间（小时）。 |
| data[].clusters_data[].delivery_time_FBS | number | FBS模式下的规定配送时间（小时）。 |
| data[].clusters_data[].delivery_time_status | v1AverageDeliveryTimeDetailsResponseDeliveryTimeStatus | - |
| data[].clusters_data[].orders_count | integer | 从运输集群订购的商品数量。 |
| data[].clusters_data[].orders_percent | integer | 该集群订单数量占所有运输集群订单总数的百分比。 |
| data[].item | AverageDeliveryTimeDetailsResponseItemData | - |
| data[].item.delivery_schema | AverageDeliveryTimeDetailsResponseItemDataDeliverySchema | - |
| data[].item.name | string | 商品名称。 |
| data[].item.offer_id | string | 卖家系统中的商品标识符 —— 货号。 |
| data[].item.sku | integer | Ozon系统中的商品标识符 —— SKU。 |
| data[].metrics | v1AverageDeliveryTimeDetailsResponseMetrics | - |
| data[].metrics.attention_level | AverageDeliveryTimeDetailsResponseMetricsAttentionLevel | - |
| data[].metrics.average_delivery_time | integer | 配送至买家的平均时间。 |
| data[].metrics.average_delivery_time_status | v1AverageDeliveryTimeDetailsResponseDeliveryTimeStatus | - |
| data[].metrics.impact_share | integer | 集群对总体指标的影响占比（百分比）。 |
| data[].metrics.lost_profit | integer | 物流额外支出。 |
| data[].metrics.orders_count | v1AverageDeliveryTimeDetailsResponseMetricsOrdersCount | - |
| data[].metrics.orders_count.fast | v1AverageDeliveryTimeDetailsResponseMetricsOrdersCountValueFast | - |
| data[].metrics.orders_count.long | v1AverageDeliveryTimeDetailsResponseMetricsOrdersCountValueLong | - |
| data[].metrics.orders_count.medium | v1AverageDeliveryTimeDetailsResponseMetricsOrdersCountValueMedium | - |
| data[].metrics.orders_count.total | integer | 订购的商品总数。 |
| data[].metrics.recommended_supply | integer | 建议交货量（件）。 |
| total_rows | integer | 总记录数。 |


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
  "data": [
    {
      "clusters_data": [
        {
          "another_delivery_time": [],
          "cluster_id": 154,
          "delivery_time_FBO": 0,
          "delivery_time_FBS": 0,
          "delivery_time_status": "Fast",
          "orders_count": 1,
          "orders_percent": 100
        }
      ],
      "item": {
        "name": "充气球适合儿童（套装：足球、篮球、橄榄球）配有打气筒",
        "delivery_schema": "ALL",
        "sku": 1423433655,
        "offer_id": "59704000"
      },
      "metrics": {
        "average_delivery_time": 31,
        "average_delivery_time_status": "Fast",
        "recommended_supply": 0,
        "orders_count": {
          "total": 1,
          "fast": {
            "value": 1,
            "percent": 100
          },
          "medium": {
            "value": 0,
            "percent": 0
          },
          "long": {
            "value": 0,
            "percent": 0
          }
        },
        "impact_share": 0,
        "attention_level": "LOW",
        "lost_profit": 0
      }
    }
  ],
  "total_rows": 10
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863090.md

---

## 体积重量特征不正确的商品列表

### 接口说明

返回体积重量特征不正确的商品列表。如果您已正确填写尺寸，请联系Ozon客服。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1260-Informer-nekorrektnykh-OVKh)区中，留下对此方法的反馈。

### 接口标题

体积重量特征不正确的商品列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/info/wrong-volume`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductInfoWrongVolumeRequest | 否 | 请求体。 |
| cursor | body | string | 否 | 用于获取下一批数据的指针。 |
| limit | body | integer | 否 | 响应中记录数量的限制。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| cursor | string | 用于获取下一批数据的指针。 |
| products | ProductInfoWrongVolumeResponseWrongVolumeProduct[] | 商品列表。 |
| products[] | ProductInfoWrongVolumeResponseWrongVolumeProduct[] | 商品列表。 |
| products[].height | integer | 商品高度。 |
| products[].length | integer | 商品长度。 |
| products[].name | string | 商品名称。 |
| products[].offer_id | string | 卖家系统中的商品标识符 —— 货号。 |
| products[].product_id | integer | 卖家系统中的商品标识符 —— `product_id`。 |
| products[].sku | integer | Ozon系统中的商品标识符 —— SKU。 |
| products[].weight | integer | 商品包装重量。 |
| products[].width | integer | 商品宽度。 |


#### 400 请求有误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 403 禁止访问

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 404 记录不存在

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


#### 409 409

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 有关错误的补充信息。 |
| details[] | protobufAny[] | 有关错误的补充信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误描述。 |


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
  "cursor": "string",
  "products": [
    {
      "height": 0,
      "length": 0,
      "name": "string",
      "offer_id": "string",
      "product_id": 0,
      "sku": 0,
      "weight": 0,
      "width": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863091.md

---
