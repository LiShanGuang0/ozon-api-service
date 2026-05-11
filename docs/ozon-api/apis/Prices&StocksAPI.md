# Prices&StocksAPI

接口数量：7

## 接口列表

- [更新库存商品的数量](#更新库存商品的数量) - `POST /v2/products/stocks`
- [关于商品数量的信息](#关于商品数量的信息) - `POST /v4/product/info/stocks`
- [关于卖家库存余额的信息](#关于卖家库存余额的信息) - `POST /v1/product/info/stocks-by-warehouse/fbs`
- [更新价格](#更新价格) - `POST /v1/product/import/prices`
- [获取商品价格信息](#获取商品价格信息) - `POST /v5/product/info/prices`
- [通过减价商品的SKU查找减价商品和主商品的信息](#通过减价商品的sku查找减价商品和主商品的信息) - `POST /v1/product/info/discounted`
- [为打折商品设置折扣](#为打折商品设置折扣) - `POST /v1/product/update/discount`

## 更新库存商品的数量

### 接口说明

可以改变一个商品的库存数量信息。
转交库存数量是当前可用库存，不包括已预留库存。在更新库存之前，请使用以下方法检查已预留库存数量：/v1/product/info/stocks-by-warehouse/fbs。
在一次查询中最多可以改变100个商品。从一个卖家账号每分钟可以发送不超过80次请求。
您只能每 30 秒钟更新1次仓库中的货物库存，否则响应将显示错误：TOO_MANY_REQUESTS。
只有当一个商品的状态改变为 `price_sent` 时，才有可能设置其可用性。
大件商品的库存只能在其指定的库存地点更新。
如果请求中同时包含参数 `offer_id` 和 `product_id`，系统将优先根据 `offer_id` 应用更改。为避免歧义，建议仅使用一个参数。

### 接口标题

更新库存商品的数量

### 接口地址

`POST https://api-seller.ozon.ru/v2/products/stocks`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productv2ProductsStocksRequest | 否 | 请求体。 |
| stocks | body | productv2ProductsStocksRequestStock[] | 是 | 仓库中商品的信息。 |
| stocks[] | body | productv2ProductsStocksRequestStock[] | 否 | 仓库中商品的信息。 |
| stocks[].offer_id | body | string | 否 | 卖家系统中的商品编号是 — 商品代码。 |
| stocks[].product_id | body | integer | 是 | 卖家系统中的商品标识符 — `product_id`。 |
| stocks[].stock | body | integer | 是 | 扣除预留库存后的可售商品数量。 |
| stocks[].warehouse_id | body | integer | 是 | 得出的仓库编号的方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productv2ProductsStocksResponseResult[] | - |
| result[] | productv2ProductsStocksResponseResult[] | - |
| result[].errors | productv2ProductsStocksResponseError[] | 在搜索处理过程中发生的数组错误。 |
| result[].errors[] | productv2ProductsStocksResponseError[] | 在搜索处理过程中发生的数组错误。 |
| result[].errors[].code | string | 错误代码。 |
| result[].errors[].message | string | 错误原因。 |
| result[].offer_id | string | 卖家系统中的商品编号是 — 商品代码。 |
| result[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result[].updated | boolean | 如果商品信息已被成功更新 — `true`。 |
| result[].warehouse_id | integer | 仓库编号。 |


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
  "result": [
    {
      "warehouse_id": 22142605386000,
      "product_id": 118597312,
      "offer_id": "PH11042",
      "updated": true,
      "errors": []
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998335.md

---

## 关于商品数量的信息

### 接口说明

返回关于 FBS 和 rFBS 方案下商品数量的信息:
- 有多少现货。
- 给买家保留了多少。

### 接口标题

关于商品数量的信息

### 接口地址

`POST https://api-seller.ozon.ru/v4/product/info/stocks`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v4GetProductInfoStocksRequest | 否 | 请求体。 |
| cursor | body | string | 否 | 后续数据的选择标志。 |
| filter | body | v4GetProductInfoStocksRequestFilter | 是 | - |
| filter.offer_id | body | string[] | 否 | 基于参数 `offer_id` 的过滤。 可以提交数值列表。 |
| filter.offer_id[] | body | string[] | 否 | 基于参数 `offer_id` 的过滤。 可以提交数值列表。 |
| filter.product_id | body | string[] | 否 | 基于参数 `product_id` 的过滤。 可以提交数值列表。 |
| filter.product_id[] | body | string[] | 否 | 基于参数 `product_id` 的过滤。 可以提交数值列表。 |
| filter.visibility | body | v4Visibility | 否 | - |
| filter.with_quant | body | FilterWithQuant | 否 | - |
| filter.with_quant.created | body | boolean | 否 | 处于活跃状态的经济商品。 |
| filter.with_quant.exists | body | boolean | 否 | 所有状态下的经济商品。 |
| limit | body | integer | 是 | 页面上的值数量。最低为1，最高为1000。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| cursor | string | 后续数据的选择标志。 |
| items | v4GetProductInfoStocksResponseItem[] | 商品信息。 |
| items[] | v4GetProductInfoStocksResponseItem[] | 商品信息。 |
| items[].offer_id | string | 卖家系统中的商品识别符——货号。 |
| items[].product_id | integer | 商品识别符。 |
| items[].stocks | GetProductInfoStocksResponseStock[] | 库存信息。 |
| items[].stocks[] | GetProductInfoStocksResponseStock[] | 库存信息。 |
| items[].stocks[].present | integer | 现在在仓库中。 |
| items[].stocks[].reserved | integer | 已预定。 |
| items[].stocks[].shipment_type | StockShipmentType | - |
| items[].stocks[].sku | integer | Ozon系统中的商品识别符——SKU。 |
| items[].stocks[].type | string | 仓库类型。 |
| total | integer | 显示库存信息的独特商品数量。 |


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
  "items": [
    {
      "offer_id": "string",
      "product_id": 0,
      "stocks": [
        null
      ]
    }
  ],
  "total": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863051.md

---

## 关于卖家库存余额的信息

### 接口说明

暂无接口说明。

### 接口标题

关于卖家库存余额的信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/info/stocks-by-warehouse/fbs`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productsv1GetProductInfoStocksByWarehouseFbsRequest | 否 | 请求体。 |
| sku | body | string[] | 是 | Ozon系统中的商品识别码是SKU。 |
| sku[] | body | string[] | 否 | Ozon系统中的商品识别码是SKU。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productsv1GetProductInfoStocksByWarehouseFbsResponseResult[] | 该处理方法的结果。 |
| result[] | productsv1GetProductInfoStocksByWarehouseFbsResponseResult[] | 该处理方法的结果。 |
| result[].sku | integer | Ozon系统中的商品识别码是SKU。 |
| result[].present | integer | 库存商品总量。 |
| result[].product_id | integer | 卖家系统中的卖家系统中的商品标识符 — `product_id`。 |
| result[].reserved | integer | 仓库中的保留商品的数量。 |
| result[].warehouse_id | integer | 仓库编号。 |
| result[].warehouse_name | string | 仓库名称。 |


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
  "result": [
    {
      "sku": 0,
      "present": 0,
      "product_id": 0,
      "reserved": 0,
      "warehouse_id": 0,
      "warehouse_name": "string"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998337.md

---

## 更新价格

### 接口说明

允许更改一个或多个商品的价格。每个商品的价格每小时不能更新超过10次。要重置`old_price`，请将此参数设为0。
如果请求中同时包含参数 `offer_id` 和 `product_id`，系统将优先根据 `offer_id` 应用更改。为避免歧义，建议仅使用一个参数。

### 接口标题

更新价格

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/import/prices`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productImportProductsPricesRequest | 否 | 请求体。 |
| prices | body | productImportProductsPricesRequestPrice[] | 否 | 商品价格信息。 |
| prices[] | body | productImportProductsPricesRequestPrice[] | 否 | 商品价格信息。 |
| prices[].auto_action_enabled | body | enum(UNKNOWN, ENABLED, DISABLED) | 否 | 启用和禁用自动应用活动的属性：<br>- `ENABLED` — 启用;<br>- `DISABLED` — 关闭;<br>- `UNKNOWN` — 不做任何更改，默认赋值。<br>例如，如果你以前启用了活动的自动应用，并且不想关闭它，请提交`UNKNOWN`。<br>如果你在这个参数中提交`ENABLED`，在`min_price`参数中设置最低价格。 |
| prices[].currency_code | body | string | 否 | 您的价格的货币。提交的数值必须与你个人主页设置中的货币相匹配。默认情况下，会提交 `RUB` — 俄罗斯卢布。<br>例如，如果您设置的相互结算的货币是人民币，请提交数值 `CNY`，否则将返回错误。<br>可填的数值：<br>- `RUB` — 俄罗斯卢布。<br>- `BYN` — 白俄罗斯卢布。<br>- `KZT` — 坚戈。<br>- `EUR' — 欧元。<br>- `USD` — 美元。<br>- `CNY` — 人民币。 |
| prices[].min_price | body | string | 否 | 应用促销活动后的商品最低价格。 |
| prices[].min_price_for_auto_actions_enabled | body | boolean | 否 | `true`，如果为 Ozon 在添加到促销时会考虑最低价格。如果不传递任何值，价格计算的状态将保持不变。 |
| prices[].net_price | body | string | 否 | 产品成本价。 |
| prices[].offer_id | body | string | 否 | 卖家系统中的卖家系统中的商品标识符 — `product_id`。 |
| prices[].old_price | body | string | 否 | 折扣前的价格（在商品卡上划掉）价格以卢布表。小数部分用一个点隔开，点后最多两个字符。<br>如果商品没有折扣，在这个字段中输入 "0"，并将当前价格提交到 "price"栏中。 |
| prices[].price | body | string | 否 | 商品的价格，包括折扣，都显示在商品详情页上。<br>若参数`old_price`值大于0,则`price`与`old_price`之间应为具体差额。<br>差额取决于`price`值。<br>\| `price`值 \| 最小差额 \|<br>\|---\|---\|<br>\|  10 000 \| 500 卢布 \| |
| prices[].price_strategy_enabled | body | enum(UNKNOWN, ENABLED, DISABLED) | 否 | 用于自动应用价格策略的属性：<br>- `ENABLED` — 启用;<br>- `DISABLED` — 关闭;<br>- `UNKNOWN` — 不做任何更改，默认赋值。<br>如果您之前已启用价格策略的自动应用，并且不希望关闭，请在后续请求中赋值 `UNKNOWN` 。<br>如果你在这个参数中提交`ENABLED`，在`min_price`参数中设置最低价格。<br>如果您在此参数中赋值 `DISABLED`，商品将从策略中移除。 |
| prices[].product_id | body | integer | 否 | 卖家系统中的商品标识符 — `product_id`。 |
| prices[].vat | body | string | 否 | 商品增值税税率：<br>- `0` — 免除增值税,<br>- `0.05` — 5%,<br>- `0.07` — 7%,<br>- `0.1` — 10%,<br>- `0.2` — 20%。<br>传递当前有效的出价值。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productImportProductsPricesResponseProcessResult[] | 搜索结果。 |
| result[] | productImportProductsPricesResponseProcessResult[] | 搜索结果。 |
| result[].errors | productImportProductsPricesResponseError[] | 在搜索处理过程中发生的数组错误。 |
| result[].errors[] | productImportProductsPricesResponseError[] | 在搜索处理过程中发生的数组错误。 |
| result[].errors[].code | string | 错误代码。 |
| result[].errors[].message | string | 错误原因。 |
| result[].offer_id | string | 卖家系统中的商品编号是 — 商品代码。 |
| result[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result[].updated | boolean | 如果商品信息已被成功更新 — `true`。 |


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
  "result": [
    {
      "product_id": 1386,
      "offer_id": "PH8865",
      "updated": true,
      "errors": []
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998338.md

---

## 获取商品价格信息

### 接口说明

暂无接口说明。

### 接口标题

获取商品价格信息

### 接口地址

`POST https://api-seller.ozon.ru/v5/product/info/prices`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productv5GetProductInfoPricesV5Request | 否 | 请求体。 |
| cursor | body | string | 否 | 用于选择数据的指针。 |
| filter | body | productv5Filter | 是 | - |
| filter.offer_id | body | string[] | 否 | 基于 `offer_id` 参数的筛选（最多可传递 1000 个值）。 |
| filter.offer_id[] | body | string[] | 否 | 基于 `offer_id` 参数的筛选（最多可传递 1000 个值）。 |
| filter.product_id | body | string[] | 否 | 基于 `product_id` 参数的筛选（最多可传递 1000 个值）。 |
| filter.product_id[] | body | string[] | 否 | 基于 `product_id` 参数的筛选（最多可传递 1000 个值）。 |
| filter.visibility | body | productv5GetProductListRequestFilterFilterVisibility | 否 | - |
| limit | body | integer | 是 | 每页显示的数值数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| cursor | string | 用于选择数据的指针。 |
| items | productGetProductInfoPricesV5ResponseItem[] | 商品列表。 |
| items[] | productGetProductInfoPricesV5ResponseItem[] | 商品列表。 |
| items[].acquiring | integer | 最高收单手续费。 |
| items[].commissions | ItemCommissionsv5 | - |
| items[].commissions.fbo_deliv_to_customer_amount | number | 尾程物流 (FBO)。 |
| items[].commissions.fbo_direct_flow_trans_max_amount | number | 干线运输至仓 (FBO)。 |
| items[].commissions.fbo_direct_flow_trans_min_amount | number | 干线运输出仓 (FBO)。 |
| items[].commissions.fbo_return_flow_amount | number | 退货及取消订单手续费 (FBO)。 |
| items[].commissions.fbs_deliv_to_customer_amount | number | 尾程物流 (FBS)。 |
| items[].commissions.fbs_direct_flow_trans_max_amount | number | 干线运输至仓 (FBS)。 |
| items[].commissions.fbs_direct_flow_trans_min_amount | number | 干线运输出仓 (FBS)。 |
| items[].commissions.fbs_first_mile_max_amount | number | 货件处理最高佣金 (FBS)。 |
| items[].commissions.fbs_first_mile_min_amount | number | 货件处理最低佣金 (FBS)。 |
| items[].commissions.fbs_return_flow_amount | number | 退货及取消货件佣金，货件处理费用 (FBS)。 |
| items[].commissions.sales_percent_fbo | number | 销售佣金比例 (FBO)。 |
| items[].commissions.sales_percent_fbs | number | 销售佣金比例 (FBS)。 |
| items[].marketing_actions | ItemMarketing | 卖家营销活动。 |
| items[].marketing_actions.actions | MarketingAction[] | 卖家营销活动。 `date_from`, `date_to`, `title` 和 `value` 为每个营销活动单独指定。 |
| items[].marketing_actions.actions[] | MarketingAction[] | 卖家营销活动。 `date_from`, `date_to`, `title` 和 `value` 为每个营销活动单独指定。 |
| items[].offer_id | string | 商品在卖家系统中的标识符 — 货号。 |
| items[].price | ItemPricev5 | - |
| items[].price.auto_action_enabled | boolean | 如果商品启用了促销活动的自动应用，则为 `true`。 |
| items[].price.currency_code | string | 您的定价货币（与个人中心设置中指定的货币相同）。<br>可能的值：<br>- `RUB` — 俄罗斯卢布，<br>- `BYN` — 白俄罗斯卢布，<br>- `KZT` — 坚戈，<br>- `EUR` — 欧元，<br>- `USD` — 美元，<br>- `CNY` — 人民币。 |
| items[].price.marketing_price | number | 商品在 Ozon 橱窗中的最终价格，包含所有促销折扣，但不含Ozon 卡优惠。 |
| items[].price.marketing_seller_price | number | 包含卖家促销的商品价格。 |
| items[].price.min_price | number | 商品在应用所有折扣后的最低价格。 |
| items[].price.net_price | number | 商品成本。 |
| items[].price.old_price | number | 未应用折扣前的价格（在商品卡片显示为划线价）。 |
| items[].price.price | number | 包含折扣的商品价格（在商品卡片展示的实际售价）。 |
| items[].price.retail_price | number | 供应商价格。 |
| items[].price.vat | number | 商品的增值税税率。 |
| items[].price_indexes | GetProductInfoPricesResponseItemPriceIndexes | - |
| items[].price_indexes.color_index | enum(WITHOUT_INDEX, GREEN, YELLOW, RED) | 最终价格指数：<br>- `WITHOUT_INDEX` — 无价格指数，<br>- `GREEN` — 有利，<br>- `YELLOW` — 中等，<br>- `RED` — 不利。 |
| items[].price_indexes.external_index_data | PriceIndexesIndexExternalData | - |
| items[].price_indexes.external_index_data.min_price | string | 竞争对手在其他平台上的最低商品价格。 |
| items[].price_indexes.external_index_data.min_price_currency | string | 价格的货币单位。 |
| items[].price_indexes.external_index_data.price_index_value | number | 价格指数值。 |
| items[].price_indexes.ozon_index_data | PriceIndexesIndexOzonData | - |
| items[].price_indexes.ozon_index_data.min_price | string | Ozon 上竞争对手的最低商品价格。 |
| items[].price_indexes.ozon_index_data.min_price_currency | string | 价格的货币单位。 |
| items[].price_indexes.ozon_index_data.price_index_value | number | 价格指数值。 |
| items[].price_indexes.self_marketplaces_index_data | PriceIndexesIndexSelfData | - |
| items[].price_indexes.self_marketplaces_index_data.min_price | string | 您的商品在其他平台上的最低价格。 |
| items[].price_indexes.self_marketplaces_index_data.min_price_currency | string | 价格的货币单位。 |
| items[].price_indexes.self_marketplaces_index_data.price_index_value | number | 价格指数值。 |
| items[].product_id | integer | 商品在卖家系统中的标识符 — `product_id`。 |
| items[].volume_weight | number | 商品体积重量。 |
| total | integer | 商品列表中的商品数量。 |


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
  "cursor": "string",
  "items": [
    {
      "acquiring": 0,
      "commissions": {
        "fbo_deliv_to_customer_amount": 14.75,
        "fbo_direct_flow_trans_max_amount": 46.5,
        "fbo_direct_flow_trans_min_amount": 31,
        "fbo_return_flow_amount": 50,
        "fbs_deliv_to_customer_amount": 60,
        "fbs_direct_flow_trans_max_amount": 61.5,
        "fbs_direct_flow_trans_min_amount": 41,
        "fbs_first_mile_max_amount": 25,
        "fbs_first_mile_min_amount": 0,
        "fbs_return_flow_amount": 40,
        "sales_percent_fbo": 15,
        "sales_percent_fbs": 0
      },
      "marketing_actions": {
        "actions": [
          {
            "date_from": "2024-12-13T06:49:37.591Z",
            "date_to": "2024-12-13T06:49:37.591Z",
            "title": "string",
            "value": 0
          }
        ],
        "current_period_from": "2024-12-13T06:49:37.591Z",
        "current_period_to": "2024-12-13T06:49:37.591Z",
        "ozon_actions_exist": true
      },
      "offer_id": "356792",
      "price": {
        "auto_action_enabled": true,
        "currency_code": "RUB",
        "marketing_price": 0,
        "marketing_seller_price": 0,
        "min_price": 0,
        "net_price": 0,
        "old_price": 579,
        "price": 499,
        "retail_price": 0,
        "vat": 0.2
      },
      "price_indexes": {
        "color_index": "WITHOUT_INDEX",
        "external_index_data": {
          "min_price": 0,
          "min_price_currency": "string",
          "price_index_value": 0
        },
        "ozon_index_data": {
          "min_price": 0,
          "min_price_currency": "string",
          "price_index_value": 0
        },
        "self_marketplaces_index_data": {
          "min_price": 0,
          "min_price_currency": "string",
          "price_index_value": 0
        }
      },
      "product_id": 243686911,
      "volume_weight": 0
    }
  ],
  "total": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863052.md

---

## 通过减价商品的SKU查找减价商品和主商品的信息

### 接口说明

一种通过SKU获取打折商品的状况和缺陷信息的方法。该方法还返回主商品的SKU。

### 接口标题

通过减价商品的SKU查找减价商品和主商品的信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/info/discounted`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetProductInfoDiscountedRequest | 否 | 请求体。 |
| discounted_skus | body | string[] | 是 | 降价的商品SKU清单。 |
| discounted_skus[] | body | string[] | 否 | 降价的商品SKU清单。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| items | v1GetProductInfoDiscountedResponseItem[] | 关于减价和主要商品的信息。 |
| items[] | v1GetProductInfoDiscountedResponseItem[] | 关于减价和主要商品的信息。 |
| items[].comment_reason_damaged | string | 对损坏原因的评论。 |
| items[].condition | string | 商品的状态 — 新的或二手的。 |
| items[].condition_estimation | string | 商品的状况，以1至7分为标准。<br>- 1 — 令人满意。<br>- 2 — 良好。<br>- 3 — 非常好。<br>- 4 — 优秀。<br>- 5-7 — 像新的一样。 |
| items[].defects | string | 商品缺陷。 |
| items[].discounted_sku | integer | 折扣商品的SKU。 |
| items[].mechanical_damage | string | 机械性损坏的说明。 |
| items[].package_damage | string | 包装损坏的说明。 |
| items[].packaging_violation | string | 篡改包装的痕迹。 |
| items[].reason_damaged | string | 损害原因。 |
| items[].repair | string | 商品已被修理的痕迹。 |
| items[].shortage | string | 表示商品不完整。 |
| items[].sku | integer | 主要商品的SKU。 |
| items[].warranty_type | string | 商品有有效保修的证明。 |


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
  "items": [
    {
      "discounted_sku": 635548518,
      "sku": 320067758,
      "condition_estimation": "4",
      "packaging_violation": "",
      "warranty_type": "",
      "reason_damaged": "Механическое повреждение",
      "comment_reason_damaged": "повреждена заводская упаковка",
      "defects": "",
      "mechanical_damage": "",
      "package_damage": "",
      "shortage": "",
      "repair": "",
      "condition": ""
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998340.md

---

## 为打折商品设置折扣

### 接口说明

FBS模式下出售折扣商品的折扣幅度设置方法。

### 接口标题

为打折商品设置折扣

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/update/discount`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductUpdateDiscountRequest | 否 | 请求体。 |
| discount | body | integer | 是 | 折扣力度：从3%到99%。 |
| product_id | body | integer | 是 | 卖家系统中的商品标识符 — `product_id`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 方式工作结果 `true`, 如果正确完成请求。 |


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
  "result": false
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998341.md

---
