# WarehouseAPI

接口数量：2

## 接口列表

- [仓库清单](#仓库清单) - `POST /v2/warehouse/list`
- [仓库物流方式清单](#仓库物流方式清单) - `POST /v1/delivery-method/list`

## 仓库清单

### 接口说明

方法返回仓库列表。`/v1/warehouse/list` 已禁用，请使用新版 `/v2/warehouse/list`。

### 接口标题

仓库清单

### 接口地址

`POST https://api-seller.ozon.ru/v2/warehouse/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | WarehouseListRequest | 是 | 请求体。 |
| cursor | body | string | 否 | 后续数据的选择标志。首次请求可不传或传空字符串。 |
| limit | body | integer | 是 | 响应中返回的值数量，最大 200。 |
| warehouse_ids | body | string[] &lt;int64&gt; | 否 | 仓库识别符列表，最多 200 个。用于按仓库 ID 过滤。 |

### 请求示例

```json
{
  "cursor": "",
  "limit": 200,
  "warehouse_ids": [
    "20605650762000"
  ]
}
```


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| cursor | string | 后续数据的选择标志。 |
| warehouses | Warehouse[] | 仓库列表。 |
| warehouses[] | Warehouse[] | 仓库对象。 |
| warehouses[].address_info | object | 仓库位置信息。 |
| warehouses[].address_info.address | string | 仓库地址。 |
| warehouses[].address_info.latitude | number | 纬度。 |
| warehouses[].address_info.longitude | number | 经度。 |
| warehouses[].address_info.utc | string | 仓库所在时区，例如 `UTC+03:00`。 |
| warehouses[].carriage_label_type | enum(UNSPECIFIED, BIG, SMALL) | 标签类型：`UNSPECIFIED` 未知类型，`BIG` 大标签，`SMALL` 小标签。 |
| warehouses[].courier_comment | string | 给快递员的评论。 |
| warehouses[].courier_phones | string[] | 用于与快递员联系的电话号码。 |
| warehouses[].created_at | string &lt;date-time&gt; | 仓库创建日期和时间。 |
| warehouses[].cut_in_time | integer &lt;int64&gt; | 发运所需时间，单位分钟。 |
| warehouses[].first_mile | object | 头程物流。 |
| warehouses[].first_mile.type | string | 头程物流类型。 |
| warehouses[].first_mile.dropoff_point_id | string | Drop-off 点识别号。 |
| warehouses[].first_mile.timeslot_from | string | 时间段开始时间。 |
| warehouses[].first_mile.timeslot_id | integer | 时间段 ID。 |
| warehouses[].first_mile.timeslot_to | string | 时间段结束时间。 |
| warehouses[].first_mile.first_mile_is_changing | boolean | 头程物流设置是否正在变更。 |
| warehouses[].has_entrusted_acceptance | boolean | 信任验收开通标识。 |
| warehouses[].has_postings_limit | boolean | 是否存在最低订单数量限额。 |
| warehouses[].is_auto_assembly | boolean | 是否开启自动备货。 |
| warehouses[].is_comfort | boolean | Comfort 配送标志，送达买家时间大于等于 60 分钟。 |
| warehouses[].is_express | boolean | Express 配送标志，送达买家时间不超过 60 分钟。 |
| warehouses[].is_kgt | boolean | 仓库是否接收超大货物。 |
| warehouses[].is_rfbs | boolean | 仓库是否在 rFBS 工作模式下工作。 |
| warehouses[].is_waybill_enabled | boolean | 是否开启运单打印。 |
| warehouses[].min_postings_limit | integer &lt;int32&gt; | 一次交货中可以运来的最低订单数量。 |
| warehouses[].name | string | 仓库名称。 |
| warehouses[].phone | string | 仓库电话号码。 |
| warehouses[].postings_limit | integer &lt;int32&gt; | 订单限额。没有限额时返回 `-1`。 |
| warehouses[].sla_cut_in | integer &lt;int64&gt; | 订单备货最低时间，单位分钟。 |
| warehouses[].status | string | 仓库状态。 |
| warehouses[].timetable | object | 仓库工作时间表。 |
| warehouses[].timetable.timetable_from | string &lt;date-time&gt; | 时间表开始时间。 |
| warehouses[].timetable.timetable_to | string &lt;date-time&gt; | 时间表结束时间。 |
| warehouses[].timetable.working_hours | object[] | 工作时间列表。 |
| warehouses[].timetable.working_hours[].time_from | string &lt;date-time&gt; | 工作时间开始。 |
| warehouses[].timetable.working_hours[].time_to | string &lt;date-time&gt; | 工作时间结束。 |
| warehouses[].updated_at | string &lt;date-time&gt; | 仓库信息最后一次更新的日期和时间。 |
| warehouses[].warehouse_id | integer &lt;int64&gt; | 仓库识别符。 |
| warehouses[].warehouse_type | string | 仓库类型。 |
| warehouses[].with_item_list | boolean | 是否开启拣货单打印。 |
| warehouses[].working_days | enum(UNSPECIFIED, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)[] | 仓库工作日。 |
| has_next | boolean | `true` 表示本次响应未返回所有数据，需要继续用返回的 `cursor` 查询下一页。 |


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
  "warehouses": [
    {
      "address_info": {
        "address": "Россия, Московская Область, Софьино, промзона ССТ, к2, 2",
        "latitude": 55.495093,
        "longitude": 38.172731,
        "utc": "UTC+03:00"
      },
      "carriage_label_type": "BIG",
      "courier_comment": "",
      "courier_phones": [
        "+7(999)999-99-99"
      ],
      "created_at": "2025-03-11T11:57:51.811Z",
      "first_mile": {
        "type": "PICK_UP",
        "dropoff_point_id": "1020002075314000",
        "timeslot_from": "20:59",
        "timeslot_id": 287231,
        "timeslot_to": "21:00",
        "first_mile_is_changing": false
      },
      "has_entrusted_acceptance": true,
      "has_postings_limit": false,
      "is_auto_assembly": true,
      "is_kgt": true,
      "is_rfbs": true,
      "is_waybill_enabled": true,
      "min_postings_limit": 2,
      "is_comfort": true,
      "is_express": true,
      "warehouse_type": "string",
      "cut_in_time": 0,
      "name": "17023",
      "phone": "+7(999)999-99-99",
      "postings_limit": -1,
      "sla_cut_in": 2939,
      "status": "created",
      "timetable": {
        "timetable_from": "2025-03-11T11:57:51.811Z",
        "timetable_to": "2025-03-11T11:57:51.811Z",
        "working_hours": [
          {
            "time_from": "2025-03-11T11:57:51.811Z",
            "time_to": "2025-03-11T11:57:51.811Z"
          }
        ]
      },
      "updated_at": "2025-03-11T11:57:51.811Z",
      "warehouse_id": 20605650762000,
      "with_item_list": true,
      "working_days": [
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY"
      ]
    }
  ],
  "has_next": false
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998366.md

---

## 仓库物流方式清单

### 接口说明

暂无接口说明。

### 接口标题

仓库物流方式清单

### 接口地址

`POST https://api-seller.ozon.ru/v1/delivery-method/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | warehouseDeliveryMethodListRequest | 否 | 请求体。 |
| filter | body | DeliveryMethodListRequestFilter | 否 | - |
| filter.provider_id | body | integer | 否 | 快递服务识别号。 |
| filter.status | body | string | 否 | 快递方式状态:<br>- `NEW` — 已创建,<br>- `EDITED` — 正在编辑,<br>- `ACTIVE` — 已激活,<br>- `DISABLED` — 未激活。 |
| filter.warehouse_id | body | integer | 否 | 仓库识别号。可以使用方法 `/v2/warehouse/list` 获取。 |
| limit | body | integer | 是 | 回答中的元素数量。最多50，最少1。 |
| offset | body | integer | 否 | 回答中会被略过的元素数量。例如，如果`offset = 10`，回答将从发现的第11个元素开始。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| has_next | boolean | 以下该迹象会表明在查询中只送回了部分快递方式。<br>- `true` — 请用新的 `offset` 参数重新请求，以获得剩余的方式；<br>- `false` — 回答中包含了所有应要求的快递方式。 |
| result | DeliveryMethodListResponseDeliveryMethod[] | 查询结果。 |
| result[] | DeliveryMethodListResponseDeliveryMethod[] | 查询结果。 |
| result[].company_id | integer | 卖家识别号。 |
| result[].created_at | string | 创建快递方式的日期和时间。 |
| result[].cutoff | string | 卖方必须在此之前备货的时间。 |
| result[].id | integer | 快递方式识别号。 |
| result[].name | string | 快递方式名称。 |
| result[].provider_id | integer | 快递服务识别号。 |
| result[].sla_cut_in | integer | 根据仓库设置，订单备货的最短时间（以分钟为单位）。 |
| result[].status | string | 快递方式状态:<br>- `NEW` — 已创建,<br>- `EDITED` — 正在编辑,<br>- `ACTIVE` — 已激活,<br>- `DISABLED` — 未激活。 |
| result[].template_id | integer | 订单快递服务识别号。 |
| result[].updated_at | string | 快递方式最后更新的日期和时间。 |
| result[].warehouse_id | integer | 仓库识别号。 |


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
      "id": 15588127982000,
      "company_id": 1,
      "name": "Ozon物流快递员，Yesipovo",
      "status": "ACTIVE",
      "cutoff": "13:00",
      "provider_id": 24,
      "template_id": 0,
      "warehouse_id": 15588127982000,
      "created_at": "2019-04-04T15:22:31.048202Z",
      "updated_at": "2021-08-15T10:21:44.854209Z",
      "sla_cut_in": 1440
    }
  ],
  "has_next": false
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998367.md

---
