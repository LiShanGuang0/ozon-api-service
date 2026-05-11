# ReturnsAPI

接口数量：1

## 接口列表

- [FBO和FBS退货信息](#fbo和fbs退货信息) - `POST /v1/returns/list`

## FBO和FBS退货信息

### 接口说明

用于获取 FBO 和 FBS 退货信息的方法。

### 接口标题

FBO和FBS退货信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/returns/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetReturnsListRequest | 否 | 请求体。 |
| filter | body | GetReturnsListRequestFilter | 否 | - |
| filter.logistic_return_date | body | v1TimeRange_return_date | 否 | - |
| filter.logistic_return_date.time_from | body | string | 否 | 开始日期。 |
| filter.logistic_return_date.time_to | body | string | 否 | 结束日期。 |
| filter.storage_tariffication_start_date | body | v1TimeRange_storage_tariffication | 否 | - |
| filter.storage_tariffication_start_date.time_from | body | string | 否 | 开始日期。 |
| filter.storage_tariffication_start_date.time_to | body | string | 否 | 结束日期。 |
| filter.visual_status_change_moment | body | v1TimeRange_visual_status | 否 | - |
| filter.visual_status_change_moment.time_from | body | string | 否 | 开始日期。 |
| filter.visual_status_change_moment.time_to | body | string | 否 | 结束日期。 |
| filter.order_id | body | integer | 否 | 根据订单ID筛选。 |
| filter.posting_numbers | body | string[] | 否 | 根据货件编号筛选。请勿传递超过 50 个货盒单号。 |
| filter.posting_numbers[] | body | string[] | 否 | 根据货件编号筛选。请勿传递超过 50 个货盒单号。 |
| filter.product_name | body | string | 否 | 根据商品名称筛选。 |
| filter.offer_id | body | string | 否 | 根据商品货号筛选。 |
| filter.visual_status_name | body | string | 否 | 根据退货状态筛选：<br>- `DisputeOpened` — 与买家有争议；<br>- `OnSellerApproval` — 等待卖家批准；<br>- `ArrivedAtReturnPlace` — 到达取货点；<br>- `OnSellerClarification` — 等待卖家确认；<br>- `OnSellerClarificationAfterPartialCompensation` — 部分补偿后等待卖家确认；<br>- `OfferedPartialCompensation` — 提供部分补偿；<br>- `ReturnMoneyApproved` — 退货款项已批准；<br>- `PartialCompensationReturned` — 部分款项已退还；<br>- `CancelledDisputeNotOpen` — 退货被拒绝，争议未开启；<br>- `Rejected` — 申请被拒绝；<br>- `CrmRejected` — Ozon拒绝申请；<br>- `Cancelled` — 申请已取消；<br>- `Approved` — 卖家批准了申请；<br>- `ApprovedByOzon` — Ozon批准了申请；<br>- `ReceivedBySeller` —卖家已收到退货；<br>- `MovingToSeller` — 退货正在运往卖家；<br>- `ReturnCompensated` —卖家已获得补偿；<br>- `ReturningToSellerByCourier` — 快递员正在将退货送回卖家；<br>- `Utilizing` — 正在销毁中；<br>- `Utilized` — 已销毁；<br>- `MoneyReturned` — 已退还全款给买家；<br>- `PartialCompensationInProcess` — 部分退款已批准；<br>- `DisputeYouOpened` — 卖家提出争议；<br>- `CompensationRejected` — 补偿被拒绝；<br>- `DisputeOpening` — 已向客服发送请求；<br>- `CompensationOffered` — 等待您对补偿的决定；<br>- `WaitingCompensation` —等待补偿；<br>- `SendingError` — 发送客服请求时发生错误；<br>- `CompensationRejectedBySla` — 补偿请求过期；<br>- `CompensationRejectedBySeller` — 卖家拒绝补偿；<br>- `MovingToOzon` — 正在运往Ozon仓库；<br>- `ReturnedToOzon` — 已返回Ozon仓库；<br>- `MoneyReturnedBySystem` — 快速退款；<br>- `WaitingShipment` — 等待发货。 |
| filter.warehouse_id | body | integer | 否 | 根据仓库ID筛选。可以使用方法 [/v1/warehouse/list](#operation/WarehouseAPI_WarehouseList)获取。 |
| filter.barcode | body | string | 否 | 根据退货标签条形码筛选。 |
| filter.return_schema | body | string | 否 | 根据配送方案筛选：`FBS` 或`FBO`。 |
| limit | body | integer | 是 | 加载的退货数量。 |
| last_id | body | integer | 否 | 最后加载的退货ID。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| returns | GetReturnsListResponseReturnsItem[] | 退货信息。 |
| returns[] | GetReturnsListResponseReturnsItem[] | 退货信息。 |
| returns[].exemplars | GetReturnsListResponseExemplar[] | 退货实例信息。 |
| returns[].exemplars[] | GetReturnsListResponseExemplar[] | 退货实例信息。 |
| returns[].exemplars[].id | integer | 实例ID。 |
| returns[].id | integer | 退货ID。 |
| returns[].company_id | integer | 卖家ID。 |
| returns[].return_reason_name | string | 退货或取消的原因。 |
| returns[].type | string | 退货类型：<br>`Cancellation` - 取消订单（交货前）；<br>`FullReturn` - 完全拒收（交货时）；<br>`PartialReturn` - 部分拒收（交货时）；<br>`ClientReturn` - 客户退货（交货后）；<br>`Unknown` - 技术退货。 |
| returns[].schema | string | 退货方案：<br>`FBS`；<br>`FBO`。 |
| returns[].order_id | integer | 订单ID。 |
| returns[].order_number | string | 订单编号。 |
| returns[].place | GetReturnsListResponsePlace_now | - |
| returns[].place.id | integer | 仓库ID。 |
| returns[].place.name | string | 名称。 |
| returns[].place.address | string | 地址。 |
| returns[].target_place | GetReturnsListResponsePlace_target | - |
| returns[].target_place.id | integer | 仓库ID。 |
| returns[].target_place.name | string | 名称。 |
| returns[].target_place.address | string | 地址。 |
| returns[].storage | GetReturnsListResponseStorage | - |
| returns[].storage.sum | seller_returnsv1Money_storage | - |
| returns[].storage.sum.currency_code | string | 货币。 |
| returns[].storage.sum.price | number | 存储费用。 |
| returns[].storage.tariffication_first_date | string | 计算存储费用的第一天。 |
| returns[].storage.tariffication_start_date | string | 计算存储费用的开始日期。 |
| returns[].storage.arrived_moment | string | 退货准备交付给卖家的日期。 |
| returns[].storage.days | integer | 退货等待交付给卖家的天数。 |
| returns[].storage.utilization_sum | seller_returnsv1Money_utilization | - |
| returns[].storage.utilization_sum.currency_code | string | 货币。 |
| returns[].storage.utilization_sum.price | number | 销毁费用。 |
| returns[].storage.utilization_forecast_date | string | 预计销毁日期。 |
| returns[].product | GetReturnsListResponseProduct | - |
| returns[].product.sku | integer | 商品在Ozon系统中的ID（SKU）。 |
| returns[].product.offer_id | string | 卖家系统中的商品标识符是商品货号。 |
| returns[].product.name | string | 商品名称。 |
| returns[].product.price | seller_returnsv1Money_product | - |
| returns[].product.price.currency_code | string | 货币。 |
| returns[].product.price.price | number | 商品价格。 |
| returns[].product.price_without_commission | seller_returnsv1Money_without_commission | - |
| returns[].product.price_without_commission.currency_code | string | 货币。 |
| returns[].product.price_without_commission.price | number | 不含佣金的商品价格。 |
| returns[].product.commission_percent | number | 佣金比例。 |
| returns[].product.commission | seller_returnsv1Money_commission | - |
| returns[].product.commission.currency_code | string | 货币。 |
| returns[].product.commission.price | number | 佣金费用。 |
| returns[].product.quantity | integer | 产品数量。 |
| returns[].logistic | GetReturnsListResponseLogistic | - |
| returns[].logistic.technical_return_moment | string | 商品被标记为技术退货的日期。 |
| returns[].logistic.final_moment | string | 退货到达履约中心或卖家收到退货的日期。 |
| returns[].logistic.cancelled_with_compensation_moment | string | 向卖家补偿退货的日期。 |
| returns[].logistic.return_date | string | 买家退货的日期。 |
| returns[].logistic.barcode | string | 退货标签的条形码。 |
| returns[].visual | GetReturnsListResponseVisual | - |
| returns[].visual.status | GetReturnsListResponseVisualStatus | - |
| returns[].visual.status.id | integer | 退货状态ID。 |
| returns[].visual.status.display_name | string | 退货状态名称。 |
| returns[].visual.status.sys_name | string | 退货状态的系统名称。 |
| returns[].visual.change_moment | string | 退货状态的变更日期。 |
| returns[].additional_info | GetReturnsListResponseAdditionalInfo | - |
| returns[].additional_info.is_opened | boolean | 如果退货已开封，显示`true`。 |
| returns[].additional_info.is_super_econom | boolean | 如果退货为"超级经济"商品，显示`true`。 |
| returns[].source_id | integer | 先前的退货ID。 |
| returns[].posting_number | string | 货件编号。 |
| returns[].clearing_id | integer | 初始货件条形码。 |
| returns[].return_clearing_id | integer | 初始货件的退货条形码。 |
| has_next | boolean | 如果卖家有其他退货，显示`true`。 |


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
  "returns": [
    {
      "exemplars": [
        {
          "id": "1019562967545956"
        }
      ],
      "id": "1000015552",
      "company_id": "3058",
      "return_reason_name": "买家拒绝取货：对商品质量不满意",
      "type": "FullReturn",
      "schema": "Fbs",
      "order_id": "24540784250",
      "order_number": "58544282-0057",
      "place": {
        "id": "23869688194000",
        "name": "СЦ_Львовский_Возвраты",
        "address": "Россия, обл. Московская, г. Подольск, промышленная зона Львовский, ул. Московская, д. 69, стр. 5"
      },
      "target_place": {
        "id": "23869688194000",
        "name": "СЦ_Львовский_Возвраты",
        "address": "Россия, обл. Московская, г. Подольск, промышленная зона Львовский, ул. Московская, д. 69, стр. 5"
      },
      "storage": {
        "sum": {
          "currency_code": "RUB",
          "price": "1231"
        },
        "tariffication_first_date": "2024-07-30T06:15:48.998146Z",
        "tariffication_start_date": "2024-07-29T06:15:48.998146Z",
        "arrived_moment": "2024-07-29T06:15:48.998146Z",
        "days": "0",
        "utilization_sum": {
          "currency_code": "RUB",
          "price": "1231"
        },
        "utilization_forecast_date": "2024-07-29T06:15:48.998146Z"
      },
      "product": {
        "sku": "1100526203",
        "offer_id": "81451",
        "name": "Кукла Дотти Плачущий младенец Cry Babies Dressy Dotty",
        "price": {
          "currency_code": "RUB",
          "price": "3318"
        },
        "price_without_commission": {
          "currency_code": "RUB",
          "price": "3318"
        },
        "commission_percent": "1.2",
        "commission": {
          "currency_code": "RUB",
          "price": "2312"
        }
      },
      "logistic": {
        "technical_return_moment": "2024-07-29T06:15:48.998146Z",
        "final_moment": "2024-07-29T06:15:48.998146Z",
        "cancelled_with_compensation_moment": "2024-07-29T06:15:48.998146Z",
        "return_date": "2024-07-29T06:15:48.998146Z",
        "barcode": "ii5275210303"
      },
      "visual": {
        "status": {
          "id": 3,
          "display_name": "在取货点",
          "sys_name": "ArrivedAtReturnPlace"
        },
        "change_moment": "2024-07-29T06:15:48.998146Z"
      },
      "additional_info": {
        "is_opened": true,
        "is_super_econom": false
      },
      "source_id": "90426223",
      "posting_number": "58544282-0057-1",
      "clearing_id": "21190893156000",
      "return_clearing_id": null
    }
  ],
  "has_next": false
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863058.md

---
