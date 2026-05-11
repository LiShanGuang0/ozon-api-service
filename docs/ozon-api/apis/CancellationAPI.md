# CancellationAPI

接口数量：7

## 接口列表

- [获取有关rFBS取消订单的消息](#获取有关rfbs取消订单的消息) - `POST /v1/conditional-cancellation/get`
- [获取 rFBS 取消申请列表](#获取-rfbs-取消申请列表) - `POST /v2/conditional-cancellation/list`
- [获取rFBS取消申请列表](#获取rfbs取消申请列表) - `POST /v1/conditional-cancellation/list`
- [确认 rFBS 取消申请](#确认-rfbs-取消申请) - `POST /v2/conditional-cancellation/approve`
- [确定rFBS取消订单](#确定rfbs取消订单) - `POST /v1/conditional-cancellation/approve`
- [拒绝 rFBS 取消申请](#拒绝-rfbs-取消申请) - `POST /v2/conditional-cancellation/reject`
- [拒绝取消rFBS申请](#拒绝取消rfbs申请) - `POST /v1/conditional-cancellation/reject`

## 获取有关rFBS取消订单的消息

### 接口说明

获取有关rFBS取消订单消息的方法。

### 接口标题

获取有关rFBS取消订单的消息

### 接口地址

`POST https://api-seller.ozon.ru/v1/conditional-cancellation/get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetConditionalCancellationRequest | 否 | 请求体。 |
| cancellation_id | body | integer | 是 | 订单取消ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1ConditionalCancellation | - |
| result.cancellation_id | integer | 取消申请ID。 |
| result.posting_number | string | 发货号。 |
| result.cancellation_reason | ConditionalCancellationCancellationReason | - |
| result.cancellation_reason.id | integer | 取消原因ID。 |
| result.cancellation_reason.name | string | 取消原因名称。 |
| result.cancelled_at | string | 创建取消订单的日期。 |
| result.cancellation_reason_message | string | 取消者手动输入的取消申请评论。 |
| result.tpl_integration_type | string | 与快递服务的集成类型。 |
| result.state | ConditionalCancellationState | - |
| result.state.id | integer | 状态ID。 |
| result.state.name | string | 状态名称。 |
| result.state.state | enum(ON_APPROVAL, APPROVED, REJECTED) | 申请状态：<br>- `ON_APPROVAL` — 等待决定。<br>- `APPROVED` — 确定。<br>- `REJECTED` — 拒绝。 |
| result.cancellation_initiator | enum(OZON, SELLER, CLIENT, SYSTEM, DELIVERY) | 取消发起人：<br>- `OZON` — Ozon，<br>- `SELLER` — 卖家，<br>- `CLIENT` — 买家，<br>- `SYSTEM` — 系统，<br>- `DELIVERY` — 快递服务。 |
| result.order_date | string | 订单创建日期。 |
| result.approve_comment | string | 确认或拒绝取消申请时留下的评论。 |
| result.approve_date | string | 确认或拒绝取消申请的日期。 |
| result.auto_approve_date | string | 申请将被自动确认的日期。 |


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
    "cancellation_id": 90066344,
    "posting_number": "47134289-0029-1",
    "cancellation_reason": {
      "id": 508,
      "name": "Покупатель отменил заказ"
    },
    "cancelled_at": "2022-04-07T06:37:26.871105Z",
    "cancellation_reason_message": "Изменение пункта выдачи заказа.",
    "tpl_integration_type": "ThirdPartyTracking",
    "state": {
      "id": 2,
      "name": "Подтверждена",
      "state": "APPROVED"
    },
    "cancellation_initiator": "CLIENT",
    "order_date": "2022-04-06T17:17:24.517Z",
    "approve_comment": "",
    "approve_date": "2022-04-07T07:52:45.971824Z",
    "auto_approve_date": "2022-04-09T06:37:26.871105Z"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998394.md

---

## 获取 rFBS 取消申请列表

### 接口说明

用于获取 rFBS 订单取消申请列表的方法。

### 接口标题

获取 rFBS 取消申请列表

### 接口地址

`POST https://api-seller.ozon.ru/v2/conditional-cancellation/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v2GetConditionalCancellationListV2Request | 否 | 请求体。 |
| filters | body | GetConditionalCancellationListV2RequestFilters | 否 | - |
| filters.cancellation_initiator | body | v2CancellationInitiatorEnum[] | 否 | 取消发起人：<br>- `SELLER` — 卖家，<br>- `CLIENT` — 买家，<br>- `OZON` — Ozon，<br>- `SYSTEM` — 系统，<br>- `DELIVERY` — 配送服务。 |
| filters.cancellation_initiator[] | body | v2CancellationInitiatorEnum[] | 否 | 取消发起人：<br>- `SELLER` — 卖家，<br>- `CLIENT` — 买家，<br>- `OZON` — Ozon，<br>- `SYSTEM` — 系统，<br>- `DELIVERY` — 配送服务。 |
| filters.posting_number | body | string[] | 否 | 按货件编号筛选。 |
| filters.posting_number[] | body | string[] | 否 | 按货件编号筛选。 |
| filters.state | body | v2CancellationStateEnumFilters | 否 | 按取消申请状态筛选：<br>- `ALL` — 所有状态的申请，<br>- `ON_APPROVAL` — 审核中申请，<br>- `APPROVED` — 已确认申请，<br>- `REJECTED` — 已拒绝申请。 |
| last_id | body | integer | 否 | 页面上最后一个值的标识符。在首次请求时此字段留空。<br>要获取后续值，请指定上一次请求响应中的 `last_id`。 |
| limit | body | integer | 是 | 响应中包含的申请总数。 |
| with | body | GetConditionalCancellationListV2RequestWith | 否 | - |
| with.counter | body | boolean | 否 | 表示需要在响应中返回处于 `ON_APPROVAL` 状态的申请数量的标志。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| counter | integer | `ON_APPROVAL` 状态申请的计数器。 |
| last_id | integer | 页面上最后一个值的标识符。<br>要获取后续值，请指定上一次请求响应中的 `last_id`。 |
| result | GetConditionalCancellationListV2ResponseResult[] | 取消申请的详细信息。 |
| result[] | GetConditionalCancellationListV2ResponseResult[] | 取消申请的详细信息。 |
| result[].approve_comment | string | 在确认或拒绝取消申请时填写的备注。 |
| result[].approve_date | string | 取消申请确认或拒绝的日期。 |
| result[].auto_approve_date | string | 申请将在此日期后自动确认。 |
| result[].cancellation_id | integer | 取消申请标识符。 |
| result[].cancellation_initiator | v2CancellationInitiatorEnum | - |
| result[].cancellation_reason | GetConditionalCancellationListV2ResponseCancellationReason | - |
| result[].cancellation_reason.id | integer | 取消原因标识符。 |
| result[].cancellation_reason.name | string | 取消原因名称。 |
| result[].cancellation_reason_message | string | 取消申请中由取消发起人手动填写的备注。 |
| result[].cancelled_at | string | 取消申请的创建日期。 |
| result[].order_date | string | 订单的创建日期。 |
| result[].posting_number | string | 货件编号。 |
| result[].source_id | integer | 上一次取消申请的标识符。<br>用于保持向后兼容性。 |
| result[].state | GetConditionalCancellationListV2ResponseState | - |
| result[].state.id | integer | 状态标识符。 |
| result[].state.name | string | 状态名称。 |
| result[].state.state | v2CancellationStateEnum | - |
| result[].tpl_integration_type | string | 与配送服务的集成类型。 |


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
      "approve_comment": "string",
      "approve_date": "2024-11-27T12:31:43.621Z",
      "auto_approve_date": "2024-11-27T12:31:43.621Z",
      "cancellation_id": 0,
      "cancellation_initiator": "OZON",
      "cancellation_reason": {
        "id": 0,
        "name": "string"
      },
      "cancellation_reason_message": "string",
      "cancelled_at": "2024-11-27T12:31:43.621Z",
      "order_date": "2024-11-27T12:31:43.621Z",
      "posting_number": "string",
      "state": {
        "id": 0,
        "name": "string",
        "state": "ALL"
      },
      "tpl_integration_type": "string"
    }
  ],
  "counter": "1",
  "last_id": 283784254
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863059.md

---

## 获取rFBS取消申请列表

### 接口说明

2025年8月3日，旧方法将被停用。请切换到/v2/conditional-cancellation/list。
获取rFBS取消申请列表的方法。

### 接口标题

获取rFBS取消申请列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/conditional-cancellation/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetConditionalCancellationListRequest | 否 | 请求体。 |
| filters | body | GetConditionalCancellationListRequestFilters | 否 | - |
| filters.cancellation_initiator | body | enum(OZON, SELLER, CLIENT, SYSTEM, DELIVER)[] | 否 | 取消发起人：<br>- `SELLER` — 卖家,<br>- `CLIENT` — 客户或买家,<br>- `OZON` — Ozon,<br>- `SYSTEM` — 系统,<br>- `DELIVERY` — 配送服务。<br>非必要参数。可以传递多个值。 |
| filters.cancellation_initiator[] | body | enum(OZON, SELLER, CLIENT, SYSTEM, DELIVER)[] | 否 | 取消发起人：<br>- `SELLER` — 卖家,<br>- `CLIENT` — 客户或买家,<br>- `OZON` — Ozon,<br>- `SYSTEM` — 系统,<br>- `DELIVERY` — 配送服务。<br>非必要参数。可以传递多个值。 |
| filters.posting_number | body | array of strings | 否 | 按照快递号过滤。<br>非必要参数。可以传递多个值。 |
| filters.state | body | enum(ALL, ON_APPROVAL, APPROVED, REJECTED) | 否 | 按取消请求状态筛选：<br>- `ALL` — 任何状态的申请，<br>- `ON_APPROVAL` — 在审查的申请，<br>- `APPROVED` — 已确定的申请，<br>- `REJECTED` — 已拒绝的申请。 |
| limit | body | integer | 是 | 响应中的申请数量。 |
| offset | body | integer | 否 | 将在响应中跳过的元素数。 例如，如果'offset=10`，响应将从找到的第11个元素开始。 |
| with | body | GetConditionalCancellationListRequestWith | 否 | - |
| with.counters | body | boolean | 否 | 响应中应显示处于不同状态的申请计数器标志。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1ConditionalCancellation[] | 订单取消列表。 |
| result[] | v1ConditionalCancellation[] | 订单取消列表。 |
| result[].cancellation_id | integer | 取消申请ID。 |
| result[].posting_number | string | 发货号。 |
| result[].cancellation_reason | ConditionalCancellationCancellationReason | - |
| result[].cancellation_reason.id | integer | 取消原因ID。 |
| result[].cancellation_reason.name | string | 取消原因名称。 |
| result[].cancelled_at | string | 创建取消订单的日期。 |
| result[].cancellation_reason_message | string | 取消者手动输入的取消申请评论。 |
| result[].tpl_integration_type | string | 与快递服务的集成类型。 |
| result[].state | ConditionalCancellationState | - |
| result[].state.id | integer | 状态ID。 |
| result[].state.name | string | 状态名称。 |
| result[].state.state | enum(ON_APPROVAL, APPROVED, REJECTED) | 申请状态：<br>- `ON_APPROVAL` — 等待决定。<br>- `APPROVED` — 确定。<br>- `REJECTED` — 拒绝。 |
| result[].cancellation_initiator | enum(OZON, SELLER, CLIENT, SYSTEM, DELIVERY) | 取消发起人：<br>- `OZON` — Ozon，<br>- `SELLER` — 卖家，<br>- `CLIENT` — 买家，<br>- `SYSTEM` — 系统，<br>- `DELIVERY` — 快递服务。 |
| result[].order_date | string | 订单创建日期。 |
| result[].approve_comment | string | 确认或拒绝取消申请时留下的评论。 |
| result[].approve_date | string | 确认或拒绝取消申请的日期。 |
| result[].auto_approve_date | string | 申请将被自动确认的日期。 |
| total | integer | 按指定过滤器的申请总数。 |
| counters | GetConditionalCancellationListResponseCounters | - |
| counters.on_approval | integer | 在审核的订单数。 |
| counters.approved | integer | 已确定的订单数。 |
| counters.rejected | integer | 已拒绝的订单数。 |


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
      "cancellation_id": 50186754,
      "posting_number": "41267064-0032-1",
      "cancellation_reason": {
        "id": 508,
        "name": "买家取消订单"
      },
      "cancelled_at": "2021-09-03T07:17:12.116114Z",
      "cancellation_reason_message": "",
      "tpl_integration_type": "ThirdPartyTracking",
      "state": {
        "id": 2,
        "name": "确定",
        "state": "APPROVED"
      },
      "cancellation_initiator": "CLIENT",
      "order_date": "2021-09-03T07:04:53.220Z",
      "approve_comment": "",
      "approve_date": "2021-09-03T09:13:12.614200Z",
      "auto_approve_date": "2021-09-06T07:17:12.116114Z"
    },
    {
      "cancellation_id": 51956491,
      "posting_number": "14094410-0018-1",
      "cancellation_reason": {
        "id": 507,
        "name": "买家决定不买了"
      },
      "cancelled_at": "2021-09-13T15:03:25.155827Z",
      "cancellation_reason_message": "",
      "tpl_integration_type": "ThirdPartyTracking",
      "state": {
        "id": 5,
        "name": "自动取消",
        "state": "REJECTED"
      },
      "cancellation_initiator": "CLIENT",
      "order_date": "2021-09-13T07:48:50.143Z",
      "approve_comment": "",
      "approve_date": null,
      "auto_approve_date": "2021-09-16T15:03:25.155827Z"
    }
  ],
  "total": 19,
  "counters": {
    "on_approval": 0,
    "approved": 14,
    "rejected": 5
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998395.md

---

## 确认 rFBS 取消申请

### 接口说明

此方法可将状态为 `ON_APPROVAL` 的取消申请标记为已确认。订单将被取消，款项退还给买家。

### 接口标题

确认 rFBS 取消申请

### 接口地址

`POST https://api-seller.ozon.ru/v2/conditional-cancellation/approve`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v2ConditionalCancellationMoveV2Request | 否 | 请求体。 |
| cancellation_id | body | integer | 是 | 取消申请标识符。 |
| comment | body | string | 否 | 备注。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863060.md

---

## 确定rFBS取消订单

### 接口说明

2025年8月3日，旧方法将被停用。请切换到/v2/conditional-cancellation/approve。
该方法允许您在 `ON_APPROVAL` 状态下批准取消订单的申请。 该方法适用于 rFBS 订单。 订单将被取消，款项将退还给买家。

### 接口标题

确定rFBS取消订单

### 接口地址

`POST https://api-seller.ozon.ru/v1/conditional-cancellation/approve`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ConditionalCancellationMoveRequest | 否 | 请求体。 |
| cancellation_id | body | integer | 是 | 取消订单ID。 |
| comment | body | string | 否 | 评论。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998396.md

---

## 拒绝 rFBS 取消申请

### 接口说明

此方法可拒绝状态为 `ON_APPROVAL` 的取消申请。在 `comment` 参数中说明拒绝原因。订单将保留当前状态，并需继续发货给买家。

### 接口标题

拒绝 rFBS 取消申请

### 接口地址

`POST https://api-seller.ozon.ru/v2/conditional-cancellation/reject`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v2ConditionalCancellationMoveV2Request | 否 | 请求体。 |
| cancellation_id | body | integer | 是 | 取消申请标识符。 |
| comment | body | string | 否 | 备注。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863061.md

---

## 拒绝取消rFBS申请

### 接口说明

2025年8月3日，旧方法将被停用。请切换到/v2/conditional-cancellation/reject。
该方法允许您拒绝处于 `ON_APPROVAL`状态的取消申请。该方法适用于 rFBS 订单。 请在 `comment`参数中解释您的决定。
订单将保持相同的状态，并且交付给买家。

### 接口标题

拒绝取消rFBS申请

### 接口地址

`POST https://api-seller.ozon.ru/v1/conditional-cancellation/reject`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ConditionalCancellationMoveRequest | 否 | 请求体。 |
| cancellation_id | body | integer | 是 | 取消订单ID。 |
| comment | body | string | 否 | 评论。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998397.md

---
