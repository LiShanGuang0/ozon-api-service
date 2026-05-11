# FBS

接口数量：13

## 接口列表

- [未处理货件列表 （第三 版）](#未处理货件列表-（第三-版）) - `POST /v3/posting/fbs/unfulfilled/list`
- [货件列表（第三版）](#货件列表（第三版）) - `POST /v3/posting/fbs/list`
- [按照ID获取货件信息](#按照id获取货件信息) - `POST /v3/posting/fbs/get`
- [按条形码获取有关货件的信息](#按条形码获取有关货件的信息) - `POST /v2/posting/fbs/get-by-barcode`
- [可用产地名单](#可用产地名单) - `POST /v2/posting/fbs/product/country/list`
- [添加商品产地信息](#添加商品产地信息) - `POST /v2/posting/fbs/product/country/set`
- [打印标签](#打印标签) - `POST /v2/posting/fbs/package-label`
- [货件装运](#货件装运) - `POST /v2/posting/fbs/awaiting-delivery`
- [货件取消原因](#货件取消原因) - `POST /v2/posting/fbs/cancel-reason/list`
- [货运取消原因](#货运取消原因) - `POST /v1/posting/fbs/cancel-reason`
- [取消货运](#取消货运) - `POST /v2/posting/fbs/cancel`
- [为货件中的称重商品添加重量](#为货件中的称重商品添加重量) - `POST /v2/posting/fbs/product/change`
- [取消某些商品发货](#取消某些商品发货) - `POST /v2/posting/fbs/product/cancel`

## 未处理货件列表 （第三 版）

### 接口说明

返回指定时间段的未处理货件列表 —— 不应超过一年。
可能的货件运输状态：
- `awaiting_registration` — 等待注册，
- `acceptance_in_progress` — 正在验收，
- `awaiting_approve` — 等待确认，
- `awaiting_packaging` — 等待包装，
- `awaiting_deliver` — 等待装运，
- `arbitration` — 仲裁，
- `client_arbitration` — 快递客户仲裁，
- `delivering` — 运输中，
- `driver_pickup` — 司机处，
- `cancelled` — 已取消，
- `not_accepted` — 分拣中心未接受，
- `sent_by_seller` – 由卖家发送。

### 接口标题

未处理货件列表 （第三 版）

### 接口地址

`POST https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingv3GetFbsPostingUnfulfilledListRequest | 否 | 请求体。 |
| dir | body | string | 否 | 分类方向：<br>- `asc` — 从小到大，<br>- `desc` — 从大到小。 |
| filter | body | postingv3GetFbsPostingUnfulfilledListRequestFilter | 是 | - |
| filter.cutoff_from | body | string | 是 | 按卖家需要收订单的时间进行筛选。 时间段开始。<br>格式： YYYY-MM-DDThh:mm:ss.mcsZ.<br>例子： 2020-03-18T07:34:50.359Z. |
| filter.cutoff_to | body | string | 是 | 按卖家需要收订单的时间进行筛选。 时间段结束。<br>格式： YYYY-MM-DDThh:mm:ss.mcsZ.<br>例子： 2020-03-18T07:34:50.359Z. |
| filter.delivering_date_from | body | string | 否 | 将货件交给物流的最快日期。 |
| filter.delivering_date_to | body | string | 否 | 将货件交给物流的最迟日期。 |
| filter.delivery_method_id | body | integer[] | 否 | 快递方式ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.delivery_method_id[] | body | integer[] | 否 | 快递方式ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.fbpFilter | body | string | 否 | 从合作伙伴仓库（FBP）发货时的货件筛选器：<br>- `ALL` —  响应中将显示所有符合其他筛选器条件的货件；<br>- `ONLY` —  仅显示FBP货件；<br>- `WITHOUT` —  显示除FBP外的所有货件。<br>默认值为 `ALL`。 |
| filter.provider_id | body | integer[] | 否 | 快递服务ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.provider_id[] | body | integer[] | 否 | 快递服务ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.status | body | string | 否 | 货件运输状态：<br>- `acceptance_in_progress` — 正在验收，<br>- `awaiting_approve` — 等待确认，<br>- `awaiting_packaging` — 等待包装，<br>- `awaiting_registration` — 等待注册，<br>- `awaiting_deliver` — 等待装运，<br>- `arbitration` — 仲裁，<br>- `client_arbitration` — 快递客户仲裁，<br>- `delivering` — 运输中，<br>- `driver_pickup` — 司机处，<br>- `not_accepted` — 分拣中心未接受。 |
| filter.warehouse_id | body | integer[] | 否 | 仓库ID。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| filter.warehouse_id[] | body | integer[] | 否 | 仓库ID。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| limit | body | integer | 是 | 响应中值的数量：<br>- 最大值 — 1000，<br>- 最小值 — 1。 |
| offset | body | integer | 是 | 将在响应中跳过的元素数。 例如，如果“offset=10”，那么响应将从找到的第11个元素开始。 |
| with | body | postingv3FbsPostingWithParams | 否 | - |
| with.analytics_data | body | boolean | 否 | 将分析数据添加到响应中。 |
| with.barcodes | body | boolean | 否 | 将货件条形码添加到响应中。 |
| with.financial_data | body | boolean | 否 | 将财务数据添加到响应中。 |
| with.legal_info | body | boolean | 否 | 将法律信息添加到响应中。 |
| with.translit | body | boolean | 否 | 完成返回值的拼写。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | postingv3GetFbsPostingUnfulfilledListResponseResult | - |
| result.count | integer | 在响应中的元素计数器。 |
| result.postings | v3FbsPosting[] | 货件清单和每个货物的详细信息。 |
| result.postings[] | v3FbsPosting[] | 货件清单和每个货物的详细信息。 |
| result.postings[].addressee | v3AddresseeFbsLists | - |
| result.postings[].addressee.name | string | 收件人姓名。 |
| result.postings[].addressee.phone | string | 联系电话。<br>总是返回空字符串 `""`。 |
| result.postings[].analytics_data | v3FbsPostingAnalyticsData | - |
| result.postings[].analytics_data.city | string | 快递城市。仅适用于rFBS货件和独联体卖家。 |
| result.postings[].analytics_data.delivery_date_begin | string | 快递开始日期和时间。 |
| result.postings[].analytics_data.delivery_date_end | string | 快递结束日期和时间。 |
| result.postings[].analytics_data.delivery_type | string | 快递方式。 |
| result.postings[].analytics_data.is_legal | boolean | 收件人是法人的标志：<br>- `true` — 法人，<br>- `false` — 自然人。 |
| result.postings[].analytics_data.is_premium | boolean | 有Premium订阅。 |
| result.postings[].analytics_data.payment_type_group_name | string | 付款方法：<br>- `在线银行卡支付`，<br>- `Ozon卡片`，<br>- `取货时自动从Ozon卡片收费`，<br>- `收货时从已保存的银行卡收费`，<br>- `快速支付系统`，<br>- `Ozon分期付款`，<br>- `支付至结算账户`，<br>- `SberPay`。 |
| result.postings[].analytics_data.region | string | 快递地区。 |
| result.postings[].analytics_data.tpl_provider | string | 快递服务。 |
| result.postings[].analytics_data.tpl_provider_id | integer | 快递服务ID。 |
| result.postings[].analytics_data.warehouse | string | 订单发送仓库名称。 |
| result.postings[].analytics_data.warehouse_id | integer | 仓库ID。 |
| result.postings[].available_actions | string[] | 可用的操作和货件信息包括：<br>- `arbitration` — 提出争议；<br>- `awaiting_delivery` — 转为“等待发运”状态；<br>- `can_create_chat` — 与买家开启聊天；<br>- `cancel` — 取消货件；<br>- `click_track_number` — 在个人中心通过追踪号查看状态历史；<br>- `customer_phone_available` — 获取买家电话号码；<br>- `has_weight_products` — 货件中包含以重量结算；<br>- `hide_region_and_city` — 在报告中隐藏买家的地区和城市；<br>- `invoice_get` — 获取发票信息；<br>- `invoice_send` — 创建发票；<br>- `invoice_update` — 编辑发票；<br>- `label_download_big` — 下载大标签；<br>- `label_download_small` — 下载小标签；<br>- `label_download` — 下载标签；<br>- `non_int_delivered` — 转为“可能已收”状态；<br>- `non_int_delivering` — 转为“运输中”状态；<br>- `non_int_last_mile` — 转为“快递员派件中”状态；<br>- `product_cancel` — 取消部分货件中的商品；<br>- `set_cutoff` — 需要指定发货日期，请使用方法[/v1/posting/cutoff/set](#operation/PostingAPI_SetPostingCutoff)；<br>- `set_timeslot` — 修改买家的送货时间；<br>- `set_track_number` — 指定或更改追踪号；<br>- `ship_async_in_process` — 货件备货中；<br>- `ship_async_retry` — 发生错误后重新发货；<br>- `ship_async` — 备货货件；<br>- `ship_with_additional_info` — 需要填写额外信息；<br>- `ship` — 备货货件;<br>- `update_cis` — 修改附加信息。 |
| result.postings[].available_actions[] | string[] | 可用的操作和货件信息包括：<br>- `arbitration` — 提出争议；<br>- `awaiting_delivery` — 转为“等待发运”状态；<br>- `can_create_chat` — 与买家开启聊天；<br>- `cancel` — 取消货件；<br>- `click_track_number` — 在个人中心通过追踪号查看状态历史；<br>- `customer_phone_available` — 获取买家电话号码；<br>- `has_weight_products` — 货件中包含以重量结算；<br>- `hide_region_and_city` — 在报告中隐藏买家的地区和城市；<br>- `invoice_get` — 获取发票信息；<br>- `invoice_send` — 创建发票；<br>- `invoice_update` — 编辑发票；<br>- `label_download_big` — 下载大标签；<br>- `label_download_small` — 下载小标签；<br>- `label_download` — 下载标签；<br>- `non_int_delivered` — 转为“可能已收”状态；<br>- `non_int_delivering` — 转为“运输中”状态；<br>- `non_int_last_mile` — 转为“快递员派件中”状态；<br>- `product_cancel` — 取消部分货件中的商品；<br>- `set_cutoff` — 需要指定发货日期，请使用方法[/v1/posting/cutoff/set](#operation/PostingAPI_SetPostingCutoff)；<br>- `set_timeslot` — 修改买家的送货时间；<br>- `set_track_number` — 指定或更改追踪号；<br>- `ship_async_in_process` — 货件备货中；<br>- `ship_async_retry` — 发生错误后重新发货；<br>- `ship_async` — 备货货件；<br>- `ship_with_additional_info` — 需要填写额外信息；<br>- `ship` — 备货货件;<br>- `update_cis` — 修改附加信息。 |
| result.postings[].barcodes | v3Barcodes | - |
| result.postings[].barcodes.lower_barcode | string | 货件标签的下条码。 |
| result.postings[].barcodes.upper_barcode | string | 货件标签的上条码。 |
| result.postings[].cancellation | v3Cancellation | - |
| result.postings[].cancellation.affect_cancellation_rating | boolean | 如果取消影响买家排行 — `true`。 |
| result.postings[].cancellation.cancel_reason | string | 取消原因。 |
| result.postings[].cancellation.cancel_reason_id | integer | 取消货运的原因ID。 |
| result.postings[].cancellation.cancellation_initiator | string | 取消货运的发起者：<br>- `卖家`,<br>- `客户` 或`买家`,<br>- `Ozon`,<br>- `系统`,<br>- `配送服务`。 |
| result.postings[].cancellation.cancellation_type | string | 货运取消类型：<br>- `seller` — 卖家取消；<br>- `client` 或 `customer` — 买家取消；<br>- `ozon` — Ozon取消；<br>- `system`— 系统取消；<br>- `delivery` — 配送服务取消。 |
| result.postings[].cancellation.cancelled_after_ship | boolean | 如果订单在装运后取消 — `true`。 |
| result.postings[].customer | v3CustomerFbsLists | - |
| result.postings[].customer.address | v3Address | - |
| result.postings[].customer.customer_id | integer | 买家ID。 |
| result.postings[].customer.name | string | 买家姓名。 |
| result.postings[].customer.phone | string | 联系电话。<br>始终返回空字符串 `""`。 |
| result.postings[].delivering_date | string | 货件交付物流的时间。 |
| result.postings[].delivery_method | v3DeliveryMethod | - |
| result.postings[].delivery_method.id | integer | 快递方式ID。 |
| result.postings[].delivery_method.name | string | 快递方式名称。 |
| result.postings[].delivery_method.tpl_provider | string | 快递服务。 |
| result.postings[].delivery_method.tpl_provider_id | integer | 快递服务ID。 |
| result.postings[].delivery_method.warehouse | string | 仓库名称。 |
| result.postings[].delivery_method.warehouse_id | integer | 仓库ID。 |
| result.postings[].financial_data | v3PostingFinancialData | - |
| result.postings[].financial_data.cluster_from | string | 订单发送区域代码。 |
| result.postings[].financial_data.cluster_to | string | 订单接受区域代码。 |
| result.postings[].financial_data.products | PostingFinancialDataProduct[] | 订单中的商品列表。 |
| result.postings[].in_process_at | string | 开始处理货件的日期和时间。 |
| result.postings[].is_express | boolean | 如果使用快速物流 Ozon Express —— `true`。 |
| result.postings[].legal_info | v2FboSinglePostingLegalInfo | - |
| result.postings[].legal_info.company_name | string | 公司名称。 |
| result.postings[].legal_info.inn | string | 纳税人识别号（INN）。 |
| result.postings[].legal_info.kpp | string | 税务登记原因代码（KPP）。 |
| result.postings[].optional | v3FbsPostingDetailOptional | - |
| result.postings[].optional.products_with_possible_mandatory_mark | string[] | 带有可能标志的商品列表。 |
| result.postings[].order_id | integer | 货件所属订单的ID。 |
| result.postings[].order_number | string | 货件所属的订单号。 |
| result.postings[].parent_posting_number | string | 快递母件编号，从该母件中拆分出了当前货件。 |
| result.postings[].posting_number | string | 货件号。 |
| result.postings[].products | v3FbsPostingProduct[] | 货运商品列表。 |
| result.postings[].products[] | v3FbsPostingProduct[] | 货运商品列表。 |
| result.postings[].requirements | v3FbsPostingRequirementsV3 | - |
| result.postings[].requirements.products_requiring_gtd | string[] | 必须上传货运报关单号（Cargo Customs Declaration）的商品ID(SKU)的列表。<br>要配货，请上传上述商品的货运报关单号（Cargo Customs Declaration）或者有关无该号码的信息，通过方法<br>[/v3/posting/fbs/ship/package](#operation/PostingAPI_PackageShipFbsPostingV3)<br>或者 [/v3/posting/fbs/ship](#operation/PostingAPI_ShipFbsPostingV3)。 |
| result.postings[].requirements.products_requiring_country | string[] | 需要上传制造国信息的商品ID列表 (SKU)。<br>要配货，请上传上述商品的制造国信息，通过方法 [/v2/posting/fbs/product/country/set](#operation/PostingAPI_SetCountryProductFbsPostingV2)。 |
| result.postings[].requirements.products_requiring_mandatory_mark | string[] | 需要上传“诚实标志”标签的商品ID列表 (SKU)。 |
| result.postings[].requirements.products_requiring_rnpt | string[] | 商品ID列表(SKU), 需要上传商品批次注册号（Product Batch Registration Number）。 |
| result.postings[].shipment_date | string | 必须收取货件的日期和时间。 超出该时间后将适用新费率，相关信息请查看字段 `tariffication`。 |
| result.postings[].status | string | 货运状态:<br>- `acceptance_in_progress` —— 正在验收，<br>- `arbitration` —— 仲裁，<br>- `awaiting_approve` —— 等待确认，<br>- `awaiting_deliver` —— 等待装运，<br>- `awaiting_packaging` —— 等待包装，<br>- `awaiting_registration` —— 等待注册，<br>- `awaiting_verification` —— 已创建，<br>- `cancelled` —— 已取消，<br>- `cancelled_from_split_pending`——因货件拆分而取消，<br>- `client_arbitration` —— 快递客户仲裁，<br>- `delivering` —— 运输中，<br>- `driver_pickup` —— 司机处，<br>- `not_accepted` —— 分拣中心未接受，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.postings[].substatus | string | 发货子状态：<br>- `posting_acceptance_in_progress` —— 正在验收，<br>- `posting_in_arbitration` —— 仲裁，<br>- `posting_created` —— 已创建，<br>- `posting_in_carriage` —— 在运输途中，<br>- `posting_not_in_carriage` —— 未在运输中，<br>- `posting_registered` —— 已登记，<br>- `posting_transferring_to_delivery` (`status=awaiting_deliver`) —— 移交给快递，<br>- `posting_awaiting_passport_data` —— 等待护照资料，<br>- `posting_created` —— 已创建，<br>- `posting_awaiting_registration` —— 等待注册，<br>- `posting_registration_error` —— 注册错误，<br>- `posting_transferring_to_delivery` (`status=awaiting_registration`) —— 交给快递员,<br>- `posting_split_pending` —— 已创建，<br>- `posting_canceled` —— 已取消，<br>- `posting_in_client_arbitration` —— 快递会员仲裁，<br>- `posting_delivered` —— 已送达，<br>- `posting_received` —— 已收到，<br>- `posting_conditionally_delivered` —— 暂时送到，<br>- `posting_in_courier_service` —— 快递员正在路上，<br>- `posting_in_pickup_point` —— 在取货点，<br>- `posting_on_way_to_city` —— 发往城市途中，<br>- `posting_on_way_to_pickup_point` —— 正发往取货点，<br>- `posting_returned_to_warehouse` —— 返回仓库，<br>- `posting_transferred_to_courier_service` —— 转交给快递员，<br>- `posting_driver_pick_up` —— 在司机那儿，<br>- `posting_not_in_sort_center` —— 集散中心未收到，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.postings[].tpl_integration_type | string | 快递服务集成类型：<br>- `ozon` —— Ozon 快递服务。<br>- `3pl_tracking` —— 集成服务快递。<br>- `non_integrated` —— 第三方物流服务。<br>- `aggregator` —— 通过Ozon合作物流伙伴交付。<br>- `hybryd`—— 俄罗斯邮政配送方案。 |
| result.postings[].tracking_number | string | 货件跟踪号。 |
| result.postings[].tariffication | v3FbsTariffication[] | 发运的计费信息。 |
| result.postings[].tariffication[] | v3FbsTariffication[] | 发运的计费信息。 |


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
    "postings": [
      {
        "posting_number": "23713478-0018-3",
        "order_id": 559293114,
        "order_number": "33713378-0051",
        "status": "awaiting_packaging",
        "delivery_method": {
          "id": 15110442724000,
          "name": "Ozon 物流快递员，莫斯科",
          "warehouse_id": 15110442724000,
          "warehouse": "列宁街道仓库",
          "tpl_provider_id": 24,
          "tpl_provider": "Ozon Логистика"
        },
        "tracking_number": "",
        "tpl_integration_type": "ozon",
        "in_process_at": "2021-08-25T10:48:38Z",
        "shipment_date": "2021-08-26T10:00:00Z",
        "delivering_date": null,
        "optional": {
          "products_with_possible_mandatory_mark": [
            0
          ]
        },
        "cancellation": {
          "cancel_reason_id": 0,
          "cancel_reason": "",
          "cancellation_type": "",
          "cancelled_after_ship": false,
          "affect_cancellation_rating": false,
          "cancellation_initiator": ""
        },
        "customer": null,
        "products": [
          {
            "price": "1259",
            "currency_code": "RUB",
            "offer_id": "УТ-0001365",
            "name": "球，颜色： 黑色, 5千克",
            "sku": 140048123,
            "quantity": 1
          }
        ],
        "addressee": null,
        "barcodes": {
          "upper_barcode": "%101%806044518",
          "lower_barcode": "23024930500000"
        },
        "analytics_data": {
          "region": "圣彼得堡",
          "city": "圣彼得堡",
          "delivery_type": "PVZ",
          "is_premium": false,
          "payment_type_group_name": "付款卡",
          "warehouse_id": 15110442724000,
          "warehouse": "列宁街道仓库",
          "tpl_provider_id": 24,
          "tpl_provider": "Ozon物流",
          "delivery_date_begin": "2022-08-28T14:00:00Z",
          "delivery_date_end": "2022-08-28T18:00:00Z",
          "is_legal": false
        },
        "financial_data": {
          "products": [
            {
              "commission_amount": 0,
              "commission_percent": 0,
              "payout": 0,
              "product_id": 140048123,
              "old_price": 1888,
              "price": 1259,
              "total_discount_value": 629,
              "total_discount_percent": 33.32,
              "actions": [
                "卖家的系统虚拟折扣"
              ],
              "quantity": 1
            }
          ]
        },
        "is_express": false,
        "legal_info": {
          "company_name": "string",
          "inn": "string",
          "kpp": "string"
        },
        "requirements": {
          "products_requiring_gtd": [],
          "products_requiring_country": []
        },
        "tariffication": [
          {
            "current_tariff_rate": 0,
            "current_tariff_type": "",
            "current_tariff_charge": "",
            "current_tariff_charge_currency_code": "",
            "next_tariff_rate": 0,
            "next_tariff_type": "",
            "next_tariff_charge": "",
            "next_tariff_starts_at": "2023-11-13T08:05:57.657Z",
            "next_tariff_charge_currency_code": ""
          }
        ]
      }
    ],
    "count": 55
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998372.md

---

## 货件列表（第三版）

### 接口说明

返回指定时间段的货运列表-不应超过一年。
此外，您还可以按货件状态过滤货件。
`has_next = true` 在响应中表示，不是所有的货物数组都被返回。要获取有关剩余货件的信息，请提出新的含 `offset`值的请求。

### 接口标题

货件列表（第三版）

### 接口地址

`POST https://api-seller.ozon.ru/v3/posting/fbs/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingv3GetFbsPostingListRequest | 否 | 请求体。 |
| dir | body | string | 否 | 分类方向：<br>- `asc` — 从小到大，<br>- `desc` — 从大到小。 |
| filter | body | postingv3GetFbsPostingListRequestFilter | 是 | - |
| filter.delivery_method_id | body | integer[] | 否 | 快递方式ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.delivery_method_id[] | body | integer[] | 否 | 快递方式ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.fbpFilter | body | string | 否 | 从合作伙伴仓库（FBP）发货时的货件筛选器：<br>- `ALL` —  响应中将显示所有符合其他筛选器条件的货件；<br>- `ONLY` —  仅显示FBP货件；<br>- `WITHOUT` —  显示除FBP外的所有货件。<br>默认值为 `ALL`。 |
| filter.order_id | body | integer | 否 | 订单ID。 |
| filter.provider_id | body | integer[] | 否 | 快递服务ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.provider_id[] | body | integer[] | 否 | 快递服务ID。按照运输方式筛选。可以使用方法 [/v1/delivery-method/list](#operation/WarehouseAPI_DeliveryMethodList)获取。 |
| filter.since | body | string | 是 | 应收到货件清单时间段的开始日期。<br>UTC模式: ГГГГ-ММ-ДДTЧЧ:ММ:ССZ.<br>例子: 2019-08-24T14:15:22Z. |
| filter.to | body | string | 是 | 应收到货件清单时间段的结束日期。<br>UTC模式： ГГГГ-ММ-ДДTЧЧ:ММ:ССZ.<br>例子： 2019-08-24T14:15:22Z. |
| filter.status | body | string | 否 | 货件运输状态：<br>- `awaiting_registration` — 等待注册，<br>- `acceptance_in_progress` — 正在验收，<br>- `awaiting_approve` — 等待确认，<br>- `awaiting_packaging` — 等待包装，<br>- `awaiting_deliver` — 等待装运，<br>- `arbitration` — 仲裁，<br>- `client_arbitration` — 快递客户仲裁，<br>- `delivering` — 运输中，<br>- `driver_pickup` — 司机处，<br>- `delivered` — 已送达，<br>- `cancelled` — 已取消，<br>- `not_accepted` — 分拣中心未接受，<br>- `sent_by_seller` – 由卖家发送。 |
| filter.warehouse_id | body | string[] | 否 | 仓库ID。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| filter.warehouse_id[] | body | string[] | 否 | 仓库ID。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| filter.last_changed_status_date | body | postinglistV3status | 否 | - |
| filter.last_changed_status_date.from | body | string | 否 | 时期开始日期。 |
| filter.last_changed_status_date.to | body | string | 否 | 时期结束日期。 |
| limit | body | integer | 是 | 响应中值的数量：<br>- 最大值 — 1000,<br>- 最小值 — 1。 |
| offset | body | integer | 是 | 将在响应中跳过的元素数。 例如，如果“offset=10”，那么响应将从找到的第11个元素开始。 |
| with | body | postingv3FbsPostingWithParams | 否 | - |
| with.analytics_data | body | boolean | 否 | 将分析数据添加到响应中。 |
| with.barcodes | body | boolean | 否 | 将货件条形码添加到响应中。 |
| with.financial_data | body | boolean | 否 | 将财务数据添加到响应中。 |
| with.legal_info | body | boolean | 否 | 将法律信息添加到响应中。 |
| with.translit | body | boolean | 否 | 完成返回值的拼写。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v3GetFbsPostingListResponseV3Result | - |
| result.has_next | boolean | 响应中未返回整个货运数组的标志:<br>- `true` — 必须提出含其他值 `offset`的新请求，以获得其他货运信息；<br>- `false` — 响应中返回了在请求中提出的整个用于过滤的货运数组。 |
| result.postings | v3FbsPosting[] | 货运信息。 |
| result.postings[] | v3FbsPosting[] | 货运信息。 |
| result.postings[].addressee | v3AddresseeFbsLists | - |
| result.postings[].addressee.name | string | 收件人姓名。 |
| result.postings[].addressee.phone | string | 联系电话。<br>总是返回空字符串 `""`。 |
| result.postings[].analytics_data | v3FbsPostingAnalyticsData | - |
| result.postings[].analytics_data.city | string | 快递城市。仅适用于rFBS货件和独联体卖家。 |
| result.postings[].analytics_data.delivery_date_begin | string | 快递开始日期和时间。 |
| result.postings[].analytics_data.delivery_date_end | string | 快递结束日期和时间。 |
| result.postings[].analytics_data.delivery_type | string | 快递方式。 |
| result.postings[].analytics_data.is_legal | boolean | 收件人是法人的标志：<br>- `true` — 法人，<br>- `false` — 自然人。 |
| result.postings[].analytics_data.is_premium | boolean | 有Premium订阅。 |
| result.postings[].analytics_data.payment_type_group_name | string | 付款方法：<br>- `在线银行卡支付`，<br>- `Ozon卡片`，<br>- `取货时自动从Ozon卡片收费`，<br>- `收货时从已保存的银行卡收费`，<br>- `快速支付系统`，<br>- `Ozon分期付款`，<br>- `支付至结算账户`，<br>- `SberPay`。 |
| result.postings[].analytics_data.region | string | 快递地区。 |
| result.postings[].analytics_data.tpl_provider | string | 快递服务。 |
| result.postings[].analytics_data.tpl_provider_id | integer | 快递服务ID。 |
| result.postings[].analytics_data.warehouse | string | 订单发送仓库名称。 |
| result.postings[].analytics_data.warehouse_id | integer | 仓库ID。 |
| result.postings[].available_actions | string[] | 可用的操作和货件信息包括：<br>- `arbitration` — 提出争议；<br>- `awaiting_delivery` — 转为“等待发运”状态；<br>- `can_create_chat` — 与买家开启聊天；<br>- `cancel` — 取消货件；<br>- `click_track_number` — 在个人中心通过追踪号查看状态历史；<br>- `customer_phone_available` — 获取买家电话号码；<br>- `has_weight_products` — 货件中包含以重量结算；<br>- `hide_region_and_city` — 在报告中隐藏买家的地区和城市；<br>- `invoice_get` — 获取发票信息；<br>- `invoice_send` — 创建发票；<br>- `invoice_update` — 编辑发票；<br>- `label_download_big` — 下载大标签；<br>- `label_download_small` — 下载小标签；<br>- `label_download` — 下载标签；<br>- `non_int_delivered` — 转为“可能已收”状态；<br>- `non_int_delivering` — 转为“运输中”状态；<br>- `non_int_last_mile` — 转为“快递员派件中”状态；<br>- `product_cancel` — 取消部分货件中的商品；<br>- `set_cutoff` — 需要指定发货日期，请使用方法[/v1/posting/cutoff/set](#operation/PostingAPI_SetPostingCutoff)；<br>- `set_timeslot` — 修改买家的送货时间；<br>- `set_track_number` — 指定或更改追踪号；<br>- `ship_async_in_process` — 货件备货中；<br>- `ship_async_retry` — 发生错误后重新发货；<br>- `ship_async` — 备货货件；<br>- `ship_with_additional_info` — 需要填写额外信息；<br>- `ship` — 备货货件;<br>- `update_cis` — 修改附加信息。 |
| result.postings[].available_actions[] | string[] | 可用的操作和货件信息包括：<br>- `arbitration` — 提出争议；<br>- `awaiting_delivery` — 转为“等待发运”状态；<br>- `can_create_chat` — 与买家开启聊天；<br>- `cancel` — 取消货件；<br>- `click_track_number` — 在个人中心通过追踪号查看状态历史；<br>- `customer_phone_available` — 获取买家电话号码；<br>- `has_weight_products` — 货件中包含以重量结算；<br>- `hide_region_and_city` — 在报告中隐藏买家的地区和城市；<br>- `invoice_get` — 获取发票信息；<br>- `invoice_send` — 创建发票；<br>- `invoice_update` — 编辑发票；<br>- `label_download_big` — 下载大标签；<br>- `label_download_small` — 下载小标签；<br>- `label_download` — 下载标签；<br>- `non_int_delivered` — 转为“可能已收”状态；<br>- `non_int_delivering` — 转为“运输中”状态；<br>- `non_int_last_mile` — 转为“快递员派件中”状态；<br>- `product_cancel` — 取消部分货件中的商品；<br>- `set_cutoff` — 需要指定发货日期，请使用方法[/v1/posting/cutoff/set](#operation/PostingAPI_SetPostingCutoff)；<br>- `set_timeslot` — 修改买家的送货时间；<br>- `set_track_number` — 指定或更改追踪号；<br>- `ship_async_in_process` — 货件备货中；<br>- `ship_async_retry` — 发生错误后重新发货；<br>- `ship_async` — 备货货件；<br>- `ship_with_additional_info` — 需要填写额外信息；<br>- `ship` — 备货货件;<br>- `update_cis` — 修改附加信息。 |
| result.postings[].barcodes | v3Barcodes | - |
| result.postings[].barcodes.lower_barcode | string | 货件标签的下条码。 |
| result.postings[].barcodes.upper_barcode | string | 货件标签的上条码。 |
| result.postings[].cancellation | v3Cancellation | - |
| result.postings[].cancellation.affect_cancellation_rating | boolean | 如果取消影响买家排行 — `true`。 |
| result.postings[].cancellation.cancel_reason | string | 取消原因。 |
| result.postings[].cancellation.cancel_reason_id | integer | 取消货运的原因ID。 |
| result.postings[].cancellation.cancellation_initiator | string | 取消货运的发起者：<br>- `卖家`,<br>- `客户` 或`买家`,<br>- `Ozon`,<br>- `系统`,<br>- `配送服务`。 |
| result.postings[].cancellation.cancellation_type | string | 货运取消类型：<br>- `seller` — 卖家取消；<br>- `client` 或 `customer` — 买家取消；<br>- `ozon` — Ozon取消；<br>- `system`— 系统取消；<br>- `delivery` — 配送服务取消。 |
| result.postings[].cancellation.cancelled_after_ship | boolean | 如果订单在装运后取消 — `true`。 |
| result.postings[].customer | v3CustomerFbsLists | - |
| result.postings[].customer.address | v3Address | - |
| result.postings[].customer.customer_id | integer | 买家ID。 |
| result.postings[].customer.name | string | 买家姓名。 |
| result.postings[].customer.phone | string | 联系电话。<br>始终返回空字符串 `""`。 |
| result.postings[].delivering_date | string | 货件交付物流的时间。 |
| result.postings[].delivery_method | v3DeliveryMethod | - |
| result.postings[].delivery_method.id | integer | 快递方式ID。 |
| result.postings[].delivery_method.name | string | 快递方式名称。 |
| result.postings[].delivery_method.tpl_provider | string | 快递服务。 |
| result.postings[].delivery_method.tpl_provider_id | integer | 快递服务ID。 |
| result.postings[].delivery_method.warehouse | string | 仓库名称。 |
| result.postings[].delivery_method.warehouse_id | integer | 仓库ID。 |
| result.postings[].financial_data | v3PostingFinancialData | - |
| result.postings[].financial_data.cluster_from | string | 订单发送区域代码。 |
| result.postings[].financial_data.cluster_to | string | 订单接受区域代码。 |
| result.postings[].financial_data.products | PostingFinancialDataProduct[] | 订单中的商品列表。 |
| result.postings[].in_process_at | string | 开始处理货件的日期和时间。 |
| result.postings[].is_express | boolean | 如果使用快速物流 Ozon Express —— `true`。 |
| result.postings[].legal_info | v2FboSinglePostingLegalInfo | - |
| result.postings[].legal_info.company_name | string | 公司名称。 |
| result.postings[].legal_info.inn | string | 纳税人识别号（INN）。 |
| result.postings[].legal_info.kpp | string | 税务登记原因代码（KPP）。 |
| result.postings[].optional | v3FbsPostingDetailOptional | - |
| result.postings[].optional.products_with_possible_mandatory_mark | string[] | 带有可能标志的商品列表。 |
| result.postings[].order_id | integer | 货件所属订单的ID。 |
| result.postings[].order_number | string | 货件所属的订单号。 |
| result.postings[].parent_posting_number | string | 快递母件编号，从该母件中拆分出了当前货件。 |
| result.postings[].posting_number | string | 货件号。 |
| result.postings[].products | v3FbsPostingProduct[] | 货运商品列表。 |
| result.postings[].products[] | v3FbsPostingProduct[] | 货运商品列表。 |
| result.postings[].requirements | v3FbsPostingRequirementsV3 | - |
| result.postings[].requirements.products_requiring_gtd | string[] | 必须上传货运报关单号（Cargo Customs Declaration）的商品ID(SKU)的列表。<br>要配货，请上传上述商品的货运报关单号（Cargo Customs Declaration）或者有关无该号码的信息，通过方法<br>[/v3/posting/fbs/ship/package](#operation/PostingAPI_PackageShipFbsPostingV3)<br>或者 [/v3/posting/fbs/ship](#operation/PostingAPI_ShipFbsPostingV3)。 |
| result.postings[].requirements.products_requiring_country | string[] | 需要上传制造国信息的商品ID列表 (SKU)。<br>要配货，请上传上述商品的制造国信息，通过方法 [/v2/posting/fbs/product/country/set](#operation/PostingAPI_SetCountryProductFbsPostingV2)。 |
| result.postings[].requirements.products_requiring_mandatory_mark | string[] | 需要上传“诚实标志”标签的商品ID列表 (SKU)。 |
| result.postings[].requirements.products_requiring_rnpt | string[] | 商品ID列表(SKU), 需要上传商品批次注册号（Product Batch Registration Number）。 |
| result.postings[].shipment_date | string | 必须收取货件的日期和时间。 超出该时间后将适用新费率，相关信息请查看字段 `tariffication`。 |
| result.postings[].status | string | 货运状态:<br>- `acceptance_in_progress` —— 正在验收，<br>- `arbitration` —— 仲裁，<br>- `awaiting_approve` —— 等待确认，<br>- `awaiting_deliver` —— 等待装运，<br>- `awaiting_packaging` —— 等待包装，<br>- `awaiting_registration` —— 等待注册，<br>- `awaiting_verification` —— 已创建，<br>- `cancelled` —— 已取消，<br>- `cancelled_from_split_pending`——因货件拆分而取消，<br>- `client_arbitration` —— 快递客户仲裁，<br>- `delivering` —— 运输中，<br>- `driver_pickup` —— 司机处，<br>- `not_accepted` —— 分拣中心未接受，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.postings[].substatus | string | 发货子状态：<br>- `posting_acceptance_in_progress` —— 正在验收，<br>- `posting_in_arbitration` —— 仲裁，<br>- `posting_created` —— 已创建，<br>- `posting_in_carriage` —— 在运输途中，<br>- `posting_not_in_carriage` —— 未在运输中，<br>- `posting_registered` —— 已登记，<br>- `posting_transferring_to_delivery` (`status=awaiting_deliver`) —— 移交给快递，<br>- `posting_awaiting_passport_data` —— 等待护照资料，<br>- `posting_created` —— 已创建，<br>- `posting_awaiting_registration` —— 等待注册，<br>- `posting_registration_error` —— 注册错误，<br>- `posting_transferring_to_delivery` (`status=awaiting_registration`) —— 交给快递员,<br>- `posting_split_pending` —— 已创建，<br>- `posting_canceled` —— 已取消，<br>- `posting_in_client_arbitration` —— 快递会员仲裁，<br>- `posting_delivered` —— 已送达，<br>- `posting_received` —— 已收到，<br>- `posting_conditionally_delivered` —— 暂时送到，<br>- `posting_in_courier_service` —— 快递员正在路上，<br>- `posting_in_pickup_point` —— 在取货点，<br>- `posting_on_way_to_city` —— 发往城市途中，<br>- `posting_on_way_to_pickup_point` —— 正发往取货点，<br>- `posting_returned_to_warehouse` —— 返回仓库，<br>- `posting_transferred_to_courier_service` —— 转交给快递员，<br>- `posting_driver_pick_up` —— 在司机那儿，<br>- `posting_not_in_sort_center` —— 集散中心未收到，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.postings[].tpl_integration_type | string | 快递服务集成类型：<br>- `ozon` —— Ozon 快递服务。<br>- `3pl_tracking` —— 集成服务快递。<br>- `non_integrated` —— 第三方物流服务。<br>- `aggregator` —— 通过Ozon合作物流伙伴交付。<br>- `hybryd`—— 俄罗斯邮政配送方案。 |
| result.postings[].tracking_number | string | 货件跟踪号。 |
| result.postings[].tariffication | v3FbsTariffication[] | 发运的计费信息。 |
| result.postings[].tariffication[] | v3FbsTariffication[] | 发运的计费信息。 |


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
    "postings": [
      {
        "posting_number": "05708065-0029-1",
        "order_id": 680420041,
        "order_number": "05708065-0029",
        "status": "awaiting_deliver",
        "substatus": "posting_awaiting_passport_data",
        "delivery_method": {
          "id": 21321684811000,
          "name": "Ozon独立物流, 克拉斯诺戈尔斯克",
          "warehouse_id": 21321684811000,
          "warehouse": "Steam Toys Nahabino",
          "tpl_provider_id": 24,
          "tpl_provider": "Ozon物流"
        },
        "tracking_number": "",
        "tpl_integration_type": "ozon",
        "in_process_at": "2022-05-13T07:07:32Z",
        "shipment_date": "2022-05-13T10:00:00Z",
        "delivering_date": null,
        "optional": {
          "products_with_possible_mandatory_mark": [
            0
          ]
        },
        "cancellation": {
          "cancel_reason_id": 0,
          "cancel_reason": "",
          "cancellation_type": "",
          "cancelled_after_ship": false,
          "affect_cancellation_rating": false,
          "cancellation_initiator": ""
        },
        "customer": null,
        "products": [
          {
            "price": "1390.000000",
            "currency_code": "RUB",
            "offer_id": "205953",
            "name": " Electronic designer PinLab Positronic",
            "sku": 358924380,
            "quantity": 1
          }
        ],
        "addressee": null,
        "barcodes": null,
        "analytics_data": null,
        "financial_data": null,
        "is_express": false,
        "legal_info": {
          "company_name": "string",
          "inn": "string",
          "kpp": "string"
        },
        "requirements": {
          "products_requiring_gtd": [],
          "products_requiring_country": [],
          "products_requiring_mandatory_mark": []
        },
        "tariffication": [
          {
            "current_tariff_rate": 0,
            "current_tariff_type": "",
            "current_tariff_charge": "",
            "current_tariff_charge_currency_code": "",
            "next_tariff_rate": 0,
            "next_tariff_type": "",
            "next_tariff_charge": "",
            "next_tariff_starts_at": "2023-11-13T08:05:57.657Z",
            "next_tariff_charge_currency_code": ""
          }
        ]
      }
    ],
    "has_next": true
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998373.md

---

## 按照ID获取货件信息

### 接口说明

暂无接口说明。

### 接口标题

按照ID获取货件信息

### 接口地址

`POST https://api-seller.ozon.ru/v3/posting/fbs/get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingv3GetFbsPostingRequest | 否 | 请求体。 |
| posting_number | body | string | 是 | 货件ID。 |
| with | body | postingv3FbsPostingWithParamsExamplars | 否 | - |
| with.analytics_data | body | boolean | 否 | 将分析数据添加到响应中。 |
| with.barcodes | body | boolean | 否 | 将货件条形码添加到响应中。 |
| with.financial_data | body | boolean | 否 | 将财务数据添加到响应中。 |
| with.legal_info | body | boolean | 否 | 将法律信息添加到响应中。 |
| with.product_exemplars | body | boolean | 否 | 将有关产品及其份数的数据添加到响应中。 |
| with.related_postings | body | boolean | 否 | 将相关货件数量添加到响应中。 相关货件是在组装期间将母快递拆分的快递。 |
| with.translit | body | boolean | 否 | 完成返回值的拼写。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v3FbsPostingDetail | - |
| result.additional_data | v3AdditionalDataItem[] | - |
| result.additional_data[] | v3AdditionalDataItem[] | - |
| result.additional_data[].key | string | - |
| result.additional_data[].value | string | - |
| result.addressee | v3Addressee | - |
| result.addressee.name | string | 买家姓名。 |
| result.addressee.phone | string | 联系电话。<br>过时的参数，不再使用。并总是返回到空字符串 `""`。 |
| result.analytics_data | v3FbsPostingAnalyticsData | - |
| result.analytics_data.city | string | 快递城市。仅适用于rFBS货件和独联体卖家。 |
| result.analytics_data.delivery_date_begin | string | 快递开始日期和时间。 |
| result.analytics_data.delivery_date_end | string | 快递结束日期和时间。 |
| result.analytics_data.delivery_type | string | 快递方式。 |
| result.analytics_data.is_legal | boolean | 收件人是法人的标志：<br>- `true` — 法人，<br>- `false` — 自然人。 |
| result.analytics_data.is_premium | boolean | 有Premium订阅。 |
| result.analytics_data.payment_type_group_name | string | 付款方法：<br>- `在线银行卡支付`，<br>- `Ozon卡片`，<br>- `取货时自动从Ozon卡片收费`，<br>- `收货时从已保存的银行卡收费`，<br>- `快速支付系统`，<br>- `Ozon分期付款`，<br>- `支付至结算账户`，<br>- `SberPay`。 |
| result.analytics_data.region | string | 快递地区。 |
| result.analytics_data.tpl_provider | string | 快递服务。 |
| result.analytics_data.tpl_provider_id | integer | 快递服务ID。 |
| result.analytics_data.warehouse | string | 订单发送仓库名称。 |
| result.analytics_data.warehouse_id | integer | 仓库ID。 |
| result.available_actions | string[] | 可用的操作和货件信息包括：<br>- `arbitration` — 提出争议；<br>- `awaiting_delivery` — 转为“等待发运”状态；<br>- `can_create_chat` — 与买家开启聊天；<br>- `cancel` — 取消货件；<br>- `click_track_number` — 在个人中心通过追踪号查看状态历史；<br>- `customer_phone_available` — 获取买家电话号码；<br>- `has_weight_products` — 货件中包含以重量结算；<br>- `hide_region_and_city` — 在报告中隐藏买家的地区和城市；<br>- `invoice_get` — 获取发票信息；<br>- `invoice_send` — 创建发票；<br>- `invoice_update` — 编辑发票；<br>- `label_download_big` — 下载大标签；<br>- `label_download_small` — 下载小标签；<br>- `label_download` — 下载标签；<br>- `non_int_delivered` — 转为“可能已收”状态；<br>- `non_int_delivering` — 转为“运输中”状态；<br>- `non_int_last_mile` — 转为“快递员派件中”状态；<br>- `product_cancel` — 取消部分货件中的商品；<br>- `set_cutoff` — 需要指定发货日期，请使用方法[/v1/posting/cutoff/set](#operation/PostingAPI_SetPostingCutoff)；<br>- `set_timeslot` — 修改买家的送货时间；<br>- `set_track_number` — 指定或更改追踪号；<br>- `ship_async_in_process` — 货件备货中；<br>- `ship_async_retry` — 发生错误后重新发货；<br>- `ship_async` — 备货货件；<br>- `ship_with_additional_info` — 需要填写额外信息；<br>- `ship` — 备货货件;<br>- `update_cis` — 修改附加信息。 |
| result.available_actions[] | string[] | 可用的操作和货件信息包括：<br>- `arbitration` — 提出争议；<br>- `awaiting_delivery` — 转为“等待发运”状态；<br>- `can_create_chat` — 与买家开启聊天；<br>- `cancel` — 取消货件；<br>- `click_track_number` — 在个人中心通过追踪号查看状态历史；<br>- `customer_phone_available` — 获取买家电话号码；<br>- `has_weight_products` — 货件中包含以重量结算；<br>- `hide_region_and_city` — 在报告中隐藏买家的地区和城市；<br>- `invoice_get` — 获取发票信息；<br>- `invoice_send` — 创建发票；<br>- `invoice_update` — 编辑发票；<br>- `label_download_big` — 下载大标签；<br>- `label_download_small` — 下载小标签；<br>- `label_download` — 下载标签；<br>- `non_int_delivered` — 转为“可能已收”状态；<br>- `non_int_delivering` — 转为“运输中”状态；<br>- `non_int_last_mile` — 转为“快递员派件中”状态；<br>- `product_cancel` — 取消部分货件中的商品；<br>- `set_cutoff` — 需要指定发货日期，请使用方法[/v1/posting/cutoff/set](#operation/PostingAPI_SetPostingCutoff)；<br>- `set_timeslot` — 修改买家的送货时间；<br>- `set_track_number` — 指定或更改追踪号；<br>- `ship_async_in_process` — 货件备货中；<br>- `ship_async_retry` — 发生错误后重新发货；<br>- `ship_async` — 备货货件；<br>- `ship_with_additional_info` — 需要填写额外信息；<br>- `ship` — 备货货件;<br>- `update_cis` — 修改附加信息。 |
| result.barcodes | v3Barcodes | - |
| result.barcodes.lower_barcode | string | 货件标签的下条码。 |
| result.barcodes.upper_barcode | string | 货件标签的上条码。 |
| result.cancellation | v3Cancellation | - |
| result.cancellation.affect_cancellation_rating | boolean | 如果取消影响买家排行 — `true`。 |
| result.cancellation.cancel_reason | string | 取消原因。 |
| result.cancellation.cancel_reason_id | integer | 取消货运的原因ID。 |
| result.cancellation.cancellation_initiator | string | 取消货运的发起者：<br>- `卖家`,<br>- `客户` 或`买家`,<br>- `Ozon`,<br>- `系统`,<br>- `配送服务`。 |
| result.cancellation.cancellation_type | string | 货运取消类型：<br>- `seller` — 卖家取消；<br>- `client` 或 `customer` — 买家取消；<br>- `ozon` — Ozon取消；<br>- `system`— 系统取消；<br>- `delivery` — 配送服务取消。 |
| result.cancellation.cancelled_after_ship | boolean | 如果订单在装运后取消 — `true`。 |
| result.courier | FbsPostingDetailCourier | - |
| result.courier.car_model | string | 汽车型号。 |
| result.courier.car_number | string | 车牌号。 |
| result.courier.name | string | 快递员全名。 |
| result.courier.phone | string | 快递员电话。<br>过时的参数，不再使用。并总是返回到空字符串 `""`。 |
| result.customer | v3Customer | - |
| result.customer.address | v3Address | - |
| result.customer.address.address_tail | string | 文本格式的地址。 |
| result.customer.address.city | string | 快递城市。 |
| result.customer.address.comment | string | 订单评价。 |
| result.customer.address.country | string | 快递国家。 |
| result.customer.address.district | string | 快递地区。 |
| result.customer.address.latitude | number | 宽。 |
| result.customer.address.longitude | number | （时间的）长度。 |
| result.customer.address.provider_pvz_code | string | 3PL提供商的订单提货点的代码。 |
| result.customer.address.pvz_code | integer | 订单取货点代码。 |
| result.customer.address.region | string | 快递区域。 |
| result.customer.address.zip_code | string | 收件人邮编。 |
| result.customer.customer_id | integer | 买家ID。 |
| result.customer.name | string | 买家姓名。 |
| result.customer.phone | string | 联系电话。<br>过时的参数，不再使用。并总是返回到空字符串 `""`。 |
| result.delivering_date | string | 货件交付物流的时间。 |
| result.delivery_method | v3DeliveryMethod | - |
| result.delivery_method.id | integer | 快递方式ID。 |
| result.delivery_method.name | string | 快递方式名称。 |
| result.delivery_method.tpl_provider | string | 快递服务。 |
| result.delivery_method.tpl_provider_id | integer | 快递服务ID。 |
| result.delivery_method.warehouse | string | 仓库名称。 |
| result.delivery_method.warehouse_id | integer | 仓库ID。 |
| result.delivery_price | string | 物流价格。 |
| result.financial_data | v3PostingFinancialData | - |
| result.financial_data.cluster_from | string | 订单发送区域代码。 |
| result.financial_data.cluster_to | string | 订单接受区域代码。 |
| result.financial_data.products | PostingFinancialDataProduct[] | 订单中的商品列表。 |
| result.financial_data.products[] | PostingFinancialDataProduct[] | 订单中的商品列表。 |
| result.financial_data.products[].actions | string[] | 行为。 |
| result.financial_data.products[].currency_code | string | 价格货币，其与个人中心中设置的币种相匹配。<br>可能的值：<br>- `RUB` — 俄罗斯卢布，<br>- `BYN` — 白俄罗斯卢布，<br>- `KZT` — 坚戈，<br>- `EUR` — 欧元，<br>- `USD` — 美元，<br>- `CNY` — 元。 |
| result.financial_data.products[].commission_amount | number | 商品佣金大小。 |
| result.financial_data.products[].commission_percent | integer | 佣金百分比。 |
| result.financial_data.products[].commissions_currency_code | string | 计算佣金的币种代码。 |
| result.financial_data.products[].old_price | number | 打折前价格。在商品卡片上将被显示划掉。 |
| result.financial_data.products[].payout | number | 支付给卖方。 |
| result.financial_data.products[].price | number | 打折后的商品价格 - 该值显示在商品卡片上。 |
| result.financial_data.products[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result.financial_data.products[].quantity | integer | 运输商品数量。 |
| result.financial_data.products[].total_discount_percent | number | 折扣百分比。 |
| result.financial_data.products[].total_discount_value | number | 折扣数量。 |
| result.in_process_at | string | 开始处理货件的日期和时间。 |
| result.is_express | boolean | 如果使用了快速物流Ozon Express —— `true`。 |
| result.legal_info | v2FboSinglePostingLegalInfo | - |
| result.legal_info.company_name | string | 公司名称。 |
| result.legal_info.inn | string | 纳税人识别号（INN）。 |
| result.legal_info.kpp | string | 税务登记原因代码（KPP）。 |
| result.optional | v3FbsPostingDetailOptional | - |
| result.optional.products_with_possible_mandatory_mark | string[] | 带有可能标志的商品列表。 |
| result.optional.products_with_possible_mandatory_mark[] | string[] | 带有可能标志的商品列表。 |
| result.order_id | integer | 货件所属的订单ID。 |
| result.order_number | string | 货件所属的订单号。 |
| result.parent_posting_number | string | 母件编号，由该母件拆分出了该货件。 |
| result.posting_number | string | 货件号。 |
| result.product_exemplars | v3FbsPostingProductExemplarsV3 | - |
| result.product_exemplars.products | v3FbsPostingExemplarProductV3[] | - |
| result.product_exemplars.products[] | v3FbsPostingExemplarProductV3[] | - |
| result.product_exemplars.products[].exemplars | v3FbsPostingProductExemplarInfoV3[] | 按副本的信息。 |
| result.product_exemplars.products[].sku | integer | 在Ozon系统中的产品ID — SKU。 |
| result.products | v3PostingProductDetail[] | 货物装运的数组。 |
| result.products[] | v3PostingProductDetail[] | 货物装运的数组。 |
| result.products[].dimensions | v3Dimensions | - |
| result.products[].dimensions.height | string | 包装高度。 |
| result.products[].dimensions.length | string | 商品长度。 |
| result.products[].dimensions.weight | string | 商品包装重量。 |
| result.products[].dimensions.width | string | 包装宽度。 |
| result.products[].mandatory_mark | string[] | 商品强制性标签。 |
| result.products[].mandatory_mark[] | string[] | 商品强制性标签。 |
| result.products[].name | string | 名称。 |
| result.products[].offer_id | string | 卖家系统中的商品ID — 货号。 |
| result.products[].price | string | 折扣后商品价格 — 该值在商品卡片上显示。 |
| result.products[].currency_code | string | 价格显示的货币，其与个人中心中设置的币种相匹配。<br>-`RUB` — 俄罗斯卢布，<br>- `BYN` — 白俄罗斯卢布，<br>- `KZT` — 坚戈，<br>- `EUR` — 欧元，<br>- `USD` — 美元，<br>- `CNY` — 元。 |
| result.products[].quantity | integer | 商品数量。 |
| result.products[].sku | integer | Ozon卖家系统中的商品标识符 — `product_id`。 |
| result.provider_status | string | 快递服务状态。 |
| result.related_postings | v3FbsPostingDetailRelatedPostings | - |
| result.related_postings.related_posting_numbers | string[] | 相关货件号码列表。 |
| result.related_postings.related_posting_numbers[] | string[] | 相关货件号码列表。 |
| result.requirements | v3FbsPostingRequirementsV3 | - |
| result.requirements.products_requiring_gtd | string[] | 必须上传货运报关单号（Cargo Customs Declaration）的商品ID(SKU)的列表。<br>要配货，请上传上述商品的货运报关单号（Cargo Customs Declaration）或者有关无该号码的信息，通过方法<br>[/v3/posting/fbs/ship/package](#operation/PostingAPI_PackageShipFbsPostingV3)<br>或者 [/v3/posting/fbs/ship](#operation/PostingAPI_ShipFbsPostingV3)。 |
| result.requirements.products_requiring_gtd[] | string[] | 必须上传货运报关单号（Cargo Customs Declaration）的商品ID(SKU)的列表。<br>要配货，请上传上述商品的货运报关单号（Cargo Customs Declaration）或者有关无该号码的信息，通过方法<br>[/v3/posting/fbs/ship/package](#operation/PostingAPI_PackageShipFbsPostingV3)<br>或者 [/v3/posting/fbs/ship](#operation/PostingAPI_ShipFbsPostingV3)。 |
| result.requirements.products_requiring_country | string[] | 需要上传制造国信息的商品ID列表 (SKU)。<br>要配货，请上传上述商品的制造国信息，通过方法 [/v2/posting/fbs/product/country/set](#operation/PostingAPI_SetCountryProductFbsPostingV2)。 |
| result.requirements.products_requiring_country[] | string[] | 需要上传制造国信息的商品ID列表 (SKU)。<br>要配货，请上传上述商品的制造国信息，通过方法 [/v2/posting/fbs/product/country/set](#operation/PostingAPI_SetCountryProductFbsPostingV2)。 |
| result.requirements.products_requiring_mandatory_mark | string[] | 需要上传“诚实标志”标签的商品ID列表 (SKU)。 |
| result.requirements.products_requiring_mandatory_mark[] | string[] | 需要上传“诚实标志”标签的商品ID列表 (SKU)。 |
| result.requirements.products_requiring_rnpt | string[] | 商品ID列表(SKU), 需要上传商品批次注册号（Product Batch Registration Number）。 |
| result.requirements.products_requiring_rnpt[] | string[] | 商品ID列表(SKU), 需要上传商品批次注册号（Product Batch Registration Number）。 |
| result.shipment_date | string | 必须完成货件装配的日期和时间。 如果在此日期之前未完成货件装配，则运输自动取消。 |
| result.status | string | 货运状态:<br>- `acceptance_in_progress` —— 正在验收，<br>- `arbitration` —— 仲裁，<br>- `awaiting_approve` —— 等待确认，<br>- `awaiting_deliver` —— 等待装运，<br>- `awaiting_packaging` —— 等待包装，<br>- `awaiting_registration` —— 等待注册，<br>- `awaiting_verification` —— 已创建，<br>- `cancelled` —— 已取消，<br>- `cancelled_from_split_pending`——因货件拆分而取消，<br>- `client_arbitration` —— 快递客户仲裁，<br>- `delivered` —— 已送达，<br>- `delivering` —— 运输中，<br>- `driver_pickup` —— 司机处，<br>- `not_accepted` —— 分拣中心未接受，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.substatus | string | 发货子状态：<br>- `posting_acceptance_in_progress` —— 正在验收，<br>- `posting_in_arbitration` —— 仲裁，<br>- `posting_created` —— 已创建，<br>- `posting_in_carriage` —— 在运输途中，<br>- `posting_not_in_carriage` —— 未在运输中，<br>- `posting_registered` —— 已登记，<br>- `posting_transferring_to_delivery` (`status=awaiting_deliver`) —— 移交给快递，<br>- `posting_awaiting_passport_data` —— 等待护照资料，<br>- `posting_created` —— 已创建，<br>- `posting_awaiting_registration` —— 等待注册，<br>- `posting_registration_error` —— 注册错误，<br>- `posting_transferring_to_delivery` (`status=awaiting_registration`) —— 交给快递员,<br>- `posting_split_pending` —— 已创建，<br>- `posting_canceled` —— 已取消，<br>- `posting_in_client_arbitration` —— 快递会员仲裁，<br>- `posting_delivered` —— 已送达，<br>- `posting_received` —— 已收到，<br>- `posting_conditionally_delivered` —— 暂时送到，<br>- `posting_in_courier_service` —— 快递员正在路上，<br>- `posting_in_pickup_point` —— 在取货点，<br>- `posting_on_way_to_city` —— 发往城市途中，<br>- `posting_on_way_to_pickup_point` —— 正发往取货点，<br>- `posting_returned_to_warehouse` —— 返回仓库，<br>- `posting_transferred_to_courier_service` —— 转交给快递员，<br>- `posting_driver_pick_up` —— 在司机那儿，<br>- `posting_not_in_sort_center` —— 集散中心未收到，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.previous_substatus | string | 货件的前一个子状态。可能的取值：<br>- `posting_acceptance_in_progress` —— 正在验收，<br>- `posting_in_arbitration` —— 仲裁，<br>- `posting_created` —— 已创建，<br>- `posting_in_carriage` —— 在运输途中，<br>- `posting_not_in_carriage` —— 未在运输中，<br>- `posting_registered` —— 已登记，<br>- `posting_transferring_to_delivery` (`status=awaiting_deliver`) —— 移交给快递，<br>- `posting_awaiting_passport_data` —— 等待护照资料，<br>- `posting_created` —— 已创建，<br>- `posting_awaiting_registration` —— 等待注册，<br>- `posting_registration_error` —— 注册错误，<br>- `posting_transferring_to_delivery` (`status=awaiting_registration`) —— 交给快递员,<br>- `posting_split_pending` —— 已创建，<br>- `posting_canceled` —— 已取消，<br>- `posting_in_client_arbitration` —— 快递会员仲裁，<br>- `posting_delivered` —— 已送达，<br>- `posting_received` —— 已收到，<br>- `posting_conditionally_delivered` —— 暂时送到，<br>- `posting_in_courier_service` —— 快递员正在路上，<br>- `posting_in_pickup_point` —— 在取货点，<br>- `posting_on_way_to_city` —— 发往城市途中，<br>- `posting_on_way_to_pickup_point` —— 正发往取货点，<br>- `posting_returned_to_warehouse` —— 返回仓库，<br>- `posting_transferred_to_courier_service` —— 转交给快递员，<br>- `posting_driver_pick_up` —— 在司机那儿，<br>- `posting_not_in_sort_center` —— 集散中心未收到，<br>- `sent_by_seller` —— 由卖家发送。 |
| result.tpl_integration_type | string | 快递服务集成类型：<br>- `ozon` —— 通过Ozon物流的快递。<br>- `aggregator` —— 外部服务快递，Ozon注册订单。<br>- `3pl_tracking` —— 外部服务快递，卖家注册订单。<br>- `non_integrated` —— 卖家自行配送物流。 |
| result.tracking_number | string | 货件跟踪号。 |
| result.tariffication | v3FbsTariffication[] | 发运的计费信息。 |
| result.tariffication[] | v3FbsTariffication[] | 发运的计费信息。 |
| result.tariffication[].current_tariff_rate | number | 当前运费的百分比。 |
| result.tariffication[].current_tariff_type | string | 当前的计费类型 — 折扣或附加费。 |
| result.tariffication[].current_tariff_charge | string | 当前的折扣或附加费金额。 |
| result.tariffication[].current_tariff_charge_currency_code | string | 金额的货币单位。 |
| result.tariffication[].next_tariff_rate | number | 在参数 `next_tariff_starts_at` 指定的时间后，将按此百分比进行计费。 |
| result.tariffication[].next_tariff_type | string | 在参数 `next_tariff_starts_at` 指定的时间后，将按此类型计费 — 折扣或附加费。 |
| result.tariffication[].next_tariff_charge | string | 下一步计费中的折扣或附加金额。 |
| result.tariffication[].next_tariff_starts_at | string | 新的费率开始生效的日期和时间。<br>格式：`YYYY-MM-DDThh:mm:ss.mcsZ`.<br>示例：`2023-11-13T08:05:57.657Z`. |
| result.tariffication[].next_tariff_charge_currency_code | string | 新费率的货币单位。 |


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
    "posting_number": "57195475-0050-3",
    "order_id": 438764970,
    "order_number": "57195475-0050",
    "status": "awaiting_packaging",
    "substatus": "posting_awaiting_passport_data",
    "previous_substatus": "posting_transferring_to_delivery",
    "delivery_method": {
      "id": 18114520187000,
      "name": "Ozon独立物流，莫斯科",
      "warehouse_id": 18114520187000,
      "warehouse": "莫斯科主要",
      "tpl_provider_id": 24,
      "tpl_provider": "Ozon物流"
    },
    "tracking_number": "",
    "tpl_integration_type": "ozon",
    "in_process_at": "2021-11-20T09:14:16Z",
    "shipment_date": "2021-11-23T10:00:00Z",
    "delivering_date": null,
    "provider_status": "",
    "delivery_price": "",
    "optional": {
      "products_with_possible_mandatory_mark": [
        0
      ]
    },
    "cancellation": {
      "cancel_reason_id": 0,
      "cancel_reason": "",
      "cancellation_type": "",
      "cancelled_after_ship": false,
      "affect_cancellation_rating": false,
      "cancellation_initiator": ""
    },
    "customer": null,
    "addressee": null,
    "products": [
      {
        "currency_code": "RUB",
        "price": "279.0000",
        "offer_id": "250-7898-1",
        "name": "醇香咖啡 \"巧克力香橙\" 250克",
        "sku": 180550365,
        "quantity": 1,
        "dimensions": {
          "height": "40.00",
          "length": "240.00",
          "weight": "260",
          "width": "140.00"
        }
      }
    ],
    "barcodes": null,
    "analytics_data": null,
    "financial_data": null,
    "additional_data": [],
    "is_express": false,
    "legal_info": {
      "company_name": "string",
      "inn": "string",
      "kpp": "string"
    },
    "related_postings": {
      "related_posting_numbers": [
        "string"
      ]
    },
    "requirements": {
      "products_requiring_gtd": [],
      "products_requiring_country": []
    },
    "product_exemplars": null,
    "tariffication": [
      {
        "current_tariff_rate": 0,
        "current_tariff_type": "",
        "current_tariff_charge": "",
        "current_tariff_charge_currency_code": "",
        "next_tariff_rate": 0,
        "next_tariff_type": "",
        "next_tariff_charge": "",
        "next_tariff_starts_at": "2023-11-13T08:05:57.657Z",
        "next_tariff_charge_currency_code": ""
      }
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998374.md

---

## 按条形码获取有关货件的信息

### 接口说明

暂无接口说明。

### 接口标题

按条形码获取有关货件的信息

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/get-by-barcode`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingGetFbsPostingByBarcodeRequest | 否 | 请求体。 |
| barcode | body | string | 否 | 货运条形码。可以使用以下方法获取： [/v3/posting/fbs/get](#operation/PostingAPI_GetFbsPostingV3)、[/v3/posting/fbs/list](#operation/PostingAPI_GetFbsPostingListV3) 和 [/v3/posting/fbs/unfulfilled/list](#operation/PostingAPI_GetFbsPostingUnfulfilledList)， 在`barcodes`数组中获取数据。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v2FbsPosting | - |
| result.analytics_data | FbsPostingFbsPostingAnalyticsData | - |
| result.analytics_data.city | string | 快递城市。 |
| result.analytics_data.delivery_type | string | 快递方式。 |
| result.analytics_data.is_legal | boolean | 收件人是法人的标志：<br>- `true` — 法人，<br>- `false` — 自然人。 |
| result.analytics_data.is_premium | boolean | 有Premium订阅。 |
| result.analytics_data.payment_type_group_name | string | 付款方法：<br>- `在线银行卡支付`，<br>- `Ozon卡片`，<br>- `取货时自动从Ozon卡片收费`，<br>- `收货时从已保存的银行卡收费`，<br>- `快速支付系统`，<br>- `Ozon分期付款`，<br>- `支付至结算账户`，<br>- `SberPay`。 |
| result.analytics_data.region | string | 快递区域。 |
| result.barcodes | FbsPostingBarcodes | - |
| result.barcodes.lower_barcode | string | 货件标签的下条形码。 |
| result.barcodes.upper_barcode | string | 货件标签的上条形码。 |
| result.cancel_reason_id | integer | 取消装运原因ID。 |
| result.created_at | string | 创建装运日期和时间。 |
| result.financial_data | v2PostingFinancialData | - |
| result.financial_data.cluster_from | string | 发货地的地区代码。 |
| result.financial_data.cluster_to | string | 收货地的地区代码。 |
| result.financial_data.products | PostingFinancialDataProduct[] | 订单中的商品列表。 |
| result.financial_data.products[] | PostingFinancialDataProduct[] | 订单中的商品列表。 |
| result.financial_data.products[].actions | string[] | 行为。 |
| result.financial_data.products[].currency_code | string | 价格货币，其与个人中心中设置的币种相匹配。<br>可能的值：<br>- `RUB` — 俄罗斯卢布，<br>- `BYN` — 白俄罗斯卢布，<br>- `KZT` — 坚戈，<br>- `EUR` — 欧元，<br>- `USD` — 美元，<br>- `CNY` — 元。 |
| result.financial_data.products[].commission_amount | number | 商品佣金大小。 |
| result.financial_data.products[].commission_percent | integer | 佣金百分比。 |
| result.financial_data.products[].commissions_currency_code | string | 计算佣金的币种代码。 |
| result.financial_data.products[].old_price | number | 打折前价格。在商品卡片上将被显示划掉。 |
| result.financial_data.products[].payout | number | 支付给卖方。 |
| result.financial_data.products[].price | number | 打折后的商品价格 - 该值显示在商品卡片上。 |
| result.financial_data.products[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result.financial_data.products[].quantity | integer | 运输商品数量。 |
| result.financial_data.products[].total_discount_percent | number | 折扣百分比。 |
| result.financial_data.products[].total_discount_value | number | 折扣数量。 |
| result.in_process_at | string | 开始处理货件的日期和时间。 |
| result.order_id | integer | 货运所属订单ID。 |
| result.order_number | string | 货运所属的订单号。 |
| result.posting_number | string | 货运号。 |
| result.products | v2FbsPostingProduct[] | 货运商品列表。 |
| result.products[] | v2FbsPostingProduct[] | 货运商品列表。 |
| result.products[].name | string | 商品名称。 |
| result.products[].offer_id | string | 卖家系统中的商品ID — 货号。 |
| result.products[].price | string | 商品价格。 |
| result.products[].quantity | integer | 货运商品数量。 |
| result.products[].sku | integer | Ozon系统中的卖家系统中的商品标识符 — `product_id`。 |
| result.shipment_date | string | 必须收取货件的日期和时间。 如果在此日期之前未完成配货，则货运自动取消。 |
| result.status | string | 货运状态。 |


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
    "posting_number": "57195475-0050-3",
    "order_id": 438764970,
    "order_number": "57195475-0050",
    "status": "awaiting_packaging",
    "delivery_method": {
      "id": 18114520187000,
      "name": "Ozon独立物流，莫斯科",
      "warehouse_id": 18114520187000,
      "warehouse": "莫斯科主要",
      "tpl_provider_id": 24,
      "tpl_provider": "Ozon物流"
    },
    "tracking_number": "",
    "tpl_integration_type": "ozon",
    "in_process_at": "2021-11-20T09:14:16Z",
    "shipment_date": "2021-11-23T10:00:00Z",
    "delivering_date": null,
    "provider_status": "",
    "delivery_price": "",
    "cancellation": {
      "cancel_reason_id": 0,
      "cancel_reason": "",
      "cancellation_type": "",
      "cancelled_after_ship": false,
      "affect_cancellation_rating": false,
      "cancellation_initiator": ""
    },
    "customer": null,
    "addressee": null,
    "products": [
      {
        "price": "279.0000",
        "offer_id": "250-7898-1",
        "name": "醇香咖啡 \"巧克力味香橙\" 250 гр",
        "sku": 180550365,
        "quantity": 1,
        "dimensions": {
          "height": "40.00",
          "length": "240.00",
          "weight": "260",
          "width": "140.00"
        }
      }
    ],
    "barcodes": null,
    "analytics_data": null,
    "financial_data": null,
    "additional_data": [],
    "is_express": false,
    "requirements": {
      "products_requiring_gtd": [],
      "products_requiring_country": []
    },
    "product_exemplars": null
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998375.md

---

## 可用产地名单

### 接口说明

获取可用产地及其ISO代码列表的方法。

### 接口标题

可用产地名单

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/product/country/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v2FbsPostingProductCountryListRequest | 否 | 请求体。 |
| name_search | body | string | 否 | 按行过滤。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v2FbsPostingProductCountryListResponseResult[] | 制造国和ISO代码列表。 |
| result[] | v2FbsPostingProductCountryListResponseResult[] | 制造国和ISO代码列表。 |
| result[].name | string | 国家俄语名称 |
| result[].country_iso_code | string | ISO国家代码。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | - |
| details | protobufAny[] | - |
| details[] | protobufAny[] | - |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | - |


### 响应示例

```json
{
  "result": [
    {
      "name": "阿尔及利亚",
      "country_iso_code": "DZ"
    },
    {
      "name": "安圭拉",
      "country_iso_code": "AI"
    },
    {
      "name": "维京群岛 （英国）",
      "country_iso_code": "VG"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998376.md

---

## 添加商品产地信息

### 接口说明

将“产地”商品属性添加到方法中，如果该信息未指定。

### 接口标题

添加商品产地信息

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/product/country/set`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v2FbsPostingProductCountrySetRequest | 否 | 请求体。 |
| posting_number | body | string | 是 | 货运号。 |
| product_id | body | integer | 是 | 产品ID。 |
| country_iso_code | body | string | 是 | 根据标准ISO_3166-1添加的国家的两个字母代码<br>制造国家列表及其ISO代码可以使用该方法获得[/v2/posting/fbs/product/country/list](#operation/PostingAPI_ListCountryProductFbsPostingV2)。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| product_id | integer | 产品ID。 |
| is_gtd_needed | boolean | 有必要传送产品和货运的货物报关单（Cargo Customs Declaration）编号的标志。 |


#### 500 服务器错误

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | integer | - |
| details | protobufAny[] | - |
| details[] | protobufAny[] | - |
| details[].typeUrl | string | 数据传输协议类型。 |
| details[].value | string | 错误的值。 |
| message | string | - |


### 响应示例

```json
{
  "product_id": 180550365,
  "is_gtd_needed": true
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998377.md

---

## 打印标签

### 接口说明

生成带有指定货件标签的PDF文件。 在一个请求中最多可以传递20个ID。 如果至少有一个货件发生错误，则不会为请求中的所有货件准备标签。
我们建议在订单装配后45-60秒内询问标签。
错误 `The next postings aren't ready` 标识，未备好标签，请稍后重试。

### 接口标题

打印标签

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/package-label`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingPostingFBSPackageLabelRequest | 否 | 请求体。 |
| posting_number | body | string[] | 是 | 货运ID。 |
| posting_number[] | body | string[] | 否 | 货运ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| file_content | string | 二进制形式的文件内容。 |
| file_name | string | 文件名称。 |
| content_type | string | 文件类型。 |


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
    "content_type": "application/pdf",
    "file_name": "ticket-170660-2023-07-13T13:17:06Z.pdf",
    "file_content": "%PDF-1.7\n%âãÏÓ\n53 0 obj\n<</MarkInfo<</Marked true/Type/MarkInfo>>/Pages 9 0 R/StructTreeRoot 10 0 R/Type/Catalog>>\nendobj\n8 0 obj\n<</Filter/FlateDecode/Length 2888>>\nstream\nxå[[ݶ\u0011~?¿BÏ\u0005Bs\u001c^\u0000Àwí5ú\u0010 m\u0016Èsà¦)\n;hÒ\u0014èÏïG\u0014)<{äµ] ]?¬¬oIÎ}¤F±óϤñï\u001bÕü×X­´OÏï?^~¹$<ø¨È9q\u0013Y\u0012åñì§_¼|ÿégü\t+\u0012\u001bxª}Æxҿ¿¼_º¼xg¦þ5OkuÌ3ýíògüûå\"Ni\u0016C\u0001°\u000fA9g'r¢\"\u0013YóĪ\u0018NÑ{\u001dÕóZ¬\\Ô\""
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998381.md

---

## 货件装运

### 接口说明

将有争议的订单转到装运。货件状态将更改为 `awaiting_deliver`。

### 接口标题

货件装运

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/awaiting-delivery`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2MovePostingToAwaitingDeliveryRequest | 否 | 请求体。 |
| posting_number | body | string[] | 是 | 货运ID。一次请求中的最大数量——100。 |
| posting_number[] | body | string[] | 否 | 货运ID。一次请求中的最大数量——100。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 处理请求的结果。 如果请求执行时无误，则为“true”。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998382.md

---

## 货件取消原因

### 接口说明

返回所有货件取消原因列表。

### 接口标题

货件取消原因

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/cancel-reason/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | postingCancelReason[] | 方法操作结果。 |
| result[] | postingCancelReason[] | 方法操作结果。 |
| result[].id | integer | 取消原因ID。 |
| result[].is_available_for_cancellation | boolean | 取消装运结果。 `true`, 如果请求可以取消。 |
| result[].title | string | 类别名称。 |
| result[].type_id | string | 取消货件ID：<br>- `buyer` — 买家，<br>- `seller` — 卖家。 |


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
      "id": 352,
      "title": "在卖家仓库中已无商品",
      "type_id": "seller",
      "is_available_for_cancellation": true
    },
    {
      "id": 401,
      "title": "卖家拒绝了仲裁",
      "type_id": "seller",
      "is_available_for_cancellation": false
    },
    {
      "id": 402,
      "title": "其他（卖家的其他过错）",
      "type_id": "seller",
      "is_available_for_cancellation": true
    },
    {
      "id": 666,
      "title": "快递服务退货：在该区域没有快递",
      "type_id": "seller",
      "is_available_for_cancellation": false
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998383.md

---

## 货运取消原因

### 接口说明

返回特定货件的取消原因列表。

### 接口标题

货运取消原因

### 接口地址

`POST https://api-seller.ozon.ru/v1/posting/fbs/cancel-reason`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingCancelReasonRequest | 否 | 请求体。 |
| related_posting_numbers | body | string[] | 是 | 货件号。 |
| related_posting_numbers[] | body | string[] | 否 | 货件号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | relatedPostingCancelReason[] | 请求结果。 |
| result[] | relatedPostingCancelReason[] | 请求结果。 |
| result[].posting_number | string | 货运号。 |
| result[].reasons | relatedPostingCancelReasons[] | 取消订单原因。 |
| result[].reasons[] | relatedPostingCancelReasons[] | 取消订单原因。 |
| result[].reasons[].id | integer | 取消原因ID：<br>- `352` — 在卖家仓库已无商品。<br>- `400` — 只剩下残次品。<br>- `401` — 卖家拒绝了仲裁。<br>- `402` — 其他（卖家错误）。<br>- `665` — 买家没有收货。<br>- `666` — 快递服务退货：在该区域没有快递。<br>- `667` — 订单被快递弄丢。 |
| result[].reasons[].title | string | 描述取消原因。 |
| result[].reasons[].type_id | string | 取消货运提出方：<br>- `buyer` — 买家，<br>- `seller` — 卖家。 |


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
      "posting_number": "73837363-0010-3",
      "reasons": [
        {
          "id": 352,
          "title": "在卖家仓库中已无商品",
          "type_id": "seller"
        },
        {
          "id": 400,
          "title": "只剩下有缺陷的商品",
          "type_id": "seller"
        },
        {
          "id": 402,
          "title": "其他（卖家的其他过错）",
          "type_id": "seller"
        }
      ]
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998384.md

---

## 取消货运

### 接口说明

将装运状态改为 `cancelled`。
如果您使用 rFBS 模式, 可用以下取消原因ID — `cancel_reason_id`:
- `352` — 商品无库存；
- `400` — 只剩下有缺陷的商品。
- `401` — 仲裁取消；
- `402` — 其他原因；
- `665` — 买家没有收货；
- `666` — 在该地区没有快递；
- `667` — 订单被快递弄丢。
状态为“运输中”和“快递员派件中”的包裹可使用最后的4个理由。
无法取消可能送达的包裹。

### 接口标题

取消货运

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/cancel`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingCancelFbsPostingRequest | 否 | 请求体。 |
| cancel_reason_id | body | integer | 否 | 取消运输的原因ID。 |
| cancel_reason_message | body | string | 否 | 关于取消的附加信息。如果`cancel_reason_id = 402`，参数是必须的。 |
| posting_number | body | string | 否 | 货件ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 处理请求的结果。 如果请求执行时无误，则为“true”。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998385.md

---

## 为货件中的称重商品添加重量

### 接口说明

暂无接口说明。

### 接口标题

为货件中的称重商品添加重量

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/product/change`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingPostingProductChangeRequest | 否 | 请求体。 |
| items | body | PostingProductChangeRequestItem[] | 是 | 商品信息。 |
| items[] | body | PostingProductChangeRequestItem[] | 否 | 商品信息。 |
| items[].sku | body | integer | 是 | Ozon系统商品ID — SKU。 |
| items[].weightReal | body | number[] | 是 | 在货件中的商品单位重量。 |
| items[].weightReal[] | body | number[] | 否 | 在货件中的商品单位重量。 |
| posting_number | body | string | 是 | 货运ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | string | 货运ID。 |


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
  "result": "33920158-0006-1"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998386.md

---

## 取消某些商品发货

### 接口说明

如果您无法从货件中发送部分产品，请使用该方法。
为了在使用FBS或rFBS模式时获取取消原因的标识符`cancel_reason_id`，请使用方法[/v2/posting/fbs/cancel-reason/list](#operation/PostingAPI_GetPostingFbsCancelReasonList)。
无法取消可能送达的包裹。

### 接口标题

取消某些商品发货

### 接口地址

`POST https://api-seller.ozon.ru/v2/posting/fbs/product/cancel`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | postingPostingProductCancelRequest | 否 | 请求体。 |
| cancel_reason_id | body | integer | 是 | 货物取消发货原因ID。 |
| cancel_reason_message | body | string | 是 | 必填字段。关于取消的其他信息。 |
| items | body | PostingProductCancelRequestItem[] | 是 | 商品信息。 |
| items[] | body | PostingProductCancelRequestItem[] | 否 | 商品信息。 |
| items[].quantity | body | integer | 是 | 货运商品数量。 |
| items[].sku | body | integer | 是 | Ozon系统中的商品ID — SKU。 |
| posting_number | body | string | 是 | 货运ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | string | 货运号。 |


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
  "result": ""
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998387.md

---
