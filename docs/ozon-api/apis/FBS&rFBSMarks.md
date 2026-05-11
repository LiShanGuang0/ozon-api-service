# FBS&rFBSMarks

接口数量：7

## 接口列表

- [获取商品实例信息](#获取商品实例信息) - `POST /v5/fbs/posting/product/exemplar/create-or-get`
- [标志代码验证](#标志代码验证) - `POST /v4/fbs/posting/product/exemplar/validate`
- [检查并保存份数数据](#检查并保存份数数据) - `POST /v4/fbs/posting/product/exemplar/set`
- [检查并保存份数数据 (第5方案)](#检查并保存份数数据-第5方案) - `POST /v5/fbs/posting/product/exemplar/set`
- [获取样件添加状态](#获取样件添加状态) - `POST /v4/fbs/posting/product/exemplar/status`
- [搜集订单 (第4方案)](#搜集订单-第4方案) - `POST /v4/posting/fbs/ship`
- [货件的部分装配 (第4方案)](#货件的部分装配-第4方案) - `POST /v4/posting/fbs/ship/package`

## 获取商品实例信息

### 接口说明

该方法用于获取货件中商品的实例信息。
请使用此方法获取`exemplar_id`。

### 接口标题

获取商品实例信息

### 接口地址

`POST https://api-seller.ozon.ru/v5/fbs/posting/product/exemplar/create-or-get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v5FbsPostingProductExemplarCreateOrGetV5Request | 否 | 请求体。 |
| posting_number | body | string | 是 | 发货号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| multi_box_qty | integer | 商品包装的箱子数量。 |
| posting_number | string | 发货号。 |
| products | v5FbsPostingProductExemplarCreateOrGetV5ResponseProduct[] | 商品清单。 |
| products[] | v5FbsPostingProductExemplarCreateOrGetV5ResponseProduct[] | 商品清单。 |
| products[].exemplars | v5FbsPostingProductExemplarCreateOrGetV5ResponseProductExemplar[] | 副本信息。 |
| products[].exemplars[] | v5FbsPostingProductExemplarCreateOrGetV5ResponseProductExemplar[] | 副本信息。 |
| products[].exemplars[].exemplar_id | integer | 样件识别码。 |
| products[].exemplars[].gtd | string | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].is_gtd_absent | boolean | 不需要指出货运报关单（Cargo Customs Declaration）号码的标志。 |
| products[].exemplars[].is_rnpt_absent | boolean | 不需要指出商品批次注册号(Product Batch Registration Number)的标志。 |
| products[].exemplars[].mandatory_mark | string | 必须标记“诚信标记”。 |
| products[].exemplars[].rnpt | string | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].exemplars[].jw_uin | string | 珠宝制品唯一标识码。 |
| products[].is_gtd_needed | boolean | 说明需要递交产品和货件的货物报关单号码。 |
| products[].is_mandatory_mark_needed | boolean | 说明需要将标志递交给“诚实标志”。 |
| products[].is_rnpt_needed | boolean | 说明需要递交商品批次号码。 |
| products[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
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
      "is_mandatory_mark_needed": false,
      "is_rnpt_needed": false,
      "product_id": 0,
      "quantity": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863053.md

---

## 标志代码验证

### 接口说明

用于检查代码是否符合数量和字符组成的要求。
[查看卖家知识库中的错误详情](https://seller-edu.ozon.ru/fbs/ozon-logistika/markirovka#какие-могут-возникать-ошибки-при-проверке-кода-маркировки)
如果您没有货物报关单号，那么您可以不输入。

### 接口标题

标志代码验证

### 接口地址

`POST https://api-seller.ozon.ru/v4/fbs/posting/product/exemplar/validate`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingv4FbsPostingProductExemplarValidateRequest | 否 | 请求体。 |
| posting_number | body | string | 否 | 货件编号。 |
| products | body | postingv4FbsPostingProductExemplarValidateRequestProduct[] | 否 | 商品列表。 |
| products[] | body | postingv4FbsPostingProductExemplarValidateRequestProduct[] | 否 | 商品列表。 |
| products[].exemplars | body | postingv4FbsPostingProductExemplarValidateRequestProductExemplar[] | 否 | 样件信息。 |
| products[].exemplars[] | body | postingv4FbsPostingProductExemplarValidateRequestProductExemplar[] | 否 | 样件信息。 |
| products[].exemplars[].gtd | body | string | 否 | 货物报关单号。 |
| products[].exemplars[].mandatory_mark | body | string | 是 | “诚信标志”强制性标志。 |
| products[].exemplars[].rnpt | body | string | 否 | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].product_id | body | integer | 是 | 商品标识码。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | FbsPostingProductExemplarValidateResponseFbsPostingProductExemplarValidateResult | - |
| result.products | FbsPostingProductExemplarValidateResponseFbsPostingProductExemplarValidateResultProduct[] | 商品列表。 |
| result.products[] | FbsPostingProductExemplarValidateResponseFbsPostingProductExemplarValidateResultProduct[] | 商品列表。 |
| result.products[].error | string | 错误代码。 |
| result.products[].exemplars | FbsPostingProductExemplarValidateResponseFbsPostingProductExemplarValidateResultProductExemplar[] | 样件信息。 |
| result.products[].exemplars[] | FbsPostingProductExemplarValidateResponseFbsPostingProductExemplarValidateResultProductExemplar[] | 样件信息。 |
| result.products[].product_id | integer | 商品标识码。 |
| result.products[].valid | boolean | 验证结果。如果所有样件的代码都符合要求，那么结果将为`true`。 |


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
    "products": [
      {
        "product_id": 476925391,
        "exemplars": [
          {
            "mandatory_mark": "010290000151642731tVMohkbfFgunB",
            "jw_uin": "",
            "gtd": "",
            "valid": true,
            "errors": []
          }
        ],
        "valid": true,
        "error": ""
      }
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863054.md

---

## 检查并保存份数数据

### 接口说明

将来该方式将被关闭。请转至 /v5/fbs/posting/product/exemplar/set.
异步方法：
- 检查在“诚信标志”系统中流通份数的存在性；
- 保存份数数据。
为了获取已创建样件的数据，请使用 [/v5/fbs/posting/product/exemplar/create-or-get](#operation/PostingAPI_FbsPostingProductExemplarCreateOrGet)方式。
必要时请在`gtd`参数中指出货运报关单号。如果没有，请赋值 `is_gtd_absent = true`。
如果您在一批货件中有多个相同的商品, 请为货件中的每个商品指出一个 `product_id` 和一组`exemplars` 。
请始终传输全套份数和商品数据。
例如，如果在您的系统里有10份。您已赋值并检查和储存。然后在自己的系统中还添加了60份。
当重新提交份数以供审查和保存时，请指出所有新旧份数。

### 接口标题

检查并保存份数数据

### 接口地址

`POST https://api-seller.ozon.ru/v4/fbs/posting/product/exemplar/set`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | fbsv4SetProductExemplarRequest | 否 | 请求体。 |
| posting_number | body | string | 否 | 发货号。 |
| products | body | fbsv4SetProductExemplarRequestProduct[] | 否 | 商品清单。 |
| products[] | body | fbsv4SetProductExemplarRequestProduct[] | 否 | 商品清单。 |
| products[].exemplars | body | fbsv4SetProductExemplarRequestProductExemplar[] | 否 | 副本信息。 |
| products[].exemplars[] | body | fbsv4SetProductExemplarRequestProductExemplar[] | 否 | 副本信息。 |
| products[].exemplars[].gtd | body | string | 否 | 货运报关单号码（Cargo Customs Declaration）。 |
| products[].exemplars[].is_gtd_absent | body | boolean | 否 | 不需要指出货运报关单（Cargo Customs Declaration）号码的标志。 |
| products[].exemplars[].mandatory_mark | body | string | 否 | 必须标记“诚信标记”。 |
| products[].exemplars[].rnpt | body | string | 否 | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].exemplars[].is_rnpt_absent | body | boolean | 否 | 不需要指出商品批次注册号(Product Batch Registration Number)的标志。 |
| products[].product_id | body | integer | 否 | 在Ozon系统中的FBS商品ID — SKU。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 处理请求的结果。 `true`，如果请求成功。 |


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
  "result": true
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998370.md

---

## 检查并保存份数数据 (第5方案)

### 接口说明

异步方法：
- 检查在“诚信标志”系统中流通份数的存在性；
- 保存份数数据。
为了获取已创建样件的数据，请使用 [/v5/fbs/posting/product/exemplar/create-or-get](#operation/PostingAPI_FbsPostingProductExemplarCreateOrGet)方式。
必要时请在`gtd`参数中指出货运报关单号。如果没有，请赋值 `is_gtd_absent = true`。
如果您在一批货件中有多个相同的商品, 请为货件中的每个商品指出一个 `product_id` 和一组`exemplars` 。
仅适用于状态为 `awaiting_packaging`（等待包装）的货件，否则会返回错误 `INVALID_POSTING_STATE`。
请始终传输全套份数和商品数据。
例如，如果在您的系统里有10份。您已赋值并检查和储存。然后在自己的系统中还添加了60份。
当重新提交份数以供审查和保存时，请指出所有新旧份数。
与 [/v4/fbs/posting/product/exemplar/set](#operation/PostingAPI_SetProductExemplar) 之间的区别为 — 您可以在请求中传达更多的样件信息。
响应代码200并不保证商品数据已被接受。
它表示已创建任务以添加信息。
要检查任务状态，请使用方法[/v4/fbs/posting/product/exemplar/status](#operation/PostingAPI_GetProductExemplarStatus)。

### 接口标题

检查并保存份数数据 (第5方案)

### 接口地址

`POST https://api-seller.ozon.ru/v5/fbs/posting/product/exemplar/set`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v5FbsPostingProductExemplarSetV5Request | 否 | 请求体。 |
| multi_box_qty | body | integer | 否 | 商品包装的箱子数量。 |
| posting_number | body | string | 是 | 发货号。 |
| products | body | v5FbsPostingProductExemplarSetV5RequestProduct[] | 是 | 商品清单。 |
| products[] | body | v5FbsPostingProductExemplarSetV5RequestProduct[] | 否 | 商品清单。 |
| products[].exemplars | body | v5FbsPostingProductExemplarSetV5RequestProductExemplar[] | 否 | 副本信息。 |
| products[].exemplars[] | body | v5FbsPostingProductExemplarSetV5RequestProductExemplar[] | 否 | 副本信息。 |
| products[].exemplars[].exemplar_id | body | integer | 是 | 样件识别码。 |
| products[].exemplars[].gtd | body | string | 否 | 货运报关单号码（Cargo Customs Declaration)。 |
| products[].exemplars[].is_gtd_absent | body | boolean | 否 | 不需要指出货运报关单（Cargo Customs Declaration）号码的标志。 |
| products[].exemplars[].is_rnpt_absent | body | boolean | 否 | 不需要指出商品批次注册号(Product Batch Registration Number)的标志。 |
| products[].exemplars[].mandatory_mark | body | string | 否 | 必须标记“诚信标记”。 |
| products[].exemplars[].rnpt | body | string | 否 | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].exemplars[].jw_uin | body | string | 否 | 珠宝制品唯一标识码。 |
| products[].is_gtd_needed | body | boolean | 否 | 说明需要递交产品和货件的货物报关单号码。 |
| products[].is_mandatory_mark_needed | body | boolean | 否 | 说明需要将标志递交给“诚实标志”。 |
| products[].is_rnpt_needed | body | boolean | 否 | 说明需要递交商品批次号码。 |
| products[].product_id | body | integer | 是 | 卖家系统中的商品标识符 — `product_id`。 |
| products[].quantity | body | integer | 否 | 样件数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 请求处理结果。如果请求已被成功处理，那么结果将为`true`。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863055.md

---

## 获取样件添加状态

### 接口说明

获取在[/v5/fbs/posting/product/exemplar/set](#operation/PostingAPI_FbsPostingProductExemplarSet)方式中传输的样件添加状态的方式。
同时还归还这些样件的数据。

### 接口标题

获取样件添加状态

### 接口地址

`POST https://api-seller.ozon.ru/v4/fbs/posting/product/exemplar/status`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | fbsv4GetProductExemplarStatusRequest | 否 | 请求体。 |
| posting_number | body | string | 是 | 货件编号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| posting_number | string | 货件编号。 |
| products | fbsv4GetProductExemplarStatusResponseProduct[] | 商品列表。 |
| products[] | fbsv4GetProductExemplarStatusResponseProduct[] | 商品列表。 |
| products[].exemplars | fbsv4GetProductExemplarStatusResponseProductExemplar[] | 拷贝信息。 |
| products[].exemplars[] | fbsv4GetProductExemplarStatusResponseProductExemplar[] | 拷贝信息。 |
| products[].exemplars[].exemplar_id | integer | 商品标识码。 |
| products[].exemplars[].gtd | string | 货运报关单号码（Cargo Customs Declaration）。 |
| products[].exemplars[].gtd_check_status | string | 货物报关验证状态。 |
| products[].exemplars[].gtd_error_codes | string[] | 货物报关验证错误代码。 |
| products[].exemplars[].gtd_error_codes[] | string[] | 货物报关验证错误代码。 |
| products[].exemplars[].is_gtd_absent | boolean | 这说明没有输入货物报关单号。 |
| products[].exemplars[].jw_uin | string[] | 珠宝制品唯一标识码。 |
| products[].exemplars[].jw_uin[] | string[] | 珠宝制品唯一标识码。 |
| products[].exemplars[].jw_uin_check_status | string | 珠宝制品唯一标识码验证状态。 |
| products[].exemplars[].jw_uin_error_codes | string[] | 珠宝制品唯一标识码验证错误代码。 |
| products[].exemplars[].jw_uin_error_codes[] | string[] | 珠宝制品唯一标识码验证错误代码。 |
| products[].exemplars[].mandatory_mark | string | 必须标记“诚信标记”。 |
| products[].exemplars[].mandatory_mark_check_status | string | “诚信标志”标志验证状态：<br>- `processing`——标志正在处理中。<br>- `passed`——验证已通过。<br>- `failed`——验证未通过。 |
| products[].exemplars[].mandatory_mark_error_codes | string[] | “诚信标志”标志验证错误代码。 |
| products[].exemplars[].mandatory_mark_error_codes[] | string[] | “诚信标志”标志验证错误代码。 |
| products[].exemplars[].rnpt | string | 商品批次注册号 (Product Batch Registration Number)。 |
| products[].exemplars[].rnpt_check_status | string | 商品批次注册编号验证状态。 |
| products[].exemplars[].rnpt_error_codes | string[] | 商品批次注册编号验证错误代码。 |
| products[].exemplars[].rnpt_error_codes[] | string[] | 商品批次注册编号验证错误代码。 |
| products[].exemplars[].is_rnpt_absent | boolean | 这说明没有输入商品批次注册编号。 |
| products[].product_id | integer | 商品标识码。 |
| status | string | 所有样件和备货可用性的验证状态：<br>- `ship_available` ——可以备货，<br>- `ship_not_available` ——无法备货，<br>- `validation_in_process` ——样件正在验证中。 |


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
  "posting_number": "23281294-0063-2",
  "products": [
    {
      "exemplars": [
        {
          "exemplar_id": "",
          "gtd": "",
          "gtd_check_status": "passed",
          "gtd_error_codes": [],
          "is_gtd_absent": true,
          "is_rnpt_absent": true,
          "jw_uin": "",
          "jw_uin_check_status": "passed",
          "jw_uin_error_codes": [],
          "mandatory_mark": "010290000151642731tVMohkbfFgunB",
          "mandatory_mark_check_status": "passed",
          "mandatory_mark_error_codes": [],
          "rnpt": "",
          "rnpt_check_status": "passed",
          "rnpt_error_codes": []
        }
      ],
      "product_id": 476925391
    }
  ],
  "status": "ship_available"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863056.md

---

## 搜集订单 (第4方案)

### 接口说明

拆分订单，并将状态改为`awaiting_deliver`。
`packages`中的每个元素都可以包含多个`products`和货物。
`products`中的每个元素是包含在这批货物中的商品。
如果出现以下情况，需要拆分订单：
- 商品在一个包装里放不下，
- 商品不可以放在一个包装里。
如需拆分订单，请在`packages`数组中传递多个对象。
不需要拆分订单的请求示例：两个商品将在一个货件中发货。
```
{
"packages": [
{
"products": [
{
"product_id": 185479045,
"quantity": 2
}
]
}
],
"posting_number": "89491381-0072-1"
}
```
需要拆分订单的请求示例：每个商品将在单独的货件中发货。
```
{
"packages": [
{
"products": [
{
"product_id": 185479045,
"quantity": 1
}
]
},
{
"products": [
{
"product_id": 185479045,
"quantity": 1
}
]
}
],
"posting_number": "89491381-0072-1"
}
```
请使用[/v5/fbs/posting/product/exemplar/set](#operation/PostingAPI_FbsPostingProductExemplarSet)方式输入信息。

### 接口标题

搜集订单 (第4方案)

### 接口地址

`POST https://api-seller.ozon.ru/v4/posting/fbs/ship`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | fbsv4FbsPostingShipV4Request | 否 | 请求体。 |
| packages | body | FbsPostingShipV4RequestPackage[] | 是 | 包装清单。 每个包装都包含订单分成的发货清单。 |
| packages[] | body | FbsPostingShipV4RequestPackage[] | 否 | 包装清单。 每个包装都包含订单分成的发货清单。 |
| packages[].products | body | FbsPostingShipV4RequestPackageProduct[] | 是 | 运输途中的商品清单。 |
| packages[].products[] | body | FbsPostingShipV4RequestPackageProduct[] | 否 | 运输途中的商品清单。 |
| packages[].products[].product_id | body | integer | 是 | Ozon系统中的商品识别码是SKU。 |
| packages[].products[].quantity | body | integer | 是 | 副本数量。 |
| posting_number | body | string | 是 | 发货号。 |
| with | body | FbsPostingShipV4RequestWith | 否 | - |
| with.additional_data | body | boolean | 否 | 为获取附加信息，请点击 `true`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| additional_data | FbsPostingShipV4ResponseShipAdditionalData[] | 与发货有关的附加信息。 |
| additional_data[] | FbsPostingShipV4ResponseShipAdditionalData[] | 与发货有关的附加信息。 |
| additional_data[].posting_number | string | 发货号。 |
| additional_data[].products | fbsv4PostingProductDetailWithoutDimensions[] | 正在运输途中的商品列表。 |
| additional_data[].products[] | fbsv4PostingProductDetailWithoutDimensions[] | 正在运输途中的商品列表。 |
| additional_data[].products[].mandatory_mark | string[] | 强制标记“诚信标志”。 |
| additional_data[].products[].mandatory_mark[] | string[] | 强制标记“诚信标志”。 |
| additional_data[].products[].name | string | 商品名称。 |
| additional_data[].products[].offer_id | string | 卖家系统中的商品ID — 货号。 |
| additional_data[].products[].price | string | 价格。 |
| additional_data[].products[].quantity | integer | 发货商品数量。 |
| additional_data[].products[].sku | integer | Ozon系统中的商品ID — SKU. |
| additional_data[].products[].currency_code | string | 价格币种。这与您在个人中心中设置的币种 一 致。<br>可能的值：<br>- `RUB` — 卢布，<br>- `BYN` — 白俄罗斯卢布，<br>- `KZT` — 坚戈，<br>- `EUR` — 欧元，<br>- `USD` — 美元，<br>- `CNY` — 元。 |
| result | string[] | 货运装配结果。 |
| result[] | string[] | 货运装配结果。 |


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
  "additional_data": [
    {
      "posting_number": "89491381-0072-1",
      "products": [
        {
          "currency_code": "RUB",
          "mandatory_mark": [
            "123"
          ],
          "name": "string",
          "offer_id": "17125",
          "price": "2000",
          "quantity": 1,
          "sku": 149618972
        }
      ]
    }
  ],
  "result": [
    "89491381-0072-1"
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998371.md

---

## 货件的部分装配 (第4方案)

### 接口说明

如果在请求中转交货件中的部分商品，那么方式将把最初的货件分为两个部分。在第一个未完成备货的货件中将剩下请求中没有转交的那一部分商品。
默认情况下，创建的货件状态为`awaiting_packaging`（等待备货）。
最初的货件状态将仅在它分成的货件状态发生变化后才发生变化。

### 接口标题

货件的部分装配 (第4方案)

### 接口地址

`POST https://api-seller.ozon.ru/v4/posting/fbs/ship/package`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v4FbsPostingShipPackageV4Request | 否 | 请求体。 |
| posting_number | body | string | 是 | 发货号。 |
| products | body | v4FbsPostingShipPackageV4RequestProduct[] | 否 | 商品清单。 |
| products[] | body | v4FbsPostingShipPackageV4RequestProduct[] | 否 | 商品清单。 |
| products[].exemplarsIds | body | string[] | 否 | 商品外部识别码。 |
| products[].exemplarsIds[] | body | string[] | 否 | 商品外部识别码。 |
| products[].product_id | body | integer | 是 | 卖家系统中的商品标识符 — SKU。 |
| products[].quantity | body | integer | 是 | 样件数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | string | 备货后生成的货件号码。 |


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
  "result": "string"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863057.md

---
