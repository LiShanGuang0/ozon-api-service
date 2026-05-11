# FinanceAPI

接口数量：4

## 接口列表

- [商品销售报告 （第2版）](#商品销售报告-（第2版）) - `POST /v2/finance/realization`
- [按订单细分的商品销售报告](#按订单细分的商品销售报告) - `POST /v1/finance/realization/posting`
- [交易清单](#交易清单) - `POST /v3/finance/transaction/list`
- [清单数目](#清单数目) - `POST /v3/finance/transaction/totals`

## 商品销售报告 （第2版）

### 接口说明

当月与交付和退货有关的销售情况。订单取消与非赎回不包括其中。
与个人中心中的**财务→文件→销售报告→商品销售报告**部分相符。
报告将最迟于下个月的第五天发送。

### 接口标题

商品销售报告 （第2版）

### 接口地址

`POST https://api-seller.ozon.ru/v2/finance/realization`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2GetRealizationReportRequestV2 | 否 | 请求体。 |
| month | body | integer | 是 | 月。 |
| year | body | integer | 是 | 年。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | GetRealizationReportResponseV2Result | - |
| result.header | GetRealizationReportResponseV2Header | - |
| result.header.contract_date | string | 合同签订日期。 |
| result.header.contract_number | string | 合同编号。 |
| result.header.currency_sys_name | string | 货币。 |
| result.header.doc_amount | number | 应计总计。 |
| result.header.doc_date | string | 文件生成日期。 |
| result.header.number | string | 销售报告编号。 |
| result.header.payer_inn | string | 付款人的纳税人识别号。 |
| result.header.payer_kpp | string | 付款人的纳税人登记原因代码。 |
| result.header.payer_name | string | 付款人名称。 |
| result.header.receiver_inn | string | 收款人的纳税人识别号。 |
| result.header.receiver_kpp | string | 收款人的纳税人登记原因代码。 |
| result.header.receiver_name | string | 收款人名称。 |
| result.header.start_date | string | 期间开始。 |
| result.header.stop_date | string | 期间结束。 |
| result.header.vat_amount | number | 应计金额中包含的增值税金额。 |
| result.rows | GetRealizationReportResponseV2Row[] | 报告表格。 |
| result.rows[] | GetRealizationReportResponseV2Row[] | 报告表格。 |
| result.rows[].commission_ratio | number | 按类目分类的销售佣金份额。 |
| result.rows[].delivery_commission | RowItemCommission | - |
| result.rows[].delivery_commission.amount | number | 金额。 |
| result.rows[].delivery_commission.bonus | number | 折扣积分。 |
| result.rows[].delivery_commission.commission | number | 将折扣和加价考虑在内的总佣金。 |
| result.rows[].delivery_commission.compensation | number | Ozon负责的补付额。 |
| result.rows[].delivery_commission.price_per_instance | number | 每件价格。 |
| result.rows[].delivery_commission.quantity | integer | 商品数量。 |
| result.rows[].delivery_commission.standard_fee | number | Ozon基础奖励。 |
| result.rows[].delivery_commission.bank_coinvestment | number | 合作伙伴忠诚机制付款：绿色价格。 |
| result.rows[].delivery_commission.stars | number | 合作伙伴忠诚度机制付款：星星。 |
| result.rows[].delivery_commission.total | number | 应计总额。 |
| result.rows[].item | RowItem | - |
| result.rows[].item.barcode | string | 商品条形码。 |
| result.rows[].item.name | string | 商品名称。 |
| result.rows[].item.offer_id | string | 卖家系统中的商品标识符是商品货号。 |
| result.rows[].item.sku | integer | Ozon系统中的商品识别码是SKU。 |
| result.rows[].return_commission | RowItemCommissionReturn | - |
| result.rows[].return_commission.amount | number | 金额。 |
| result.rows[].return_commission.bonus | number | 折扣积分。 |
| result.rows[].return_commission.commission | number | 将折扣和加价考虑在内的总佣金。 |
| result.rows[].return_commission.compensation | number | Ozon负责的补付额。 |
| result.rows[].return_commission.price_per_instance | number | 每件价格。 |
| result.rows[].return_commission.quantity | integer | 商品数量。 |
| result.rows[].return_commission.standard_fee | number | Ozon基础奖励。 |
| result.rows[].return_commission.bank_coinvestment | number | 合作伙伴忠诚机制付款：绿色价格。 |
| result.rows[].return_commission.stars | number | 合作伙伴忠诚度机制付款：星星。 |
| result.rows[].return_commission.total | number | 应计总额。 |
| result.rows[].rowNumber | integer | 报告中的行编号。 |
| result.rows[].seller_price_per_instance | number | 将折扣考虑在内的卖家价格。 |


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
  "result": {
    "header": {
      "contract_date": "string",
      "contract_number": "string",
      "currency_sys_name": "string",
      "doc_amount": 0,
      "doc_date": "string",
      "number": "string",
      "payer_inn": "string",
      "payer_kpp": "string",
      "payer_name": "string",
      "receiver_inn": "string",
      "receiver_kpp": "string",
      "receiver_name": "string",
      "start_date": "string",
      "stop_date": "string",
      "vat_amount": 0
    },
    "rows": [
      {
        "commission_ratio": null,
        "delivery_commission": null,
        "item": null,
        "return_commission": null,
        "rowNumber": null,
        "seller_price_per_instance": null
      }
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863063.md

---

## 按订单细分的商品销售报告

### 接口说明

已送达和已退回商品销售的报告，带有每笔订单的详细信息。不包括取消和无人认领的订单。从现在起至2023年8月的报告可供您使用。

### 接口标题

按订单细分的商品销售报告

### 接口地址

`POST https://api-seller.ozon.ru/v1/finance/realization/posting`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetRealizationReportPostingRequest | 否 | 请求体。 |
| month | body | integer | 是 | 月。 |
| year | body | integer | 是 | 年。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| header | GetRealizationReportResponseV2Header | - |
| header.contract_date | string | 合同签订日期。 |
| header.contract_number | string | 合同编号。 |
| header.currency_sys_name | string | 货币。 |
| header.doc_amount | number | 应计总计。 |
| header.doc_date | string | 文件生成日期。 |
| header.number | string | 销售报告编号。 |
| header.payer_inn | string | 付款人的纳税人识别号。 |
| header.payer_kpp | string | 付款人的纳税人登记原因代码。 |
| header.payer_name | string | 付款人名称。 |
| header.receiver_inn | string | 收款人的纳税人识别号。 |
| header.receiver_kpp | string | 收款人的纳税人登记原因代码。 |
| header.receiver_name | string | 收款人名称。 |
| header.start_date | string | 期间开始。 |
| header.stop_date | string | 期间结束。 |
| header.vat_amount | number | 应计金额中包含的增值税金额。 |
| rows | v1GetRealizationReportPostingResponseRow[] | 报告表格。 |
| rows[] | v1GetRealizationReportPostingResponseRow[] | 报告表格。 |
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
| rows[].row_number | integer | 报告中的行号。 |
| rows[].seller_price_per_instance | number | 考虑折扣后的卖家价格。 |
| rows[].order | RowItemOrder | - |
| rows[].order.posting_number | string | 货件编号。 |
| rows[].order.created_date | string | 订单日期格式为`YYYY-MM-DD`。 |
| rows[].legal_entity_document | RowItemLegalEntityDocument | - |
| rows[].legal_entity_document.number | string | 发票编号。 |
| rows[].legal_entity_document.sale_date | string | 日期格式为`YYYY-MM-DD`。 |


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
  "header": {
    "contract_date": "string",
    "contract_number": "string",
    "currency_sys_name": "string",
    "doc_amount": 0,
    "doc_date": "string",
    "number": "string",
    "payer_inn": "string",
    "payer_kpp": "string",
    "payer_name": "string",
    "receiver_inn": "string",
    "receiver_kpp": "string",
    "receiver_name": "string",
    "start_date": "string",
    "stop_date": "string",
    "vat_amount": 0
  },
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
      "row_number": 0,
      "seller_price_per_instance": 0,
      "order": {
        "posting_number": null,
        "created_date": null
      },
      "legal_entity_document": {
        "number": null,
        "sale_date": null
      }
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863064.md

---

## 交易清单

### 接口说明

请使用顺序发送请求的方式。
返回所有应计项目的详细信息。 在一次请求中可获取信息的最长时间为1月。
如果请求中未指出 `posting_number`, 那么响应将包含指定时间段内的所有订单或特定订单类型。
与个人中心中的**财务→应计费用**部分相符。

### 接口标题

交易清单

### 接口地址

`POST https://api-seller.ozon.ru/v3/finance/transaction/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | financev3FinanceTransactionListV3Request | 否 | 请求体。 |
| filter | body | FinanceTransactionListV3RequestFilter | 否 | - |
| page | body | integer | 是 | 请求中返回的页码。 |
| page_size | body | integer | 是 | 每页的元素数。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | financev3FinanceTransactionListV3ResponseResult | - |
| result.operations | FinanceTransactionListV3ResponseOperation[] | 操作信息。 |
| result.operations[] | FinanceTransactionListV3ResponseOperation[] | 操作信息。 |
| result.operations[].accruals_for_sale | number | 考虑到卖家折扣的商品成本。 |
| result.operations[].amount | number | 交易总额。 |
| result.operations[].delivery_charge | number | 适用于2021年2月1日之前有效的关税以及大件商品的运费。 |
| result.operations[].items | OperationItem[] | 商品信息。 |
| result.operations[].items[] | OperationItem[] | 商品信息。 |
| result.operations[].operation_date | string | 操作日期。 |
| result.operations[].operation_id | integer | 操作ID。 |
| result.operations[].operation_type | string | 操作类型。 |
| result.operations[].operation_type_name | string | 操作类型名称。 |
| result.operations[].posting | OperationPosting | - |
| result.operations[].posting.delivery_schema | string | 发货方案：<br>- `FBO` — 从Ozon仓库发货，<br>- `FBS` — 从您的仓库发货，<br>- `RFBS` —  按买方选择发货，<br>- `CROSSBORDER` — 跨境配送，<br>- `FBP` — 通过 Ozon 合作仓库配送，<br>- `FBOECONOMY` — 通过 Ozon 仓库配送经济型商品，<br>- `FBSECONOMY` — 通过自有仓库配送经济商品。 |
| result.operations[].posting.order_date | string | 接收处理货物日期。 |
| result.operations[].posting.posting_number | string | 发货号。 |
| result.operations[].posting.warehouse_id | integer | 仓库ID。 |
| result.operations[].return_delivery_charge | number | 退货和取消订单费用适用于2021年2月1日之前有效的费率，以及超大商品的费用。 |
| result.operations[].sale_commission | number | 销售提成或销售提成返还。 |
| result.operations[].services | OperationService[] | 附加服务。 |
| result.operations[].services[] | OperationService[] | 附加服务。 |
| result.operations[].type | string | 收费类型：<br>- `all` — 所有,<br>- `orders` — 订单,<br>- `returns` — 退货和取消订单,<br>- `services` — 服务费,<br>- `compensation` — 补贴,<br>- `transferDelivery` — 快递价格,<br>- `other` — 其他。 |
| result.page_count | integer | 页数。如果为0，则说明已无页面。 |
| result.row_count | integer | 所有页面上的交易数量。如果为0，说明已无交易。 |


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
    "operations": [
      {
        "operation_id": 11401182187840,
        "operation_type": "MarketplaceMarketingActionCostOperation",
        "operation_date": "2021-11-01 00:00:00",
        "operation_type_name": "商品推销服务",
        "delivery_charge": 0,
        "return_delivery_charge": 0,
        "accruals_for_sale": 0,
        "sale_commission": 0,
        "amount": -6.46,
        "type": "services",
        "posting": {
          "delivery_schema": "",
          "order_date": "",
          "posting_number": "",
          "warehouse_id": 0
        },
        "items": [],
        "services": []
      }
    ],
    "page_count": 1,
    "row_count": 355
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998417.md

---

## 清单数目

### 接口说明

返回指定时间的清单总数。
与个人中心中的**财务→应计费用→总金额横幅**部分相符。

### 接口标题

清单数目

### 接口地址

`POST https://api-seller.ozon.ru/v3/finance/transaction/totals`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | financev3FinanceTransactionTotalsV3Request | 否 | 请求体。 |
| value | body | object | 否 | - |
| value | body | string | 否 | - |
| value | body | string | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | financev3FinanceTransactionTotalsV3ResponseResult | - |
| result.accruals_for_sale | number | 指定期间内商品的总成本和退货。 |
| result.compensation_amount | number | 补贴。 |
| result.money_transfer | number | 根据“卖方选择交货”计划工作时的交货和退货费用。 |
| result.others_amount | number | 其他应计费用。 |
| result.processing_and_delivery | number | 运输处理、订单装配、干线、最后一英里以及自2021年2月1日起引入新的佣金和费率前的快递服务费。<br>干线 —— 集群之间的货物交付。<br>最后一英里 —— 从订单交付点、自提点和快递员到买家处的快递。 |
| result.refunds_and_cancellations | number | 干线返回、退货处理、取消和非赎回、2021年2月1日起引入新佣金和税率之前退货价格。<br>干线 —— 集群之间的货物交付。<br>最后一英里 —— 从订单交付点、自提点和快递员到买家处的快递。 |
| result.sale_commission | number | 商品预售时预扣的佣金数额，退货时返还的佣金数。 |
| result.services_amount | number | 与商品交付和退货没有直接关系的附加服务成本。例如，促销或商品放置。 |


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
    "accruals_for_sale": 96647.58,
    "sale_commission": -11456.65,
    "processing_and_delivery": -24405.68,
    "refunds_and_cancellations": -330,
    "services_amount": -1307.57,
    "compensation_amount": 0,
    "money_transfer": 0,
    "others_amount": 113.05
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998418.md

---
