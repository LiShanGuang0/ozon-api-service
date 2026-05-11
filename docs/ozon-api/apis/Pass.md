# Pass

接口数量：8

## 接口列表

- [通行证列表](#通行证列表) - `POST /v1/pass/list`
- [创建通行证](#创建通行证) - `POST /v1/carriage/pass/create`
- [更新通行证](#更新通行证) - `POST /v1/carriage/pass/update`
- [删除通行证](#删除通行证) - `POST /v1/carriage/pass/delete`
- [创建退货通行证](#创建退货通行证) - `POST /v1/return/pass/create`
- [更新退货通行证](#更新退货通行证) - `POST /v1/return/pass/update`
- [删除退货通行证](#删除退货通行证) - `POST /v1/return/pass/delete`
- [FBS退货数量](#fbs退货数量) - `POST /v1/returns/company/fbs/info`

## 通行证列表

### 接口说明

暂无接口说明。

### 接口标题

通行证列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/pass/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | arrivalpassArrivalPassListRequest | 否 | 请求体。 |
| cursor | body | string | 否 | 用于获取下一批数据的指针。 |
| filter | body | ArrivalPassListRequestFilter | 否 | - |
| filter.arrival_pass_ids | body | string[] | 否 | 按通行证ID筛选。 |
| filter.arrival_pass_ids[] | body | string[] | 否 | 按通行证ID筛选。 |
| filter.arrival_reason | body | string | 否 | 按入场目的筛选：<br>- `FBS_DELIVERY` — 发运。<br>- `FBS_RETURN` — 运出退货。<br>如果未指定此参数，则考虑两种目的。<br>指定的原因必须在通行证的原因列表中。 |
| filter.dropoff_point_ids | body | string[] | 否 | 按发运点筛选。 |
| filter.dropoff_point_ids[] | body | string[] | 否 | 按发运点筛选。 |
| filter.only_active_passes | body | boolean | 否 | `true`, 以获取仅活跃的通行证申请。 |
| filter.warehouse_ids | body | string[] | 否 | 按卖家仓库筛选。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| filter.warehouse_ids[] | body | string[] | 否 | 按卖家仓库筛选。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| limit | body | integer | 是 | 响应中记录数量的限制。<br>默认值为1000。最大值为1000。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| arrival_passes | arrivalpassArrivalPassListResponseArrivalPass[] | 运输通行证列表。 |
| arrival_passes[] | arrivalpassArrivalPassListResponseArrivalPass[] | 运输通行证列表。 |
| arrival_passes[].arrival_pass_id | integer | 通行证ID。 |
| arrival_passes[].arrival_reasons | string[] | 入场目的。 |
| arrival_passes[].arrival_reasons[] | string[] | 入场目的。 |
| arrival_passes[].arrival_time | string | 入场日期和时间，UTC格式。 |
| arrival_passes[].driver_name | string | 司机的姓名。 |
| arrival_passes[].driver_phone | string | 司机的电话号码。 |
| arrival_passes[].dropoff_point_id | integer | 发运点ID。 |
| arrival_passes[].is_active | boolean | 如果申请是活跃的，则为`true`。 |
| arrival_passes[].vehicle_license_plate | string | 车辆牌照号码。 |
| arrival_passes[].vehicle_model | string | 车辆型号。 |
| arrival_passes[].warehouse_id | integer | 卖家仓库ID。 |
| cursor | string | 用于获取下一批数据的指针。<br>如果此参数为空，则没有更多数据。 |


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
  "arrival_passes": [
    {
      "arrival_pass_id": 0,
      "arrival_reasons": [
        "string"
      ],
      "arrival_time": "2026-01-01T00:00:00Z",
      "driver_name": "string",
      "driver_phone": "string",
      "dropoff_point_id": 0,
      "is_active": false,
      "vehicle_license_plate": "string",
      "vehicle_model": "string",
      "warehouse_id": 0
    }
  ],
  "cursor": "string"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863067.md

---

## 创建通行证

### 接口说明

创建的通行证ID将添加到运输中。

### 接口标题

创建通行证

### 接口地址

`POST https://api-seller.ozon.ru/v1/carriage/pass/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | sellerSellerAPIArrivalPassCreateRequest | 否 | 请求体。 |
| arrival_passes | body | sellerSellerAPIArrivalPassCreateRequestArrivalPass[] | 是 | 通行证列表。 |
| arrival_passes[] | body | sellerSellerAPIArrivalPassCreateRequestArrivalPass[] | 否 | 通行证列表。 |
| arrival_passes[].driver_name | body | string | 是 | 司机的姓名。 |
| arrival_passes[].driver_phone | body | string | 是 | 司机的电话号码。 |
| arrival_passes[].vehicle_license_plate | body | string | 是 | 车辆牌照号码。 |
| arrival_passes[].vehicle_model | body | string | 是 | 车辆型号。 |
| arrival_passes[].with_returns | body | boolean | 否 | 如果要运出退货，则为`true`。<br>默认值为`false`。 |
| carriage_id | body | integer | 是 | 运输ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| arrival_pass_ids | string[] | 通行证ID。 |
| arrival_pass_ids[] | string[] | 通行证ID。 |


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
  "arrival_pass_ids": [
    "string"
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863068.md

---

## 更新通行证

### 接口说明

暂无接口说明。

### 接口标题

更新通行证

### 接口地址

`POST https://api-seller.ozon.ru/v1/carriage/pass/update`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | sellerSellerAPIArrivalPassUpdateRequest | 否 | 请求体。 |
| arrival_passes | body | sellerSellerAPIArrivalPassUpdateRequestArrivalPass[] | 是 | 通行证列表。 |
| arrival_passes[] | body | sellerSellerAPIArrivalPassUpdateRequestArrivalPass[] | 否 | 通行证列表。 |
| arrival_passes[].driver_name | body | string | 是 | 司机的姓名。 |
| arrival_passes[].driver_phone | body | string | 是 | 司机的电话号码。 |
| arrival_passes[].id | body | integer | 是 | 通行证ID。 |
| arrival_passes[].vehicle_license_plate | body | string | 是 | 车辆牌照号码。 |
| arrival_passes[].vehicle_model | body | string | 是 | 车辆型号。 |
| arrival_passes[].with_returns | body | boolean | 否 | 如果要运出退货，则为`true`。<br>默认值为`false`。 |
| carriage_id | body | integer | 是 | 运输ID。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863069.md

---

## 删除通行证

### 接口说明

暂无接口说明。

### 接口标题

删除通行证

### 接口地址

`POST https://api-seller.ozon.ru/v1/carriage/pass/delete`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | sellerSellerAPIArrivalPassDeleteRequest | 否 | 请求体。 |
| arrival_pass_ids | body | string[] | 是 | 通行证列表。 |
| arrival_pass_ids[] | body | string[] | 否 | 通行证列表。 |
| carriage_id | body | integer | 是 | 运输ID。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863070.md

---

## 创建退货通行证

### 接口说明

暂无接口说明。

### 接口标题

创建退货通行证

### 接口地址

`POST https://api-seller.ozon.ru/v1/return/pass/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | arrivalpassArrivalPassCreateRequest | 否 | 请求体。 |
| arrival_passes | body | arrivalpassArrivalPassCreateRequestArrivalPass[] | 是 | 通行证列表。 |
| arrival_passes[] | body | arrivalpassArrivalPassCreateRequestArrivalPass[] | 否 | 通行证列表。 |
| arrival_passes[].arrival_time | body | string | 是 | 入场时间，UTC格式。<br>此时通行证将开始生效。 |
| arrival_passes[].driver_name | body | string | 是 | 司机姓名。 |
| arrival_passes[].driver_phone | body | string | 是 | 司机电话号码。 |
| arrival_passes[].dropoff_point_id | body | integer | 是 | 通行证适用的仓库ID。 |
| arrival_passes[].vehicle_license_plate | body | string | 是 | 车辆牌照号码。 |
| arrival_passes[].vehicle_model | body | string | 是 | 车辆型号。 |
| arrival_passes[].warehouse_id | body | integer | 是 | 卖家仓库ID。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| arrival_pass_ids | string[] | 通行证ID。 |
| arrival_pass_ids[] | string[] | 通行证ID。 |


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
  "arrival_pass_ids": [
    "string"
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863071.md

---

## 更新退货通行证

### 接口说明

暂无接口说明。

### 接口标题

更新退货通行证

### 接口地址

`POST https://api-seller.ozon.ru/v1/return/pass/update`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | arrivalpassArrivalPassUpdateRequest | 否 | 请求体。 |
| arrival_passes | body | arrivalpassArrivalPassUpdateRequestArrivalPass[] | 是 | 通行证列表。 |
| arrival_passes[] | body | arrivalpassArrivalPassUpdateRequestArrivalPass[] | 否 | 通行证列表。 |
| arrival_passes[].arrival_pass_id | body | integer | 是 | 通行证ID。 |
| arrival_passes[].arrival_time | body | string | 是 | 入场时间，UTC格式。<br>此时通行证将开始生效。<br>要更改入场时间，请使用方法 [/v1/carriage/pass/update](#operation/carriagePassUpdate)。 |
| arrival_passes[].driver_name | body | string | 是 | 司机的姓名。 |
| arrival_passes[].driver_phone | body | string | 是 | 司机的电话号码。 |
| arrival_passes[].vehicle_license_plate | body | string | 是 | 车辆牌照号码。 |
| arrival_passes[].vehicle_model | body | string | 是 | 车辆型号。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863072.md

---

## 删除退货通行证

### 接口说明

暂无接口说明。

### 接口标题

删除退货通行证

### 接口地址

`POST https://api-seller.ozon.ru/v1/return/pass/delete`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | arrivalpassArrivalPassDeleteRequest | 否 | 请求体。 |
| arrival_pass_ids | body | string[] | 是 | 通行证ID。 |
| arrival_pass_ids[] | body | string[] | 否 | 通行证ID。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863073.md

---

## FBS退货数量

### 接口说明

获取FBS退货及其数量的信息的方法。

### 接口标题

FBS退货数量

### 接口地址

`POST https://api-seller.ozon.ru/v1/returns/company/fbs/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ReturnsCompanyFbsInfoRequest | 否 | 请求体。 |
| filter | body | v1ReturnsCompanyFbsInfoRequestFilter | 否 | - |
| filter.place_id | body | integer | 否 | 按揽收点ID筛选。 |
| pagination | body | ReturnsCompanyFbsInfoRequestPagination | 是 | - |
| pagination.last_id | body | integer | 否 | 页面上最后一个揽收点的ID。对于第一个请求，请将此字段留空。<br>要获取后续的值，请指定上一个请求响应中最后一个揽收点的`id`。 |
| pagination.limit | body | integer | 是 | 页面上揽收点的数量。最大值为500。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| drop_off_points | ReturnsCompanyFbsInfoResponseDropOffPoints[] | 揽收点信息。 |
| drop_off_points[] | ReturnsCompanyFbsInfoResponseDropOffPoints[] | 揽收点信息。 |
| drop_off_points[].address | string | 揽收点地址。 |
| drop_off_points[].box_count | integer | 在揽收点的箱数。 |
| drop_off_points[].id | integer | 揽收点ID。 |
| drop_off_points[].name | string | 揽收点名称。 |
| drop_off_points[].pass_info | ReturnsCompanyFbsInfoResponsePass_info | - |
| drop_off_points[].pass_info.count | integer | 每个揽收点的通行证数量。 |
| drop_off_points[].pass_info.is_required | boolean | 是否需要揽收点通行证的标志。 |
| drop_off_points[].place_id | integer | 到货仓库的ID。 |
| drop_off_points[].returns_count | integer | 揽收点的退货数量。 |
| drop_off_points[].utc_offset | string | 发运时间与UTC-0的时区偏移量。 |
| drop_off_points[].warehouses_ids | string[] | 卖家仓库ID。 |
| drop_off_points[].warehouses_ids[] | string[] | 卖家仓库ID。 |
| has_next | boolean | 是否还有其他揽收点等待卖家退货的标志。 |


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
  "drop_off_points": [
    {
      "address": "string",
      "box_count": 0,
      "id": 0,
      "name": "string",
      "pass_info": {
        "count": null,
        "is_required": null
      },
      "place_id": 0,
      "returns_count": 0,
      "utc_offset": "string",
      "warehouses_ids": [
        "string"
      ]
    }
  ],
  "has_next": false
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863074.md

---
