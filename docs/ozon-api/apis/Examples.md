# Examples

接口数量：5

## 接口列表

- [检查并保存份数数据](#检查并保存份数数据) - `POST /v6/fbs/posting/product/exemplar/set`
- [获取已创建样件数据](#获取已创建样件数据) - `POST /v6/fbs/posting/product/exemplar/create-or-get`
- [获取样件添加状态](#获取样件添加状态) - `POST /v5/fbs/posting/product/exemplar/status`
- [标志代码验证](#标志代码验证) - `POST /v5/fbs/posting/product/exemplar/validate`
- [Обновить данные экземпляров](#обновить-данные-экземпляров) - `POST /v1/fbs/posting/product/exemplar/update`

## 检查并保存份数数据

### 接口说明

异步方法：
- 检查在“诚信标志”系统中流通份数的存在性；
- 保存份数数据。
为了获取已创建样件的数据，请使用 [/v6/fbs/posting/product/exemplar/create-or-get](#operation/PostingAPI_FbsPostingProductExemplarCreateOrGetV6) 方式。
如果您在一批货件中有多个相同的商品, 请为货件中的每个商品指出一个 `product_id` 和一组 `exemplars`。
请始终传输全套份数和商品数据。
例如，如果在您的系统里有10份。您已赋值并检查和储存。然后在自己的系统中还添加了60份。 当重新提交份数以供审查和保存时，请指出所有新旧份数。
响应代码200并不保证商品数据已被接受。 它表示已创建任务以添加信息。 要检查任务状态，请使用方法 [/v5/fbs/posting/product/exemplar/status](#operation/PostingAPI_FbsPostingProductExemplarStatusV5)。
您可以在 [讨论](https://dev.ozon.ru/community/1269-Metody-dlia-raboty-so-spiskom-markirovok-FBS-rFBS) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

检查并保存份数数据

### 接口地址

`POST https://api-seller.ozon.ru/v6/fbs/posting/product/exemplar/set`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v6FbsPostingProductExemplarSetV6Request | 否 | 请求体。 |
| multi_box_qty | body | integer | 否 | 商品包装的箱子数量。 |
| posting_number | body | string | 否 | 发货号。 |
| products | body | FbsPostingProductExemplarSetV6RequestProducts[] | 否 | 商品清单。 |
| products[] | body | FbsPostingProductExemplarSetV6RequestProducts[] | 否 | 商品清单。 |
| products[].exemplars | body | FbsPostingProductExemplarSetV6RequestExemplars[] | 否 | 副本信息。 |
| products[].exemplars[] | body | FbsPostingProductExemplarSetV6RequestExemplars[] | 否 | 副本信息。 |
| products[].exemplars[].exemplar_id | body | integer | 否 | 样件识别码。 |
| products[].exemplars[].gtd | body | string | 否 | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].is_gtd_absent | body | boolean | 否 | 不需要指出货运报关单（Cargo Customs Declaration）号码的标志。 |
| products[].exemplars[].is_rnpt_absent | body | boolean | 否 | 不需要指出商品批次注册号(Product Batch Registration Number)的标志。 |
| products[].exemplars[].marks | body | ExemplarsMarks[] | 否 | 检查控制识别码时出现的错误。 |
| products[].exemplars[].marks[] | body | ExemplarsMarks[] | 否 | 检查控制识别码时出现的错误。 |
| products[].exemplars[].rnpt | body | string | 否 | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].product_id | body | integer | 否 | Ozon系统中的商品ID — SKU。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863092.md

---

## 获取已创建样件数据

### 接口说明

此方法用于获取货件中商品的信息，这些信息通过方法 [/v6/fbs/posting/product/exemplar/set](#operation/PostingAPI_FbsPostingProductExemplarSetV6) 传递。
请使用此方法获取 `exemplar_id`。
您可以在 [讨论](https://dev.ozon.ru/community/1269-Metody-dlia-raboty-so-spiskom-markirovok-FBS-rFBS) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

获取已创建样件数据

### 接口地址

`POST https://api-seller.ozon.ru/v6/fbs/posting/product/exemplar/create-or-get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v6FbsPostingProductExemplarCreateOrGetV6Request | 否 | 请求体。 |
| posting_number | body | string | 否 | 发货号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| multi_box_qty | integer | 商品包装的箱子数量。 |
| posting_number | string | 发货号。 |
| products | FbsPostingProductExemplarCreateOrGetV6ResponseProduct[] | 商品清单。 |
| products[] | FbsPostingProductExemplarCreateOrGetV6ResponseProduct[] | 商品清单。 |
| products[].exemplars | ProductExemplar[] | 副本信息。 |
| products[].exemplars[] | ProductExemplar[] | 副本信息。 |
| products[].exemplars[].exemplar_id | integer | 样件识别码。 |
| products[].exemplars[].gtd | string | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].is_gtd_absent | boolean | 不需要指出货运报关单（Cargo Customs Declaration）号码的标志。 |
| products[].exemplars[].is_rnpt_absent | boolean | 不需要指出商品批次注册号(Product Batch Registration Number)的标志。 |
| products[].exemplars[].marks | ExemplarMark[] | 检查控制识别码时出现的错误。 |
| products[].exemplars[].marks[] | ExemplarMark[] | 检查控制识别码时出现的错误。 |
| products[].exemplars[].rnpt | string | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].is_gtd_needed | boolean | 说明需要递交产品和货件的货物报关单号码。 |
| products[].is_jw_uin_needed | boolean | 是否需要提供珠宝制品的唯一识别编号。 |
| products[].is_mandatory_mark_needed | boolean | 说明需要将标志递交给“诚实标志”。 |
| products[].is_mandatory_mark_possible | boolean | 是否可以填写“诚实标志”（Chestny ZNAK）信息。 |
| products[].is_rnpt_needed | boolean | 说明需要递交商品批次号码。 |
| products[].product_id | integer | Ozon系统中的商品ID — SKU。 |
| products[].quantity | integer | 样件数量。 |


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
  "multi_box_qty": 0,
  "posting_number": "string",
  "products": [
    {
      "exemplars": [
        null
      ],
      "is_gtd_needed": false,
      "is_jw_uin_needed": false,
      "is_mandatory_mark_needed": false,
      "is_mandatory_mark_possible": false,
      "is_rnpt_needed": false,
      "product_id": 0,
      "quantity": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863093.md

---

## 获取样件添加状态

### 接口说明

获取在 [/v6/fbs/posting/product/exemplar/set](PostingAPI_FbsPostingProductExemplarSetV6) 方式中传输的样件添加状态的方式。
同时还归还这些样件的数据。
您可以在 [讨论](https://dev.ozon.ru/community/1269-Metody-dlia-raboty-so-spiskom-markirovok-FBS-rFBS) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

获取样件添加状态

### 接口地址

`POST https://api-seller.ozon.ru/v5/fbs/posting/product/exemplar/status`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v5FbsPostingProductExemplarStatusV5Request | 否 | 请求体。 |
| posting_number | body | string | 否 | 发货号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| posting_number | string | 发货号。 |
| products | v5FbsPostingProductExemplarStatusV5ResponseProduct[] | 商品清单。 |
| products[] | v5FbsPostingProductExemplarStatusV5ResponseProduct[] | 商品清单。 |
| products[].exemplars | v5FbsPostingProductExemplarStatusV5ResponseProductExemplar[] | 副本信息。 |
| products[].exemplars[] | v5FbsPostingProductExemplarStatusV5ResponseProductExemplar[] | 副本信息。 |
| products[].exemplars[].exemplar_id | integer | 样件识别码。 |
| products[].exemplars[].gtd | string | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].gtd_check_status | string | 货物报关验证状态。 |
| products[].exemplars[].gtd_error_codes | string[] | 货物报关验证错误代码。 |
| products[].exemplars[].gtd_error_codes[] | string[] | 货物报关验证错误代码。 |
| products[].exemplars[].is_gtd_absent | boolean | 这说明没有输入货物报关单号。 |
| products[].exemplars[].is_rnpt_absent | boolean | 不需要指出商品批次注册号(Product Batch Registration Number)的标志。 |
| products[].exemplars[].marks | v5FbsPostingProductExemplarStatusV5ResponseProductExemplarMark[] | 单个实例中的控制识别码列表。 |
| products[].exemplars[].marks[] | v5FbsPostingProductExemplarStatusV5ResponseProductExemplarMark[] | 单个实例中的控制识别码列表。 |
| products[].exemplars[].rnpt | string | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].exemplars[].rnpt_check_status | string | 商品批次注册编号验证状态。 |
| products[].exemplars[].rnpt_error_codes | string[] | 商品批次注册编号验证错误代码。 |
| products[].exemplars[].rnpt_error_codes[] | string[] | 商品批次注册编号验证错误代码。 |
| products[].product_id | integer | Ozon系统中的商品ID — SKU。 |
| status | string | 所有样件和备货可用性的验证状态：<br>- `ship_available` ——可以备货，<br>- `ship_not_available` ——无法备货，<br>- `validation_in_process` ——样件正在验证中。 |


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
  "posting_number": "string",
  "products": [
    {
      "exemplars": [
        null
      ],
      "product_id": 0
    }
  ],
  "status": "string"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863094.md

---

## 标志代码验证

### 接口说明

这是一种验证代码是否符合“诚信标志”系统对字符数量和组成方面要求的方式。
如果您没有货物报关单号，那么您可以不输入。
您可以在 [讨论](https://dev.ozon.ru/community/1269-Metody-dlia-raboty-so-spiskom-markirovok-FBS-rFBS) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

标志代码验证

### 接口地址

`POST https://api-seller.ozon.ru/v5/fbs/posting/product/exemplar/validate`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v5FbsPostingProductExemplarValidateV5Request | 否 | 请求体。 |
| posting_number | body | string | 否 | 发货号。 |
| products | body | v5FbsPostingProductExemplarValidateV5RequestProduct[] | 否 | 商品清单。 |
| products[] | body | v5FbsPostingProductExemplarValidateV5RequestProduct[] | 否 | 商品清单。 |
| products[].exemplars | body | v5FbsPostingProductExemplarValidateV5RequestProductExemplar[] | 否 | 副本信息。 |
| products[].exemplars[] | body | v5FbsPostingProductExemplarValidateV5RequestProductExemplar[] | 否 | 副本信息。 |
| products[].exemplars[].gtd | body | string | 否 | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].marks | body | v5FbsPostingProductExemplarValidateV5RequestProductExemplarMark[] | 否 | 单个实例中的控制识别码列表。 |
| products[].exemplars[].marks[] | body | v5FbsPostingProductExemplarValidateV5RequestProductExemplarMark[] | 否 | 单个实例中的控制识别码列表。 |
| products[].exemplars[].rnpt | body | string | 否 | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].product_id | body | integer | 否 | Ozon系统中的商品ID — SKU。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| products | v5FbsPostingProductExemplarValidateV5ResponseProduct[] | 商品清单。 |
| products[] | v5FbsPostingProductExemplarValidateV5ResponseProduct[] | 商品清单。 |
| products[].error | string | 错误代码。 |
| products[].exemplars | v5FbsPostingProductExemplarValidateV5ResponseProductExemplar[] | 副本信息。 |
| products[].exemplars[] | v5FbsPostingProductExemplarValidateV5ResponseProductExemplar[] | 副本信息。 |
| products[].exemplars[].errors | string[] | 样件验证错误。 |
| products[].exemplars[].errors[] | string[] | 样件验证错误。 |
| products[].exemplars[].gtd | string | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].marks | v5FbsPostingProductExemplarValidateV5ResponseProductExemplarMark[] | 单个实例中的控制识别码列表。 |
| products[].exemplars[].marks[] | v5FbsPostingProductExemplarValidateV5ResponseProductExemplarMark[] | 单个实例中的控制识别码列表。 |
| products[].exemplars[].rnpt | string | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].exemplars[].valid | boolean | 验证结果。如果样件代码都符合要求，那么结果将为 `true`。 |
| products[].product_id | integer | Ozon系统中的商品ID — SKU。 |
| products[].valid | boolean | 验证结果。如果所有样件的代码都符合要求，那么结果将为 `true`。 |


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
  "products": [
    {
      "error": "string",
      "exemplars": [
        null
      ],
      "product_id": 0,
      "valid": false
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863095.md

---

## Обновить данные экземпляров

### 接口说明

请使用 [/v6/fbs/posting/product/exemplar/set](#operation/PostingAPI_FbsPostingProductExemplarSetV6), 方法，在传输实例数据后调用该方法，以保存“等待发运”状态下订单的最新实例数据。
您可以在 [讨论](https://dev.ozon.ru/community/1269-Metody-dlia-raboty-so-spiskom-markirovok-FBS-rFBS) 的评论中对此方法提供反馈 在 Ozon for dev 开发者社区中。

### 接口标题

Обновить данные экземпляров

### 接口地址

`POST https://api-seller.ozon.ru/v1/fbs/posting/product/exemplar/update`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1FbsPostingProductExemplarUpdateRequest | 否 | 请求体。 |
| posting_number | body | string | 否 | 发货号。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863096.md

---
