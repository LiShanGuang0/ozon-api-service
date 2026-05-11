# AnalyticsAPI

接口数量：1

## 接口列表

- [分析数据](#分析数据) - `POST /v1/analytics/data`

## 分析数据

### 接口说明

请指定需要计算的时间段和指标。响应将包含按`dimensions`参数分组的分析。
从一个卖家账号每分钟可以发送1次请求。
与个人中心中的**分析→图表**部分相符。

### 接口标题

分析数据

### 接口地址

`POST https://api-seller.ozon.ru/v1/analytics/data`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | analyticsAnalyticsGetDataRequest | 否 | 请求体。 |
| date_from | body | string | 是 | 数据将出现在报告中的日期。<br>若您没有Premium订阅，请指定过去三个月内的日期。 |
| date_to | body | string | 是 | 数据将出现在报告中的截止日期。 |
| dimension | body | seller_serviceanalyticsDimension[] | 是 | 报告中的分组数据。<br>所有卖家可用的分组方法：<br>- `unknownDimension` — 未知商品标识符，<br>- `sku` — 商品标识符，<br>- `spu` — 商品标识符，<br>- `day` — 日，<br>- `week` — 星期，<br>- `month` — 月。<br>只有Premium订阅卖家才能使用的分组方法：<br>- `year` — 年<br>- `category1` — 一级类别，<br>- `category2` — 二级类别，<br>- `category3` — 三级类别，<br>- `category4` — 四级类别，<br>- `brand` — 品牌，<br>- `modelID` — 型号。 |
| dimension[] | body | seller_serviceanalyticsDimension[] | 否 | 报告中的分组数据。<br>所有卖家可用的分组方法：<br>- `unknownDimension` — 未知商品标识符，<br>- `sku` — 商品标识符，<br>- `spu` — 商品标识符，<br>- `day` — 日，<br>- `week` — 星期，<br>- `month` — 月。<br>只有Premium订阅卖家才能使用的分组方法：<br>- `year` — 年<br>- `category1` — 一级类别，<br>- `category2` — 二级类别，<br>- `category3` — 三级类别，<br>- `category4` — 四级类别，<br>- `brand` — 品牌，<br>- `modelID` — 型号。 |
| filters | body | analyticsFilter[] | 否 | 过滤器。 |
| filters[] | body | analyticsFilter[] | 否 | 过滤器。 |
| filters[].key | body | string | 否 | 排序参数。 可以传递`dimension` 和 `metric`中的任何属性,  `brand`除外。 |
| filters[].op | body | FilterOp | 否 | - |
| filters[].value | body | string | 否 | 用于对比的值。 |
| limit | body | integer | 是 | 响应的值个数：<br>- 最大值 — 1000，<br>- 最小值 — 1. |
| metrics | body | analyticsMetric[] | 是 | 最多指定14个指标。如有更多，您将收到 `InvalidArgument`的错误。<br>生成报告所依据的指标列表。<br>所有卖家可用的指标：<br>- `revenue` — 订购的金额，<br>- `ordered_units` — 订购的商品。<br>仅对Premium订阅卖家可用的指标：<br>- `unknown_metric` — 未知指标。<br>- `hits_view_search` —  在搜索和类别中的指标。<br>- `hits_view_pdp` — 商品卡片上的指标。<br>- `hits_view` — 总展示次数。<br>- `hits_tocart_search` — 从搜索或类别添加到购物车。<br>- `hits_tocart_pdp` — 从商品卡片添加到购物车。<br>- `hits_tocart` — 添加到购物车的总数。<br>- `session_view_search` — 带有在搜索结果或目录中展示的会话。计算在搜索结果或目录中有浏览的唯一身份访问者。<br>- `session_view_pdp` — 在商品卡片上显示的会话。计算查看过商品卡片的唯一身份访问者。<br>- `session_view` — 所有会话。计算唯一身份访问者。<br>- `conv_tocart_search` — 从商品卡片转换到购物车。<br>- `conv_tocart_pdp` — 从商品卡片转换到购物车的总转化率。<br>- `conv_tocart` — 购物车总转化率。<br>- `returns` — 退货。<br>- `cancellations` — 取消的商品。<br>- `delivered_units` — 交付的商品。<br>- `position_category` — 在搜索和类别中的的位置。 |
| metrics[] | body | analyticsMetric[] | 否 | 最多指定14个指标。如有更多，您将收到 `InvalidArgument`的错误。<br>生成报告所依据的指标列表。<br>所有卖家可用的指标：<br>- `revenue` — 订购的金额，<br>- `ordered_units` — 订购的商品。<br>仅对Premium订阅卖家可用的指标：<br>- `unknown_metric` — 未知指标。<br>- `hits_view_search` —  在搜索和类别中的指标。<br>- `hits_view_pdp` — 商品卡片上的指标。<br>- `hits_view` — 总展示次数。<br>- `hits_tocart_search` — 从搜索或类别添加到购物车。<br>- `hits_tocart_pdp` — 从商品卡片添加到购物车。<br>- `hits_tocart` — 添加到购物车的总数。<br>- `session_view_search` — 带有在搜索结果或目录中展示的会话。计算在搜索结果或目录中有浏览的唯一身份访问者。<br>- `session_view_pdp` — 在商品卡片上显示的会话。计算查看过商品卡片的唯一身份访问者。<br>- `session_view` — 所有会话。计算唯一身份访问者。<br>- `conv_tocart_search` — 从商品卡片转换到购物车。<br>- `conv_tocart_pdp` — 从商品卡片转换到购物车的总转化率。<br>- `conv_tocart` — 购物车总转化率。<br>- `returns` — 退货。<br>- `cancellations` — 取消的商品。<br>- `delivered_units` — 交付的商品。<br>- `position_category` — 在搜索和类别中的的位置。 |
| offset | body | integer | 否 | 响应中要跳过的元素数字。例如，如果 `offset = 10`, 那么答案将从找到的第11个元素开始。 |
| sort | body | analyticsSorting[] | 否 | 报告排列设置。 |
| sort[] | body | analyticsSorting[] | 否 | 报告排列设置。 |
| sort[].key | body | string | 否 | 查询排序结果所依据的指标。 |
| sort[].order | body | SortingOrder | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | AnalyticsGetDataResponseResult | - |
| result.data | analyticsDataRow[] | 数据组。 |
| result.data[] | analyticsDataRow[] | 数据组。 |
| result.data[].dimensions | analyticsDataRowDimension[] | 报告数据分组。 |
| result.data[].dimensions[] | analyticsDataRowDimension[] | 报告数据分组。 |
| result.data[].metrics | number[] | 指标值列表。 |
| result.data[].metrics[] | number[] | 指标值列表。 |
| result.totals | number[] | 指标总计和平均值。 |
| result.totals[] | number[] | 指标总计和平均值。 |
| timestamp | string | 报告创建时间。 |


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
    "data": [],
    "totals": [
      0
    ]
  },
  "timestamp": "2021-11-25 15:19:21"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998415.md

---
