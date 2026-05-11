# DeliveryFBS

接口数量：2

## 接口列表

- [运输信息](#运输信息) - `POST /v1/carriage/get`
- [可供运输的列表](#可供运输的列表) - `POST /v1/posting/carriage-available/list`

## 运输信息

### 接口说明

暂无接口说明。

### 接口标题

运输信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/carriage/get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | carriageCarriageGetRequest | 否 | 请求体。 |
| carriage_id | body | integer | 是 | 运输标识符。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| act_type | string | 交接单类型。针对FBS卖家。 |
| arrival_pass_ids | string[] | 为运输生成的通行证标识符列表。 |
| arrival_pass_ids[] | string[] | 为运输生成的通行证标识符列表。 |
| available_actions | string[] | 运输的可用操作。 |
| available_actions[] | string[] | 运输的可用操作。 |
| cancel_availability | carriageCarriageGetResponseCancelAvailability | - |
| cancel_availability.is_cancel_available | boolean | `true`, 如果运输可以取消。 |
| cancel_availability.reason | string | 运输无法取消的原因。 |
| carriage_id | integer | 运输标识符。 |
| company_id | integer | 卖家标识符。 |
| containers_count | integer | 货位数量。 |
| created_at | string | 运输创建日期。 |
| delivery_method_id | integer | 物流方式标识符。 |
| departure_date | string | 运输完成日期。 |
| first_mile_type | string | 头程物流类型。 |
| has_postings_for_next_carriage | boolean | `true`, 如果有未能进行运输，但需要发运的货件。 |
| integration_type | string | 运输类型。 |
| is_container_label_printed | boolean | `true`, 如果您已经打印了货位标签。 |
| is_partial | boolean | `true`, 如果是部分运输。 |
| partial_num | integer | 部分运输序列号。 |
| retry_count | integer | 运输创建重复尝试数量。 |
| status | string | 运输状态。 |
| tpl_provider_id | integer | 配送服务商标识符。 |
| updated_at | string | 运输信息最后一次更新日期。 |
| warehouse_id | integer | 仓库标识符。 |


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
  "act_type": "string",
  "arrival_pass_ids": [
    "string"
  ],
  "available_actions": [
    "string"
  ],
  "cancel_availability": {
    "is_cancel_available": false,
    "reason": "string"
  },
  "carriage_id": 0,
  "company_id": 0,
  "containers_count": 0,
  "created_at": "2026-01-01T00:00:00Z",
  "delivery_method_id": 0,
  "departure_date": "string",
  "first_mile_type": "string",
  "has_postings_for_next_carriage": false,
  "integration_type": "string",
  "is_container_label_printed": false,
  "is_partial": false,
  "partial_num": 0,
  "retry_count": 0,
  "status": "string",
  "tpl_provider_id": 0,
  "updated_at": "2026-01-01T00:00:00Z",
  "warehouse_id": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863065.md

---

## 可供运输的列表

### 接口说明

需要打印验收证明书和运输货单的收货方式。

### 接口标题

可供运输的列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/posting/carriage-available/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingv1GetCarriageAvailableListRequest | 否 | 请求体。 |
| delivery_method_id | body | integer | 是 | 按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| departure_date | body | string | 否 | 装运日期。默认 —— 当前日期。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | GetCarriageAvailableListResponseResult[] | 方法操作结果。 |
| result[] | GetCarriageAvailableListResponseResult[] | 方法操作结果。 |
| result[].carriage_id | integer | 运输ID（也是文件形成的任务编号）。 |
| result[].carriage_postings_count | integer | 运输中的货件数量。 |
| result[].carriage_status | string | 所请求的交付方式和装运日期的运输状态。 |
| result[].cutoff_at | string | 需要收取货件的日期和时间。 |
| result[].delivery_method_id | integer | 快递方式ID。 |
| result[].delivery_method_name | string | 快递方式名称。 |
| result[].errors | ResultError[] | 错误列表。 |
| result[].errors[] | ResultError[] | 错误列表。 |
| result[].errors[].code | string | 错误代码。 |
| result[].errors[].status | string | 错误类型：<br>- `warning` — 提醒；<br>- `critical` — 严重错误。 |
| result[].first_mile_type | string | 第一英里类型。 |
| result[].has_entrusted_acceptance | boolean | 信任接收的标志。 如果在仓库中启用了信任接收，则为“true”。 |
| result[].mandatory_postings_count | integer | 需要收取的货件数量。 |
| result[].mandatory_packaged_count | integer | 收取货件数量。 |
| result[].recommended_time_local | string | 推荐的本地发运时间（订单接收点）。 |
| result[].recommended_time_utc_offset_in_minutes | number | 推荐发运时间与UTC-0的时区偏移量（以分钟为单位）。 |
| result[].tpl_provider_icon_url | string | 快递服务图标的链接。 |
| result[].tpl_provider_name | string | 快递服务名称。 |
| result[].warehouse_city | string | 仓库所在城市。 |
| result[].warehouse_id | integer | 仓库ID。 |
| result[].warehouse_name | string | 仓库名称。 |
| result[].warehouse_timezone | string | 仓库所在时区。 |


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
      "carriage_id": 0,
      "carriage_postings_count": 0,
      "carriage_status": "string",
      "cutoff_at": "2026-01-01T00:00:00Z",
      "delivery_method_id": 0,
      "delivery_method_name": "string",
      "errors": [
        null
      ],
      "first_mile_type": "string",
      "has_entrusted_acceptance": false,
      "mandatory_postings_count": 0,
      "mandatory_packaged_count": 0,
      "recommended_time_local": "string",
      "recommended_time_utc_offset_in_minutes": 0,
      "tpl_provider_icon_url": "string",
      "tpl_provider_name": "string",
      "warehouse_city": "string",
      "warehouse_id": 0,
      "warehouse_name": "string",
      "warehouse_timezone": "string"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998380.md

---
