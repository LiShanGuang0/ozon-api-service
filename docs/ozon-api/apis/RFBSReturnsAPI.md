# RFBSReturnsAPI

接口数量：7

## 接口列表

- [退货申请列表](#退货申请列表) - `POST /v2/returns/rfbs/list`
- [退货申请信息](#退货申请信息) - `POST /v2/returns/rfbs/get`
- [拒绝退货申请](#拒绝退货申请) - `POST /v2/returns/rfbs/reject`
- [退还部分商品金额](#退还部分商品金额) - `POST /v2/returns/rfbs/compensate`
- [批准退货申请](#批准退货申请) - `POST /v2/returns/rfbs/verify`
- [确认收到待检查商品](#确认收到待检查商品) - `POST /v2/returns/rfbs/receive-return`
- [向买家退款](#向买家退款) - `POST /v2/returns/rfbs/return-money`

## 退货申请列表

### 接口说明

暂无接口说明。

### 接口标题

退货申请列表

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsListRequest | 否 | 请求体。 |
| filter | body | v2ReturnsRfbsFilter | 否 | - |
| filter.offer_id | body | string | 否 | 卖家系统中的商品标识符 —— 货号。 |
| filter.posting_number | body | string | 否 | 货件编号。 |
| filter.group_state | body | string[] | 否 | 根据申请状态筛选:<br>- `All` — 所有申请。<br>- `New` — 新申请。<br>- `Delivering` — 在途中。<br>- `Checkout` — 审核中。<br>- `Arbitration` — 具争议。<br>- `Approved` — 已批准。<br>- `Rejected` — 已拒绝。 |
| filter.group_state[] | body | string[] | 否 | 根据申请状态筛选:<br>- `All` — 所有申请。<br>- `New` — 新申请。<br>- `Delivering` — 在途中。<br>- `Checkout` — 审核中。<br>- `Arbitration` — 具争议。<br>- `Approved` — 已批准。<br>- `Rejected` — 已拒绝。 |
| filter.created_at | body | CreatedAt | 否 | - |
| filter.created_at.from | body | string | 否 | 开始日期。 |
| filter.created_at.to | body | string | 否 | 结束日期。 |
| last_id | body | integer | 否 | 页面上的最后一个值的标识符。在第一次请求时，请将此字段留空。 |
| limit | body | integer | 是 | 响应中的值数量。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| returns | ReturnsRfbsListResponseReturns | - |
| returns.client_name | string | 买家姓名。 |
| returns.created_at | string | 创建日期。 |
| returns.order_number | string | 订单号。 |
| returns.posting_number | string | 货件编号。 |
| returns.product | v2Product | - |
| returns.product.name | string | 商品名称。 |
| returns.product.offer_id | string | 卖家系统中的商品标识符 —— 货号。 |
| returns.product.currency_code | string | 您的价格所使用的货币。与您在个人中心中设置的货币相匹配。<br>可能的值:<br>- `RUB` — 俄罗斯卢布,<br>- `BYN` — 白俄罗斯卢布,<br>- `KZT` — 坚戈,<br>- `EUR` — 欧元,<br>- `USD` — 美元,<br>- `CNY` — 人民币。 |
| returns.product.price | string | 商品价格。 |
| returns.product.sku | integer | Ozon系统中的商品标识符 —— SKU。 |
| returns.return_id | integer | 退货申请的标识符。 |
| returns.return_number | string | 退货申请编号。 |
| returns.state | v2ReturnsRfbsListV2ResponseState | - |
| returns.state.group_state | string | 根据应用的筛选器的申请状态。 |
| returns.state.money_return_state_name | string | 退款状态。 |
| returns.state.state | string | 申请状态。 |
| returns.state.state_name | string | 退货申请状态的俄语名称。 |


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
  "returns": {
    "client_name": "string",
    "created_at": "2026-01-01T00:00:00Z",
    "order_number": "string",
    "posting_number": "string",
    "product": {
      "name": "string",
      "offer_id": "string",
      "currency_code": "string",
      "price": "string",
      "sku": 0
    },
    "return_id": 0,
    "return_number": "string",
    "state": {
      "group_state": "string",
      "money_return_state_name": "string",
      "state": "string",
      "state_name": "string"
    }
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863075.md

---

## 退货申请信息

### 接口说明

暂无接口说明。

### 接口标题

退货申请信息

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsGetRequest | 否 | 请求体。 |
| return_id | body | integer | 是 | 申请的标识符。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| returns | ReturnsRfbsGetResponseReturns | - |
| returns.available_actions | ReturnsRfbsGetV2ResponseAvailableAction[] | 申请的可用操作的信息。 |
| returns.available_actions[] | ReturnsRfbsGetV2ResponseAvailableAction[] | 申请的可用操作的信息。 |
| returns.available_actions[].id | integer | 操作标识符。 |
| returns.available_actions[].name | string | 操作名称。 |
| returns.client_name | string | 买家姓名。 |
| returns.client_photo | string[] | 商品照片链接。 |
| returns.client_photo[] | string[] | 商品照片链接。 |
| returns.client_return_method_type | ReturnsRfbsGetV2ResponseClientReturnMethodType | - |
| returns.client_return_method_type.id | integer | 标识符。 |
| returns.client_return_method_type.name | string | 名称。 |
| returns.comment | string | 买家评论。 |
| returns.created_at | string | 申请创建日期。 |
| returns.order_number | string | 订单号。 |
| returns.posting_number | string | 货件编号。 |
| returns.product | v2Product | - |
| returns.product.name | string | 商品名称。 |
| returns.product.offer_id | string | 卖家系统中的商品标识符 —— 货号。 |
| returns.product.currency_code | string | 您的价格所使用的货币。与您在个人中心中设置的货币相匹配。<br>可能的值:<br>- `RUB` — 俄罗斯卢布,<br>- `BYN` — 白俄罗斯卢布,<br>- `KZT` — 坚戈,<br>- `EUR` — 欧元,<br>- `USD` — 美元,<br>- `CNY` — 人民币。 |
| returns.product.price | string | 商品价格。 |
| returns.product.sku | integer | Ozon系统中的商品标识符 —— SKU。 |
| returns.rejection_comment | string | 有关申请被拒绝的备注。 |
| returns.rejection_reason | ReturnsRfbsGetV2ResponseRejectionReason[] | 申请被拒绝的原因的信息。 |
| returns.rejection_reason[] | ReturnsRfbsGetV2ResponseRejectionReason[] | 申请被拒绝的原因的信息。 |
| returns.rejection_reason[].hint | string | 有关退货的进一步操作的提示。 |
| returns.rejection_reason[].id | integer | 原因的标识符。 |
| returns.rejection_reason[].is_comment_required | boolean | 指示是否需要备注。 |
| returns.rejection_reason[].name | string | 原因的描述。 |
| returns.return_method_description | string | 商品退货方式。 |
| returns.return_number | string | 退货申请编号。 |
| returns.return_reason | ReturnsRfbsGetV2ResponseReturnReason | - |
| returns.return_reason.id | integer | 原因的标识符。 |
| returns.return_reason.is_defect | boolean | 指示商品是否有瑕疵。 |
| returns.return_reason.name | string | 原因的描述。 |
| returns.ru_post_tracking_number | string | 跟踪号码。 |
| returns.state | v2ReturnsRfbsGetV2ResponseState | - |
| returns.state.state | string | 状态。 |
| returns.state.state_name | string | 状态的俄语名称。 |
| returns.warehouse_id | integer | 仓库标识符。 |


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
  "returns": {
    "available_actions": [
      {
        "id": null,
        "name": null
      }
    ],
    "client_name": "string",
    "client_photo": [
      "string"
    ],
    "client_return_method_type": {
      "id": 0,
      "name": "string"
    },
    "comment": "string",
    "created_at": "2026-01-01T00:00:00Z",
    "order_number": "string",
    "posting_number": "string",
    "product": {
      "name": "string",
      "offer_id": "string",
      "currency_code": "string",
      "price": "string",
      "sku": 0
    },
    "rejection_comment": "string",
    "rejection_reason": [
      {
        "hint": null,
        "id": null,
        "is_comment_required": null,
        "name": null
      }
    ],
    "return_method_description": "string",
    "return_number": "string",
    "return_reason": {
      "id": 0,
      "is_defect": false,
      "name": "string"
    },
    "ru_post_tracking_number": "string",
    "state": {
      "state": "string",
      "state_name": "string"
    },
    "warehouse_id": 0
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863076.md

---

## 拒绝退货申请

### 接口说明

将来该方式将被关闭。请转至 /v1/returns/rfbs/action/set。
该方法允许拒绝rFBS订单的退货申请。您可以在 `comment` 参数中解释您的决定。

### 接口标题

拒绝退货申请

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/reject`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsRejectRequest | 否 | 请求体。 |
| return_id | body | integer | 是 | 退货申请的标识符。 |
| comment | body | string | 否 | 备注。<br>如果 [/v2/returns/rfbs/get](#operation/RFBSReturnsAPI_ReturnsRfbsGetV2) 方法的响应中 `rejection_reason.is_comment_required` 参数为 `true`，则传递备注。 |
| rejection_reason_id | body | integer | 是 | 取消原因的标识符。<br>从 [/v2/returns/rfbs/get](#operation/RFBSReturnsAPI_ReturnsRfbsGetV2) 响应中获取的原因列表中传递标识符，参数为 `rejection_reason`。 |


### 响应参数

#### 200 成功

暂无参数。


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
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863077.md

---

## 退还部分商品金额

### 接口说明

将来该方式将被关闭。请转至 /v1/returns/rfbs/action/set。
用于部分赔偿商品金额的方法：您退还部分款项给买家，商品则留在买家手中。

### 接口标题

退还部分商品金额

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/compensate`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsCompensateRequest | 否 | 请求体。 |
| compensation_amount | body | string | 否 | 赔偿金额。 |
| return_id | body | integer | 是 | 退货申请的标识符。 |


### 响应参数

#### 200 成功

暂无参数。


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
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863078.md

---

## 批准退货申请

### 接口说明

将来该方式将被关闭。请转至 /v1/returns/rfbs/action/set。
该方法允许批准申请并同意接收商品进行检查。
请使用[/v2/returns/rfbs/receive-return](#operation/RFBSReturnsAPI_ReturnsRfbsReceiveReturnV2)方法确认收到商品。

### 接口标题

批准退货申请

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/verify`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsVerifyRequest | 否 | 请求体。 |
| return_id | body | integer | 是 | 退货申请的标识符。 |
| return_method_description | body | string | 否 | 商品退货方式。 |


### 响应参数

#### 200 成功

暂无参数。


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
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863079.md

---

## 确认收到待检查商品

### 接口说明

将来该方式将被关闭。请转至 /v1/returns/rfbs/action/set。

### 接口标题

确认收到待检查商品

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/receive-return`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsReceiveReturnRequest | 否 | 请求体。 |
| return_id | body | integer | 是 | 退货申请的标识符。 |


### 响应参数

#### 200 成功

暂无参数。


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
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863080.md

---

## 向买家退款

### 接口说明

将来该方式将被关闭。请转至 /v1/returns/rfbs/action/set。
该方法确认退还商品的全额。
如果您同意以下条件，请使用此方法：
- 立即退还商品金额并将其留给买家；
- 在收到并检查商品后退还金额。
如果商品有瑕疵或质量问题，请在赔偿栏中填写运费金额，然后点击发送。

### 接口标题

向买家退款

### 接口地址

`POST https://api-seller.ozon.ru/v2/returns/rfbs/return-money`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ReturnsRfbsReturnMoneyRequest | 否 | 请求体。 |
| return_id | body | integer | 是 | 退货申请的标识符。 |
| return_for_back_way | body | integer | 否 | 退还给买家的商品运费金额。 |


### 响应参数

#### 200 成功

暂无参数。


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
{}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863081.md

---
