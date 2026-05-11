# ReportAPI

接口数量：7

## 接口列表

- [报告信息](#报告信息) - `POST /v1/report/info`
- [报告清单](#报告清单) - `POST /v1/report/list`
- [商品报告](#商品报告) - `POST /v1/report/products/create`
- [发货报告](#发货报告) - `POST /v1/report/postings/create`
- [财务报告](#财务报告) - `POST /v1/finance/cash-flow-statement/list`
- [减价商品报告](#减价商品报告) - `POST /v1/report/discounted/create`
- [关于FBS仓库库存报告](#关于fbs仓库库存报告) - `POST /v1/report/warehouse/stock`

## 报告信息

### 接口说明

通过识别码回送有关先前创建的报告的信息。

### 接口标题

报告信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/report/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | reportReportInfoRequest | 否 | 请求体。 |
| code | body | string | 是 | 报告的唯一识别码。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | reportReportinfo | - |
| result.code | string | 报告的唯一识别码。 |
| result.created_at | string | 报告创建日期。 |
| result.error | string | 生成报告时的错误代码。 |
| result.file | string | XLSX文件的链接。<br>`SELLER_RETURNS` 类型的报告，链接有效期为5分钟。 |
| result.params | object | 一个数组，包含卖家创建报告时指定的过滤器。 |
| result.report_type | string | 报告类型：<br>- `SELLER_PRODUCTS` — 商品报告，<br>- `SELLER_TRANSACTIONS` — 交易报告，<br>- `SELLER_PRODUCT_PRICES` — 商品价格报告，<br>- `SELLER_STOCK` — 商品库存报告，<br>- `SELLER_RETURNS` — 退货报告，<br>- `SELLER_POSTINGS` — 发货报告，<br>- `SELLER_FINANCE` — 财务报告，<br>- `SELLER_PRODUCT_DISCOUNTED` — 减价商品报告，<br>- `DOCUMENT_B2B_SALES` — 面向法人客户的销售报告，<br>- `MUTUAL_SETTLEMENT` — 结算报告，<br>- `COMPENSATION` — 赔偿报告，<br>- `DECOMPENSATION` — 赔偿返还报告。 |
| result.status | string | 报告生成状态：<br>- `waiting`—在等待队列中待处理，<br>- `processing`—正在处理，<br>- `success`，<br>- `failed`。 |


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

```json
{
  "result": {
    "code": "REPORT_seller_products_924336_1720170405_a9ea2f27-a473-4b13-99f9-d0cfcb5b1a69",
    "status": "success",
    "error": "",
    "file": "https://cdn1.ozone.ru/s3/item-picture-6/f3/ce/f4ceae54b323213d3e61e59c323bd8e5.csv",
    "report_type": "seller_products",
    "params": {},
    "created_at": "2021-11-25T14:54:55.688260Z"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998407.md

---

## 报告清单

### 接口说明

回送之前已经生成的报告的列表。

### 接口标题

报告清单

### 接口地址

`POST https://api-seller.ozon.ru/v1/report/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | reportReportListRequest | 否 | 请求体。 |
| page | body | integer | 是 | 页数。 |
| page_size | body | integer | 是 | 每页的值的数量：<br>- 默认值 — 100，<br>- 最大值 — 1,000。 |
| report_type | body | ReportListRequestReportType | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | ReportListResponseResult | - |
| result.reports | reportReport[] | 包含所有生成的报告的数组。 |
| result.reports[] | reportReport[] | 包含所有生成的报告的数组。 |
| result.reports[].code | string | 报告的唯一识别码。要获取报告，请将此值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |
| result.reports[].created_at | string | 报告创建日期。 |
| result.reports[].error | string | 生成报告时的错误代码。 |
| result.reports[].file | string | XLSX文件的链接。<br>`SELLER_RETURNS` 类型的报告，链接有效期为5分钟。 |
| result.reports[].params | object | 一个数组，包含卖家创建报告时指定的过滤器。 |
| result.reports[].report_type | string | 报告类型：<br>- `SELLER_PRODUCTS` — 商品报告，<br>- `SELLER_TRANSACTIONS` — 交易报告，<br>- `SELLER_PRODUCT_PRICES` — 商品价格报告，<br>- `SELLER_STOCK` — 商品库存报告，<br>- `SELLER_RETURNS` — 退货报告，<br>- `SELLER_POSTINGS` — 发货报告，<br>- `SELLER_FINANCE` — 财务报告，<br>- `SELLER_PRODUCT_DISCOUNTED` — 减价商品报告，<br>- `DOCUMENT_B2B_SALES` — 面向法人客户的销售报告，<br>- `MUTUAL_SETTLEMENT` — 结算报告，<br>- `COMPENSATION` — 赔偿报告，<br>- `DECOMPENSATION` — 赔偿返还报告。 |
| result.reports[].status | string | 报告生成状态：<br>- `waiting`—在等待队列中待处理，<br>- `processing`—正在处理，<br>- `success`—报告成功生成，<br>- `failed` — 报告生成错误。 |
| result.total | integer | 累计报告数。 |


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

```json
{
  "result": {
    "reports": [
      {
        "code": "REPORT_seller_products_924336_1720170405_a9ea2f27-a473-4b13-99f9-d0cfcb5b1a69",
        "status": "success",
        "error": "",
        "file": "https://cdn1.ozone.ru/s3/item-picture-6/f3/ce/f4ceae54b323213d3e61e59c323bd8e5.csv",
        "report_type": "seller_products",
        "params": {
          "visibility": "3"
        },
        "created_at": "2019-02-06T12:09:47.258062Z"
      },
      {
        "code": "REPORT_seller_products_924336_1720170405_a9ea2f27-a473-4b13-99f9-d0cfcb5b1a69",
        "status": "success",
        "error": "",
        "file": "https://cdn1.ozone.ru/s3/item-picture-6/f3/ce/f4ceae54b323213d3e61e59c323bd8e5.csv",
        "report_type": "seller_products",
        "params": {
          "visibility": "3"
        },
        "created_at": "2019-02-15T08:34:32.267178Z"
      }
    ],
    "total": 2
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998408.md

---

## 商品报告

### 接口说明

获得带有商品数据的报告的方法。例如，Ozon的ID，商品的数量，价格，状态。
与个人中心中的**商品和价格→商品列表→下载商品CSV**部分相符。
一些空白的解释：
- __Ozon Product ID__ — 我们系统中的卖家系统中的商品标识符 — `product_id`。例如，如果你从Ozon仓库和你自己的仓库销售商品，Ozon商品识别码对他们来说将是相同的。
- __FBO Ozon SKU ID__ — 从Ozon仓库出售的卖家系统中的商品标识符 — `product_id`。
- __FBO Ozon SKU ID__ — 从您的仓库出售的卖家系统中的商品标识符 — `product_id`。
- __CrossBorder Ozon SKU__ — 从国外销售的卖家系统中的商品标识符 — `product_id`。
- __Barcode__ — 印在标签上的商品条形码。
- __Статус товара__ — 该商品是否可以在Ozon上购买。如果状态是 "准备出售"，则不能购买该商品。
- __Доступно на складе Ozon, шт__ — 可供销售的库存商品的数量。这个数额不包括保留商品。
- __Зарезервировано, шт__ — 一个状态为 "已预订 "的商品有多少单位。商品从Ozon收到订单的那一刻起就被保留了，直到它被包装好交付给客户。
- __Текущая цена с учётом скидки, руб.__ — 报告加载时商品的销售价格（包括折扣）。如果该商品参加了促销活动，则指定的价格没有折扣。
- __Базовая цена (цена до скидок), руб.__ — 无折扣的价格。
- __Цена Premium, руб.__ — 有Ozon Premium订阅买家的价格。
- __Рекомендованная цена, руб.__ — 商品在另一个市场上的最低价格。
- __Актуальная ссылка на рекомендованную цену__ — 在另一个市场上有推荐价格商品的链接。

### 接口标题

商品报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/report/products/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | reportCreateCompanyProductsReportRequest | 否 | 请求体。 |
| language | body | reportLanguage | 否 | - |
| offer_id | body | string[] | 否 | 卖家系统中的商品标识符是商品货号。 |
| offer_id[] | body | string[] | 否 | 卖家系统中的商品标识符是商品货号。 |
| search | body | string | 否 | 在记录内容中搜索，检查现货。 |
| sku | body | integer[] | 否 | Ozon系统中的卖家系统中的商品标识符 — `product_id`。 |
| sku[] | body | integer[] | 否 | Ozon系统中的卖家系统中的商品标识符 — `product_id`。 |
| visibility | body | reportCreateCompanyProductsReportRequestVisibility | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | CreateReportResponseCode | - |
| result.code | string | 报告的唯一识别码。要获取报告，请将此值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |


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

```json
{
  "result": {
    "code": "REPORT_seller_products_924336_1720170405_a9ea2f27-a473-4b13-99f9-d0cfcb5b1a69"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998409.md

---

## 发货报告

### 接口说明

带有订单信息的发货报告：
- 订单状态，
- 处理的开始日期，
- 订单号，
- 发货号码，
- 发货费用，
- 发货内容。
与个人中心中的**FBO→来自Ozon仓库的订单**和**FBS→来自我的仓库的订单→CSV**部分相符。

### 接口标题

发货报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/report/postings/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | reportCreateCompanyPostingsReportRequest | 否 | 请求体。 |
| filter | body | reportCreateCompanyPostingsReportRequestFilter | 是 | - |
| filter.cancel_reason_id | body | integer[] | 否 | 取消原因的识别码。 |
| filter.cancel_reason_id[] | body | integer[] | 否 | 取消原因的识别码。 |
| filter.delivery_schema | body | string[] | 否 | 运作机制是FBO或FBS。<br>对于海外卖家来说，只有FBS方案可用，所以在参数中提交数值`fbs`。 |
| filter.delivery_schema[] | body | string[] | 否 | 运作机制是FBO或FBS。<br>对于海外卖家来说，只有FBS方案可用，所以在参数中提交数值`fbs`。 |
| filter.offer_id | body | string | 否 | 卖家系统中的商品标识符是商品货号。 |
| filter.processed_at_from | body | string | 否 | 订单进入处理程序的时间。 |
| filter.processed_at_to | body | string | 否 | 订单出现在个人账户的时间。 |
| filter.sku | body | integer[] | 否 | Ozon系统中的卖家系统中的商品标识符 — `product_id`。 |
| filter.sku[] | body | integer[] | 否 | Ozon系统中的卖家系统中的商品标识符 — `product_id`。 |
| filter.status_alias | body | string[] | 否 | 状态文本。 |
| filter.status_alias[] | body | string[] | 否 | 状态文本。 |
| filter.statuses | body | integer[] | 否 | 数值状况。 |
| filter.statuses[] | body | integer[] | 否 | 数值状况。 |
| filter.title | body | string | 否 | 商品名称。 |
| language | body | reportLanguage | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | CreateReportResponseCode | - |
| result.code | string | 报告的唯一识别码。要获取报告，请将此值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |


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

```json
{
  "result": {
    "code": "REPORT_seller_postings_514893_1722847571_32a3508c-6b53-408c-a212-6c97138d23ed"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998411.md

---

## 财务报告

### 接口说明

从1号到15号以及从16号到31号的财务报告获取方式。
在请求一天的报告时，您将收到15天的报告。
与个人中心中的**财务→报告列表**部分相符。

### 接口标题

财务报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/finance/cash-flow-statement/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v3FinanceCashFlowStatementListRequest | 否 | 请求体。 |
| date | body | financev3Period | 是 | - |
| date.from | body | string | 是 | 计算报告的起始日期。 |
| date.to | body | string | 是 | 计算报告的停止日期。 |
| page | body | integer | 是 | 请求返回中的页码。 |
| with_details | body | boolean | 否 | `true`，如果需要在响应中添加附加参数。 |
| page_size | body | integer | 是 | 页面上的元素数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v3FinanceCashFlowStatementListResponseResult | - |
| result.cash_flows | FinanceCashFlowStatementListResponseCashFlow[] | 报告清单。 |
| result.cash_flows[] | FinanceCashFlowStatementListResponseCashFlow[] | 报告清单。 |
| result.cash_flows[].period | v3FinanceCashFlowStatementListResponsePeriod | 时期。 |
| result.cash_flows[].period.id | integer | 时期识别码。 |
| result.cash_flows[].period.begin | string | 开始阶段。 |
| result.cash_flows[].period.end | string | 结束阶段。 |
| result.cash_flows[].orders_amount | number | 已成交商品的价格总和。 |
| result.cash_flows[].returns_amount | number | 退货价格总和。 |
| result.cash_flows[].commission_amount | number | 商品销售Ozon佣金。 |
| result.cash_flows[].services_amount | number | 附加服务数额。 |
| result.cash_flows[].item_delivery_and_return_amount | number | 物流服务数额。 |
| result.cash_flows[].currency_code | string | 佣金计算的货币代码。 |
| result.details | FinanceCashFlowStatementListResponseDetails[] | 细节信息。 |
| result.details[] | FinanceCashFlowStatementListResponseDetails[] | 细节信息。 |
| result.details[].begin_balance_amount | number | 开始阶段的收支。 |
| result.details[].delivery | DetailsDeliveryDetails | 方法操作结果。 |
| result.details[].delivery.total | number | 总额。 |
| result.details[].delivery.amount | number | 考虑佣金商品购买的价格。 |
| result.details[].delivery.delivery_services | DetailsServices | 加工费和运费。 |
| result.details[].invoice_transfer | number | 当期应付金额。 |
| result.details[].loan | number | 根据贷款协议转账。 |
| result.details[].payments | DetailsPayment | 期间已付清。 |
| result.details[].payments.currency_code | string | 货币。 |
| result.details[].payments.payment | number | 支付金额。 |
| result.details[].period | v3FinanceCashFlowStatementListResponsePeriod | 时期。 |
| result.details[].period.id | integer | 时期识别码。 |
| result.details[].period.begin | string | 开始阶段。 |
| result.details[].period.end | string | 结束阶段。 |
| result.details[].return | DetailsReturnDetails | - |
| result.details[].return.total | number | 总金额。 |
| result.details[].return.amount | number | 佣金考虑在内的退款金额。 |
| result.details[].return.return_services | DetailsReturns | 退款和取消的费用。 |
| result.details[].rfbs | DetailsRfbsDetails | rFBS框架下的转账金额。 |
| result.details[].rfbs.total | number | 总额。 |
| result.details[].rfbs.transfer_delivery | number | 来自买家的转账金额。 |
| result.details[].rfbs.transfer_delivery_return | number | 退还给买家的转账金额。 |
| result.details[].rfbs.compensation_delivery_return | number | 物流转账金额补贴。 |
| result.details[].rfbs.partial_compensation | number | 将部分退款转移给买家。 |
| result.details[].rfbs.partial_compensation_return | number | 退换部分退款。 |
| result.details[].services | DetailsService | 服务。 |
| result.details[].services.total | number | 总额。 |
| result.details[].services.items | FinanceCashFlowStatementListResponseService[] | 细节。 |
| result.details[].others | DetailsOthers | 补偿费和其他费用。 |
| result.details[].others.total | number | 总数。 |
| result.details[].others.items | FinanceCashFlowStatementListResponseDetailsOthers[] | 细节。 |
| result.details[].end_balance_amount | number | 结束阶段的收支。 |
| result.page_count | integer | 含有报告的页数。 |


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

```json
{
  "result": {
    "cash_flows": [
      {
        "commission_amount": 1437,
        "currency_code": "string",
        "item_delivery_and_return_amount": 1991,
        "orders_amount": 1000,
        "period": {
          "begin": "2023-04-03T09:12:10.239Z",
          "end": "2023-04-03T09:12:10.239Z",
          "id": 11567022278500
        },
        "returns_amount": -3000,
        "services_amount": 8471.28
      }
    ],
    "details": {
      "period": {
        "begin": "2023-04-03T09:12:10.239Z",
        "end": "2023-04-03T09:12:10.239Z",
        "id": 11567022278500
      },
      "payments": [
        {
          "payment": 0,
          "currency_code": "string"
        }
      ],
      "begin_balance_amount": 0,
      "delivery": {
        "total": 0,
        "amount": 0,
        "delivery_services": {
          "total": 0,
          "items": [
            {
              "name": "string",
              "price": 0
            }
          ]
        }
      },
      "return": {
        "total": 0,
        "amount": 0,
        "return_services": {
          "total": 0,
          "items": [
            {
              "name": "string",
              "price": 0
            }
          ]
        }
      },
      "loan": 0,
      "invoice_transfer": 0,
      "rfbs": {
        "total": 0,
        "transfer_delivery": 0,
        "transfer_delivery_return": 0,
        "compensation_delivery_return": 0,
        "partial_compensation": 0,
        "partial_compensation_return": 0
      },
      "services": {
        "total": 0,
        "items": [
          {
            "name": "string",
            "price": 0
          }
        ]
      },
      "others": {
        "total": 0,
        "items": [
          {
            "name": "string",
            "price": 0
          }
        ]
      },
      "end_balance_amount": 0
    }
  },
  "page_count": 15
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998412.md

---

## 减价商品报告

### 接口说明

开始生成关于Ozon仓库中打折商品的报告。
Ozon可以自行处理一个商品，例如，如果它被损坏了。
请求结果将不是报告本身，而是其唯一的识别码。
要获取报告，请在 [/v1/report/info](#operation/ReportAPI_ReportInfo) 方法请求中发送ID。
从一个卖家账号每分钟可以发送1次请求。
与个人中心中的**分析→报告→来自Ozon仓库的销售→由Ozon减价的商品**部分相符。

### 接口标题

减价商品报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/report/discounted/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | reportCreateDiscountedRequest | 否 | 请求体。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | string | 报告的唯一识别码。要获取报告，请将此值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |


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

```json
{
  "code": "REPORT_seller_products_924336_1720170405_a9ea2f27-a473-4b13-99f9-d0cfcb5b1a69"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998413.md

---

## 关于FBS仓库库存报告

### 接口说明

报告包含仓库中可用和预留的商品数量的信息。
与个人中心中的**FBO→物流管理→库存管理→以XLS格式下载**部分相符。
查询的结果不是报告本身，而是其唯一ID。要获取报告，请在 [/v1/report/info](#operation/ReportAPI_ReportInfo) 方法的请求中发送ID。

### 接口标题

关于FBS仓库库存报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/report/warehouse/stock`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1CreateStockByWarehouseReportRequest | 否 | 请求体。 |
| language | body | reportLanguage | 否 | - |
| warehouseId | body | string[] | 是 | 仓库ID。 |
| warehouseId[] | body | string[] | 否 | 仓库ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | CreateReportResponseCode | - |
| result.code | string | 报告的唯一识别码。要获取报告，请将此值传递到方法 [/v1/report/info](#operation/ReportAPI_ReportInfo)。 |


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

```json
{
  "code": "REPORT_seller_products_924336_1720170405_a9ea2f27-a473-4b13-99f9-d0cfcb5b1a69"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998414.md

---
