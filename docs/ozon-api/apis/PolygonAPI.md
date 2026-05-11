# PolygonAPI

接口数量：2

## 接口列表

- [创建一个快递的设施](#创建一个快递的设施) - `POST /v1/polygon/create`
- [将快递方式与快递设施联系起来](#将快递方式与快递设施联系起来) - `POST /v1/polygon/bind`

## 创建一个快递的设施

### 接口说明

你可以为快递方式添加一个设施。
通过在https://geojson.io，获取其坐标来创建一个设施：在地图上至少标记3个点，并用线连接起来。

### 接口标题

创建一个快递的设施

### 接口地址

`POST https://api-seller.ozon.ru/v1/polygon/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | polygonv1PolygonCreateRequest | 否 | 请求体。 |
| coordinates | body | string | 是 | 快递设施的坐标，格式为 `[[[lat long]]]`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| polygon_id | integer | 设施识别号。 |


#### 400 请求有误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | 错误代码。 |
| details | protobufAny[] | 错误信息。 |
| details[] | protobufAny[] | 错误信息。 |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误信息:<br>- `coordinates not provided` — 未移交坐标;<br>- `invalid coordinates, must have two points in coordinate` — 在一个点上只移交了纬度或经度，需要移交两个点;<br>- `the first and last points in loop must be same` — 第一个点和最后一个点不重合（根据标准的geojson规则，这些点必须重合);<br>- `non-full loops must have at least 4 unique vertices for polygons` — 为设施移交的点少于4个。 |


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
  "polygonId": "1323"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998368.md

---

## 将快递方式与快递设施联系起来

### 接口说明

暂无接口说明。

### 接口标题

将快递方式与快递设施联系起来

### 接口地址

`POST https://api-seller.ozon.ru/v1/polygon/bind`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | polygonv1PolygonBindRequest | 否 | 请求体。 |
| delivery_method_id | body | integer | 是 | 快递方法识别号。 |
| polygons | body | PolygonBindRequestpolygon[] | 是 | 设施清单。 |
| polygons[] | body | PolygonBindRequestpolygon[] | 否 | 设施清单。 |
| polygons[].polygon_id | body | integer | 是 | 设施识别号。 |
| polygons[].time | body | integer | 是 | 商品在该点快递到达的时间，以分钟计。 |
| warehouse_location | body | PolygonBindRequestwh_location | 是 | - |
| warehouse_location.lat | body | string | 是 | 仓库位置的地理纬度。 |
| warehouse_location.lon | body | string | 是 | 仓库位置的地理经度。 |


### 响应参数

#### 200 成功

暂无参数。


#### 400 请求有误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | - |
| details | protobufAny[] | - |
| details[] | protobufAny[] | - |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | 错误信息:<br>- **delivery target polygons not provided** — 设施还没有被移交;<br>- **no delivery method id provided** — delivery_method_id 没有被移交;<br>- **no warehouse points provided** — 未移交的仓库坐标;<br>- **polygon id .... not found** — 数据库中未找到的设施的ID已移交;<br>- **not found polygon for warehouse point** — 该仓库点不属于任何一个被移交的设施。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998369.md

---
