# PricingStrategyAPI

接口数量：12

## 接口列表

- [竞争对手名单](#竞争对手名单) - `POST /v1/pricing-strategy/competitors/list`
- [策略列表](#策略列表) - `POST /v1/pricing-strategy/list`
- [创建策略](#创建策略) - `POST /v1/pricing-strategy/create`
- [策略信息](#策略信息) - `POST /v1/pricing-strategy/info`
- [更新策略](#更新策略) - `POST /v1/pricing-strategy/update`
- [将商品添加到策略](#将商品添加到策略) - `POST /v1/pricing-strategy/products/add`
- [策略ID列表](#策略id列表) - `POST /v1/pricing-strategy/strategy-ids-by-product-ids`
- [策略中的商品列表](#策略中的商品列表) - `POST /v1/pricing-strategy/products/list`
- [竞争对手  的商品价格](#竞争对手-的商品价格) - `POST /v1/pricing-strategy/product/info`
- [从策略中删除商品](#从策略中删除商品) - `POST /v1/pricing-strategy/products/delete`
- [更改策略状态](#更改策略状态) - `POST /v1/pricing-strategy/status`
- [删除策略](#删除策略) - `POST /v1/pricing-strategy/delete`

## 竞争对手名单

### 接口说明

获取竞争对手列表的方法 - 在其他在线商店和电商平台上拥有类似商品的卖家。

### 接口标题

竞争对手名单

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/competitors/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetCompetitorsRequest | 否 | 请求体。 |
| page | body | integer | 是 | 需要下载竞争对手的列表页面。 最小值为`1`。 |
| limit | body | integer | 是 | 每页的最大竞争对手数。有效值是从`1`到`50`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| competitor | GetCompetitorsResponseCompetitorInfo[] | 竞争对手列表。 |
| competitor[] | GetCompetitorsResponseCompetitorInfo[] | 竞争对手列表。 |
| competitor[].name | string | 竞争对手名称。 |
| competitor[].id | integer | 竞争对手ID。 |
| total | integer | 竞争对手总数。 |


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
  "competitor": [
    {
      "competitor_name": "string",
      "competitor_id": 0
    }
  ],
  "total": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998354.md

---

## 策略列表

### 接口说明

暂无接口说明。

### 接口标题

策略列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetStrategyListRequest | 否 | 请求体。 |
| page | body | integer | 是 | 卸载策略的列表页面。 最小值为`1`。 |
| limit | body | integer | 是 | 每页的最大策略数。有效值是从`1`到`50`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| strategies | GetStrategyListResponseStrategy[] | 策略列表。 |
| strategies[] | GetStrategyListResponseStrategy[] | 策略列表。 |
| strategies[].id | string | 策略ID。 |
| strategies[].name | string | 策略名称。 |
| strategies[].type | string | 策略类型：<br>- `MIN_EXT_PRICE` —— 系统性，<br>- `COMP_PRICE` —— 用户性。 |
| strategies[].update_type | string | 策略最后变化的类型:<br>- `strategyEnabled` — 恢复，<br>- `strategyDisabled` — 停止，<br>- `strategyChanged` — 更新，<br>- `strategyCreated` — 创建，<br>- `strategyItemsListChanged` — 策略中的商品集合已更改。 |
| strategies[].updated_at | string | 最后一次修改的日期。 |
| strategies[].products_count | integer | 策略中的商品数量。 |
| strategies[].competitors_count | integer | 选择的竞争对手数量。 |
| strategies[].enabled | boolean | 策略状态：<br>- `true` —— 开启，<br>- `false` —— 关闭。 |
| total | integer | 策略总数。 |


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
  "strategies": [
    {
      "strategy_id": "string",
      "strategy_name": "string",
      "type": "string",
      "update_type": "string",
      "updated_at": "string",
      "products_count": 0,
      "competitors_count": 0,
      "enabled": true
    }
  ],
  "total": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998355.md

---

## 创建策略

### 接口说明

暂无接口说明。

### 接口标题

创建策略

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1CreatePricingStrategyRequest | 否 | 请求体。 |
| competitors | body | v1Competitor[] | 是 | 竞争对手名单。 |
| competitors[] | body | v1Competitor[] | 否 | 竞争对手名单。 |
| competitors[].coefficient | body | number | 是 | 竞争对手之间的最低价格将乘以的系数。有效范围是`0.5`到`1.2`。 |
| competitors[].competitor_id | body | integer | 是 | 竞争对手ID。 |
| strategy_name | body | string | 是 | 策略名称。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1CreatePricingStrategyResponseResult | - |
| result.strategy_id | string | 策略ID。 |


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
    "id": "4f3a1d4c-5833-4f04-b69b-495cbc1f6f1c"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998356.md

---

## 策略信息

### 接口说明

暂无接口说明。

### 接口标题

策略信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1StrategyRequest | 否 | 请求体。 |
| strategy_id | body | string | 是 | 策略ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetStrategyResponseResult | - |
| result.competitors | v1Competitor[] | 竞争对手列表。 |
| result.competitors[] | v1Competitor[] | 竞争对手列表。 |
| result.competitors[].coefficient | number | 竞争对手之间的最低价格将乘以的系数。有效范围是`0.5`到`1.2`。 |
| result.competitors[].competitor_id | integer | 竞争对手ID。 |
| result.enabled | boolean | 策略状态：<br>- `true` —— 打开，<br>- `false` —— 关闭。 |
| result.name | string | 策略名称。 |
| result.type | string | 策略类型：<br>- `MIN_EXT_PRICE` —— 系统策略，<br>- `COMP_PRICE` —— 用户策略。 |
| result.update_type | string | 上次策略更改的类型：<br>- `strategyEnabled` —— 恢复，<br>- `strategyDisabled` —— 停止，<br>- `strategyChanged` —— 更新，<br>- `strategyCreated` —— 创建，<br>- `strategyItemsListChanged` —— 策略中的商品集合已更改。 |


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
    "strategy_name": "тест1",
    "enabled": true,
    "update_type": "strategyItemsListChanged",
    "type": "COMP_PRICE",
    "competitors": [
      {
        "competitor_id": 204,
        "coefficient": 1
      },
      {
        "competitor_id": 1008426,
        "coefficient": 1
      }
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998357.md

---

## 更新策略

### 接口说明

可以更新除系统策略之外的所有策略。

### 接口标题

更新策略

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/update`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1UpdatePricingStrategyRequest | 否 | 请求体。 |
| competitors | body | v1Competitor[] | 是 | 竞争对手列表。 |
| competitors[] | body | v1Competitor[] | 否 | 竞争对手列表。 |
| competitors[].coefficient | body | number | 是 | 竞争对手之间的最低价格将乘以的系数。有效范围是`0.5`到`1.2`。 |
| competitors[].competitor_id | body | integer | 是 | 竞争对手ID。 |
| strategy_id | body | string | 是 | 策略ID。 |
| strategy_name | body | string | 是 | 策略名称。 |


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

根据响应参数结构生成的示例：

```json
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998358.md

---

## 将商品添加到策略

### 接口说明

暂无接口说明。

### 接口标题

将商品添加到策略

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/products/add`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1AddStrategyItemsRequest | 否 | 请求体。 |
| product_id | body | string[] | 是 | 商品ID列表。 最大数量为 50。 |
| product_id[] | body | string[] | 否 | 商品ID列表。 最大数量为 50。 |
| strategy_id | body | string | 是 | 策略ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1AddStrategyItemsResponseResult | - |
| result.errors | AddStrategyItemsResponseError[] | 有错误的商品。 |
| result.errors[] | AddStrategyItemsResponseError[] | 有错误的商品。 |
| result.errors[].code | string | 错误代码。 |
| result.errors[].error | string | 错误文本。 |
| result.errors[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result.failed_product_count | integer | 有错误的商品数量。 |


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
    "failed_product_count": 0
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998359.md

---

## 策略ID列表

### 接口说明

暂无接口说明。

### 接口标题

策略ID列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/strategy-ids-by-product-ids`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ItemIDsRequest | 否 | 请求体。 |
| product_id | body | string[] | 是 | 商品ID列表。最大数量 —— 50。 |
| product_id[] | body | string[] | 否 | 商品ID列表。最大数量 —— 50。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetStrategyIDsByItemIDsResponseResult | - |
| result.products_info | GetStrategyIDsByItemIDsResponseProductInfo[] | 商品信息。 |
| result.products_info[] | GetStrategyIDsByItemIDsResponseProductInfo[] | 商品信息。 |
| result.products_info[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result.products_info[].strategy_id | string | 添加商品的策略ID。 |


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
    "products_info": [
      {
        "product_id": 29209,
        "strategy_id": "b7cd30e6-5667-424d-b105-fbec30a52477"
      }
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998360.md

---

## 策略中的商品列表

### 接口说明

暂无接口说明。

### 接口标题

策略中的商品列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/products/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1StrategyRequest | 否 | 请求体。 |
| strategy_id | body | string | 是 | 策略ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetStrategyItemsResponseResult | - |
| result.product_id | string[] | 卖家系统中的商品标识符 — `product_id`。 |
| result.product_id[] | string[] | 卖家系统中的商品标识符 — `product_id`。 |


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
    "product_id": [
      "string"
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998361.md

---

## 竞争对手  的商品价格

### 接口说明

如果您向定价策略添加了商品，那么方式将恢复价格和竞争对手商品链接。

### 接口标题

竞争对手  的商品价格

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/product/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetStrategyItemInfoRequest | 否 | 请求体。 |
| product_id | body | integer | 是 | 卖家系统中的商品标识符 — `product_id`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetStrategyItemInfoResponseResult | - |
| result.strategy_id | string | 策略ID。 |
| result.is_enabled | boolean | `true`, 如果商品参与定价策略。 |
| result.strategy_product_price | integer | 定价策略。 |
| result.price_downloaded_at | string | 定价策略设定日期。 |
| result.strategy_competitor_id | integer | 竞争对手ID。 |
| result.strategy_competitor_product_url | string | 竞争对手商品链接。 |


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
    "strategy_id": "string",
    "is_enabled": true,
    "strategy_product_price": 0,
    "price_downloaded_at": "2022-11-17T15:33:53.936Z",
    "strategy_competitor_id": 0,
    "strategy_competitor_product_url": "string"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998362.md

---

## 从策略中删除商品

### 接口说明

暂无接口说明。

### 接口标题

从策略中删除商品

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/products/delete`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ItemIDsRequest | 否 | 请求体。 |
| product_id | body | string[] | 是 | 商品ID列表。最大数量 —— 50。 |
| product_id[] | body | string[] | 否 | 商品ID列表。最大数量 —— 50。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1DeleteStrategyItemsResponseResult | - |
| result.failed_product_count | integer | 有错误的商品数量。 |


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
    "failed_product_count": 0
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998363.md

---

## 更改策略状态

### 接口说明

可以更改除系统策略之外的任何策略的状态。

### 接口标题

更改策略状态

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/status`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1UpdateStatusStrategyRequest | 否 | 请求体。 |
| enabled | body | boolean | 否 | 策略状态：<br>- `true` —— 打开，<br>- `false` —— 关闭。 |
| strategy_id | body | string | 是 | 策略ID。 |


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

根据响应参数结构生成的示例：

```json
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998364.md

---

## 删除策略

### 接口说明

可以删除除系统策略之外的任何策略。

### 接口标题

删除策略

### 接口地址

`POST https://api-seller.ozon.ru/v1/pricing-strategy/delete`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1StrategyRequest | 否 | 请求体。 |
| strategy_id | body | string | 是 | 策略ID。 |


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

根据响应参数结构生成的示例：

```json
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998365.md

---
