# ProductAPI

接口数量：20

## 接口列表

- [创建或更新商品](#创建或更新商品) - `POST /v3/product/import`
- [查询商品添加或更新状态](#查询商品添加或更新状态) - `POST /v1/product/import/info`
- [通过SKU创建商品](#通过sku创建商品) - `POST /v1/product/import-by-sku`
- [更新商品特征](#更新商品特征) - `POST /v1/product/attributes/update`
- [上传或更新商品图片](#上传或更新商品图片) - `POST /v1/product/pictures/import`
- [品列表的](#品列表的) - `POST /v3/product/list`
- [按SKU获得商品的内容排名](#按sku获得商品的内容排名) - `POST /v1/product/rating-by-sku`
- [根据标识符获取商品信息](#根据标识符获取商品信息) - `POST /v3/product/info/list`
- [获取商品特征描述](#获取商品特征描述) - `POST /v3/products/info/attributes`
- [获取商品详细信息](#获取商品详细信息) - `POST /v1/product/info/description`
- [品类限制、商品的创建和更新](#品类限制、商品的创建和更新) - `POST /v4/product/info/limit`
- [从卖家的系统中改变商品货号](#从卖家的系统中改变商品货号) - `POST /v1/product/update/offer-id`
- [将商品归档](#将商品归档) - `POST /v1/product/archive`
- [从档案中还原商品](#从档案中还原商品) - `POST /v1/product/unarchive`
- [从存档删除没有SKU的商品](#从存档删除没有sku的商品) - `POST /v2/products/delete`
- [上传服务和数字商品的激活码](#上传服务和数字商品的激活码) - `POST /v1/product/upload_digital_codes`
- [激活码上传状态](#激活码上传状态) - `POST /v1/product/upload_digital_codes/info`
- [订阅该商品的用户数](#订阅该商品的用户数) - `POST /v1/product/info/subscription`
- [获取相关SKU](#获取相关sku) - `POST /v1/product/related-sku/get`
- [获取商品图片](#获取商品图片) - `POST /v2/product/pictures/info`

## 创建或更新商品

### 接口说明

如果您按照FBP工作模式从中国或香港销售，那么请为每件商品生成条形码。合作伙伴仓库将无法接收没有条形码的商品。
创建商品并更新有关商品信息的方法。
欲知限制，请使用
[/v4/product/info/limit](#operation/ProductAPI_GetUploadQuota)。 如果商品下载和更新次数
超过限制，则出现错误 `item_limit_exceeded`。
一次请求最多可转移100种商品。 每个商品都是数组中的单独元素 `items`。 请指出
有关商品的所有信息：特征、条形码、图像、尺寸、价格和价格货币。
在更新商品时，请在请求中转达有关商品的所有信息。
指定货币必须与个人中心中设置的币种相匹配。 默认情况下显示 `RUB` — 俄罗斯卢布。
如果您设置了人民币为币种, 请选择 `CNY`, 否则将返回错误。
如果您填写错误或指定，则不会创建或更新商品:
- **强制特征**: 不同类目的属性有所不同——您可以在 [卖家知识库](https://docs.ozon.ru/global/zh-hans/products/requirements/product-info/product-characteristics/#在哪里指定必要商品特性) 中查看，或者通过方法 [/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes)获取。
- **真实体积和重量特性**: `depth`, `width`, `height`, `dimension_unit`, `weight`, `weight_unit`。请勿在请求中跳过这些参数，也不要指定0。
HTML标签可用于某些特征。
[更多关于特征的信息可见卖家知识库](https://docs.ozon.ru/global/zh-hans/products/requirements/product-info/product-characteristics/)
审核后，该商品将出现在您的个人中心中，但在您将其出售之前，用户将无法看到该商品。
请求中的每项都是数组的单独元素 `items`。
为连接两张卡片, 请对每张卡片传递`9048` 在 `attributes`中。 这些卡片除了大小或颜色外的所有属性都必须匹配。
加载图片
若要上传，请将请求中的图像链接发至公共云存储中。
链接的图像格式为JPG或PNG。
按照网站上所需的顺序将图像放在`images` 数组中。 要加载主图请使用 `primary_image`参数。 如果没有传递 `primary_image`值, 主图将是
在 `images`组中的第一张图片。
对于每个商品，您最多可以上传15个图像，包括主图像。
如果传递 `primary_image`值, 在 `images` 的最大图像数为——14。
如果参数 `primary_image` 为空, 那么在`images` 可以传递最多15张图片。
若要上传招聘360，请使用`images360`字段, 上传营销名字 — `color_image`。
如果要更改图像的构图或顺序，请使用
[/v3/product/info/list](#operation/ProductAPI_GetProductInfoList)
方法获取信息 —— 里面显示当前订单和
图像组成。 请复制 `images`, `images360`, `color_image`字段的数据, 更改和完成列表或者
根据需求订购。
上传视频
上传视频请在请求中上传视频链接。
为此，请在 `complex_attributes`参数中传递对象。在`attributes`数组中，请传递两个含`complex_id = 100001`的对象:
- 在第一个中，请赋值指定 `id = 21841` 和在数组 `values` 中传输含视频链接的对象。
__例子__:
```
{
"complex_id": 100001,
"id": 21841,
"values": [
{
"value": "https://www.youtube.com/watch?v=ZwM0iBn03dY"
}
]
}
```
- 在二个中，请指定值`id = 21837` 和在 `values` 数组中传输含视频名称的对象。
__例子__:
```
{
"complex_id": 100001,
"id": 21837,
"values": [
{
"value": "videoName_1"
}
]
}
```
如果您想上传视频, 请在不同的`values`数组对象中为每个视频赋值。
__例子__:
```
{
"complex_id": 100001,
"id": 21837,
"values": [
{
"value": "videoName_1"
},
{
"value": "videoName_2"
}
]
},
{
"complex_id": 100001,
"id": 21841,
"values": [
{
"value": "https://www.youtube.com/watch?v=ZwM0iBn03dY"
},
{
"value": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
]
}
```
上传尺寸表
为添加使用以下方法创建的尺寸图表 [设计](https://table-constructor.ozon.ru/visual-editor), 请在`attributes`组传递表格，格式 JSON 如 Rich-内容 `id = 13164`。
[JSON格式的设计](https://table-constructor.ozon.ru/schema.json)
[更多关于设计可见卖家知识库](https://docs.ozon.ru/global/zh-hans/products/upload/adding-content/size-table-constructor/)
视频封面上传
您可以通过综合属性上传视频封面 `complex_attributes`。
__例子__：
```
"complex_attributes": [
{
"attributes": [
{
"id": 21845,
"complex_id": 100002,
"values": [
{
"dictionary_value_id": 0,
"value": "https://v.ozone.ru/vod/video-10/01GFATWQVCDE7G5B721421P1231Q7/asset_1.mp4"
}
]
}
]
}
]
```

### 接口标题

创建或更新商品

### 接口地址

`POST https://api-seller.ozon.ru/v3/product/import`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v3ImportProductsRequest | 否 | 请求体。 |
| items | body | v3ImportProductsRequestItem[] | 否 | 数据组。 |
| items[] | body | v3ImportProductsRequestItem[] | 否 | 数据组。 |
| items[].attributes | body | v3ImportProductsRequestAttribute[] | 是 | 商品特性组。 不同类别的特征不同 — 其可见 [卖家知识库](https://docs.ozon.ru/global/zh-hans/) 或通过 [API](https://docs.ozon.ru/api/seller/zh/)。 |
| items[].attributes[] | body | v3ImportProductsRequestAttribute[] | 否 | 商品特性组。 不同类别的特征不同 — 其可见 [卖家知识库](https://docs.ozon.ru/global/zh-hans/) 或通过 [API](https://docs.ozon.ru/api/seller/zh/)。 |
| items[].attributes[].complex_id | body | integer | 否 | 支持嵌套属性的特征ID。 例如，"处理器"特征具有嵌套特征"制造商"，"L2缓存"等。 每个嵌套特征都可以具有多值变体。 |
| items[].attributes[].id | body | integer | 否 | 特征ID。 |
| items[].attributes[].values | body | v3ImportProductsRequestDictionaryValue[] | 否 | 嵌套特征值的数组。 |
| items[].attributes[].values[] | body | v3ImportProductsRequestDictionaryValue[] | 否 | 嵌套特征值的数组。 |
| items[].barcode | body | string | 否 | 商品条码。 |
| items[].description_category_id | body | integer | 是 | 类别ID。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |
| items[].new_description_category_id | body | integer | 否 | 新的类目标识符。如果需要更改当前商品类目，请填写该标识符。 |
| items[].color_image | body | string | 否 | 营销色彩。<br>格式：公共云存储中图像链接的URL。 链接的图像格式为JPG。 |
| items[].complex_attributes | body | v3ImportProductsRequestComplexAttribute[] | 否 | 具有嵌套属性的特征组。 |
| items[].complex_attributes[] | body | v3ImportProductsRequestComplexAttribute[] | 否 | 具有嵌套属性的特征组。 |
| items[].complex_attributes[].attributes | body | v3ImportProductsRequestAttribute[] | 否 | 商品特性组。不同类别的特征不同 — 可见 [卖家知识库](https://docs.ozon.ru/global/zh-hans/) 或通过 [API](https://docs.ozon.ru/api/seller/zh/)。 |
| items[].complex_attributes[].attributes[] | body | v3ImportProductsRequestAttribute[] | 否 | 商品特性组。不同类别的特征不同 — 可见 [卖家知识库](https://docs.ozon.ru/global/zh-hans/) 或通过 [API](https://docs.ozon.ru/api/seller/zh/)。 |
| items[].currency_code | body | string | 否 | 价格显示的货币。 传输值必须与个人中心设置中所设置的货币相匹配。 默认情况下，显示`RUB` — 俄罗斯卢布。<br>例如，如果您设人民币为结算货币，请赋值`CNY`，否则将返回错误。<br>可能的值：<br>- `RUB` — 俄罗斯卢布,<br>- `BYN` — 白俄罗斯卢布,<br>- `KZT` — 坚戈,<br>- `EUR` — 欧元,<br>- `USD` — 美元,<br>- `CNY` — 元。 |
| items[].depth | body | integer | 是 | 包装厚度。 |
| items[].dimension_unit | body | string | 是 | 尺寸测量单位:<br>- `mm` — 毫米,<br>- `cm` — 厘米,<br>- `in` — 英寸。 |
| items[].geo_names | body | string[] | 否 | 地理限制 —— 如有必要，请在个人中心中创建或编辑商品时填写该参数。<br>该参数为可选项。 |
| items[].geo_names[] | body | string[] | 否 | 地理限制 —— 如有必要，请在个人中心中创建或编辑商品时填写该参数。<br>该参数为可选项。 |
| items[].height | body | integer | 是 | 包装高度。 |
| items[].images | body | string[] | 是 | 图像组。 最多15件。 图像以与组中相同的顺序显示在网站上。<br>如果不传递值 `primary_image`, 组中的第一个图像将是商品的主图。<br>如果您传递了值 `primary_image`，则最多传递14个图像。<br>如果 `primary_image` 参数为空，则最多传递15个图像。<br>格式：公共云存储中图像链接的URL。 链接的图像格式为JPG或PNG。 |
| items[].images[] | body | string[] | 否 | 图像组。 最多15件。 图像以与组中相同的顺序显示在网站上。<br>如果不传递值 `primary_image`, 组中的第一个图像将是商品的主图。<br>如果您传递了值 `primary_image`，则最多传递14个图像。<br>如果 `primary_image` 参数为空，则最多传递15个图像。<br>格式：公共云存储中图像链接的URL。 链接的图像格式为JPG或PNG。 |
| items[].primary_image | body | string | 否 | 链接到商品主图。 |
| items[].promotions | body | ImportProductRequestPromotion[] | 否 | 促销活动。 |
| items[].promotions[] | body | ImportProductRequestPromotion[] | 否 | 促销活动。 |
| items[].promotions[].operation | body | enum(UNKNOWN, ENABLE, DISABLE) | 否 | 促销活动操作属性：<br>- `ENABLE` — 启用，<br>- `DISABLE` — 禁用，<br>- `UNKNOWN` — 保持默认，不做修改。 |
| items[].promotions[].type | body | enum(REVIEWS_PROMO) | 否 | 促销活动类型：<br>- `REVIEWS_PROMO` — “评价积分”促销活动。 |
| items[].service_type | body | v2ServiceType | 否 | - |
| items[].images360 | body | string[] | 否 | 图像组360。至70件。<br>格式：公共云存储中图像链接的URL。 链接的图像格式为JPG。 |
| items[].images360[] | body | string[] | 否 | 图像组360。至70件。<br>格式：公共云存储中图像链接的URL。 链接的图像格式为JPG。 |
| items[].name | body | string | 是 | 商品名称。 至500字符。 |
| items[].offer_id | body | string | 是 | 卖方系统中的商品ID — 货号。至50字符。 |
| items[].old_price | body | string | 否 | 折扣前的价格（将在产品卡上划掉）。 以卢布表示。分数分隔<br>符号 — 点, 在点之后最多两个字符。<br>如果您之前传递了 `old_price`, 那么在更新 `price` 时也请更新 `old_price`。 |
| items[].pdf_list | body | ImportProductsRequestPdfList[] | 否 | PDF-文件清单。 |
| items[].pdf_list[] | body | ImportProductsRequestPdfList[] | 否 | PDF-文件清单。 |
| items[].pdf_list[].index | body | integer | 否 | 存储库中的文档索引，用于设置顺序。 |
| items[].pdf_list[].name | body | string | 否 | 文件名称。 |
| items[].pdf_list[].src_url | body | string | 否 | 文件地址。 |
| items[].price | body | string | 是 | 商品价格，包括折扣，显示在商品卡上。 如果商品没有折扣，请指定<br>此参数中 `old_price` 的值。 |
| items[].type_id | body | integer | 是 | 商品类型的标识符。<br>可以通过方法[/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)的响应参数 `type_id` 获取对应的值。<br>填写此参数时，可以不在 `attibutes` 中指定参数 `id:8229` 的属性，`type_id` 将优先使用。 |
| items[].vat | body | string | 是 | 商品增值税税率：<br>- `0` — 免除增值税,<br>- `0.05` — 5%,<br>- `0.07` — 7%,<br>- `0.1` — 10%,<br>- `0.2` — 20%。<br>传递当前有效的出价值。 |
| items[].weight | body | integer | 是 | 含包装的商品重量。 限值为1000公斤或其他换算值<br>计量单位。 |
| items[].weight_unit | body | string | 是 | 测重单位：<br>- `g` — 克,<br>- `kg` — 公斤,<br>- `lb` — 磅。 |
| items[].width | body | integer | 是 | 包装宽度。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v3ImportProductsResponseResult | - |
| result.task_id | integer | 装卸任务的编号。 |


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
    "task_id": 172549793
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863046.md

---

## 查询商品添加或更新状态

### 接口说明

允许获取商品卡片创建或更新的状态。

### 接口标题

查询商品添加或更新状态

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/import/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productGetImportProductsInfoRequest | 否 | 请求体。 |
| task_id | body | integer | 是 | 进口商品的任务代码。按照运输方式筛选。可以使用方法 [/v3/product/import](#operation/ProductAPI_ImportProductsV3)获取。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productGetImportProductsInfoResponseResult | - |
| result.items | GetImportProductsInfoResponseResultItem[] | 商品有关信息。 |
| result.items[] | GetImportProductsInfoResponseResultItem[] | 商品有关信息。 |
| result.items[].offer_id | string | 在卖方系统中的商品ID是货号。字段数值中行的最大长度为50个字符。 |
| result.items[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result.items[].status | string | 商品创建或更新状态。 商品信息在队列中处理。<br>可能的参数值:<br>- `pending` — 商品等待排队处理;<br>- `imported` — 商品已成功加载；<br>- `failed` — 商品加载错误；<br>- `skipped` — 商品未更新，因为请求未包含任何更改。 |
| result.items[].errors | v1ItemError[] | 错误数组。 |
| result.items[].errors[] | v1ItemError[] | 错误数组。 |
| result.total | integer | 在卖方系统中的卖家系统中的商品标识符 — `product_id`。 |


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
    "items": [
      {
        "offer_id": "143210608",
        "product_id": 137285792,
        "status": "imported",
        "errors": []
      }
    ],
    "total": 1
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998314.md

---

## 通过SKU创建商品

### 接口说明

该方法会创建指定SKU的商品卡片副本。
如果卖家[禁止复制](https://docs.ozon.ru/global/zh-hans/products/upload/upload-types/copying/?country=CN)，
将无法创建卡片副本。
无法通过SKU更新商品。

### 接口标题

通过SKU创建商品

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/import-by-sku`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productImportProductsBySKURequest | 否 | 请求体。 |
| items | body | productImportProductsBySKURequestItem[] | 否 | 商品信息。 |
| items[] | body | productImportProductsBySKURequestItem[] | 否 | 商品信息。 |
| items[].name | body | string | 否 | 商品名称。 小于500字符。 |
| items[].offer_id | body | string | 否 | 在卖家系统中的商品ID — 货号。至50字符。 |
| items[].old_price | body | string | 否 | 折扣前的价格（将在商品卡片上划掉）。 以卢布表示。 小数点分隔符是一个点，在点之后最多两个字符。 |
| items[].price | body | string | 否 | 含折扣的商品价格显示在商品卡片上。 如果商品没有折扣，请在此参数中指定值`old_price`。 |
| items[].sku | body | integer | 是 | 在Ozon系统中的商品ID — SKU。 |
| items[].vat | body | string | 否 | 商品增值税税率：<br>- `0` — 免除增值税,<br>- `0.05` — 5%,<br>- `0.07` — 7%,<br>- `0.1` — 10%,<br>- `0.2` — 20%。<br>传递当前有效的出价值。 |
| items[].currency_code | body | string | 否 | 价格显示的货币。 传输值必须与个人中心设置中所设置的货币相匹配。 默认情况下，显示`RUB` — 俄罗斯卢布。<br>例如，如果您设人民币为结算货币，请赋值`CNY`，否则将返回错误。<br>可能的值：<br>- `RUB` — 俄罗斯卢布,<br>- `BYN` — 白俄罗斯卢布,<br>- `KZT` — 坚戈,<br>- `EUR` — 欧元,<br>- `USD` — 美元,<br>- `CNY` — 元。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productImportProductsBySKUResponseResult | - |
| result.task_id | integer | 进口货物任务代码。 |
| result.unmatched_sku_list | integer[] | 商品Id列表。 |
| result.unmatched_sku_list[] | integer[] | 商品Id列表。 |


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
    "task_id": 176594213,
    "unmatched_sku_list": []
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998315.md

---

## 更新商品特征

### 接口说明

暂无接口说明。

### 接口标题

更新商品特征

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/attributes/update`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductUpdateAttributesRequest | 否 | 请求体。 |
| items | body | v1ProductUpdateAttributesRequestItem[] | 否 | 需要更新的商品和特征。 |
| items[] | body | v1ProductUpdateAttributesRequestItem[] | 否 | 需要更新的商品和特征。 |
| items[].attributes | body | v1ProductUpdateAttributesRequestAttribute[] | 否 | 商品特征。 |
| items[].attributes[] | body | v1ProductUpdateAttributesRequestAttribute[] | 否 | 商品特征。 |
| items[].attributes[].complex_id | body | integer | 否 | 支持嵌套属性的特征ID。 每个嵌套特征都可以有多个版本的值。 |
| items[].attributes[].id | body | integer | 否 | 特征ID。 |
| items[].attributes[].values | body | v1ProductUpdateAttributesRequestValue[] | 否 | 一组嵌套的特征值。 |
| items[].attributes[].values[] | body | v1ProductUpdateAttributesRequestValue[] | 否 | 一组嵌套的特征值。 |
| items[].offer_id | body | string | 是 | 卖家系统中的商品标识符是商品货号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| task_id | integer | 商品更新任务号码。<br>为检查更新状态，请将接收到的值传至方法 [/v1/product/import/info](#operation/ProductAPI_GetImportProductsInfo)。 |


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
  "task_id": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998316.md

---

## 上传或更新商品图片

### 接口说明

上传或更新商品图像的方法。
每次调用该方法时，要传递所有应该出现在商品详情页上的图片。例如，如果您调用该方法并上传了10张图片，然后再次调用该方法并上传了另一张。
那么之前的10账都将被删除。
要上传，请将图像的链接地址传到公共云存储。
链接图片的格式是JPG或PNG。
根据网站上所需的顺序排列`images`阵列中的图片。主要是阵列中的第一幅图像。
您可以为每个商品上传多达15张图片。
使用字段`images360`来上传360张图片，使用`color_image`来上传市场营销色彩。
如果您想改变图像的组成或顺序，请使用
[/v3/product/info/list](#operation/ProductAPI_GetProductInfoList)
方法获取信息 —— 它显示了当前图像的顺序和组成。
从 `images`, `images360`, `color_image`,字段中复制数据，根据需要改变和完成组成或顺序。

### 接口标题

上传或更新商品图片

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/pictures/import`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productv1ProductImportPicturesRequest | 否 | 请求体。 |
| color_image | body | string | 否 | 市场营销色彩。 |
| images | body | string[] | 否 | 数组图片链接。<br>数组中的图像是按照它们在网站上出现的顺序排列的。<br>数组中的第一个图像将是主图像。 |
| images[] | body | string[] | 否 | 数组图片链接。<br>数组中的图像是按照它们在网站上出现的顺序排列的。<br>数组中的第一个图像将是主图像。 |
| images360 | body | string[] | 否 | 360图片的数组。多达70张图片。<br>格式：公共云存储中的图像链接地址。链接图片的格式是JPG。 |
| images360[] | body | string[] | 否 | 360图片的数组。多达70张图片。<br>格式：公共云存储中的图像链接地址。链接图片的格式是JPG。 |
| product_id | body | integer | 是 | 卖家系统中的商品标识符 — `product_id`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productv1ProductInfoPicturesResponseResult | - |
| result.pictures | productProductInfoPicturesResponsePicture[] | - |
| result.pictures[] | productProductInfoPicturesResponsePicture[] | - |
| result.pictures[].is_360 | boolean | 表示该图片是一个360图像。 |
| result.pictures[].is_color | boolean | 表示图片是样品颜色。 |
| result.pictures[].is_primary | boolean | 表示该图片是主图像。 |
| result.pictures[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| result.pictures[].state | string | 图片上传状态。<br>如果方法[/v1/product/pictures/import](#operation/ProductAPI_ProductImportPictures)被使用，方法的响应将总是`imported` —— 图像未被处理。<br>要查看最终状态，请在大约10秒后使用[/v1/product/pictures/info]（#operation/ProductAPI_ProductInfoPictures）方法。<br>如果你使用方法[/v1/product/pictures/info](#operation/ProductAPI_ProductInfoPictures)，你会看到其中一个状态。<br>- `uploaded` —— 上传的图像；<br>- `pending` ——  图片上传失败，请稍后重试。 |
| result.pictures[].url | string | 公共云存储中的图像的链接地址。链接图片的格式是JPG或PNG。 |


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
  "result": {
    "pictures": [
      {
        "is_360": null,
        "is_color": null,
        "is_primary": null,
        "product_id": null,
        "state": null,
        "url": null
      }
    ]
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998317.md

---

## 品列表的

### 接口说明

用于获取所有商品列表的方法。
如果使用 `offer_id` 或 `product_id` 进行筛选，则无需填写其他参数。
每次请求只能使用一组标识符，且商品数量不能超过 1000 个。
如果不使用标识符进行查询，则需在后续请求中指定 `limit` 和 `last_id`。

### 接口标题

品列表的

### 接口地址

`POST https://api-seller.ozon.ru/v3/product/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productv3GetProductListRequest | 否 | 请求体。 |
| filter | body | productv3GetProductListRequestFilter | 否 | - |
| filter.offer_id | body | string[] | 否 | 基于参数 `offer_id` 的过滤。 可以提交数值列表。 |
| filter.offer_id[] | body | string[] | 否 | 基于参数 `offer_id` 的过滤。 可以提交数值列表。 |
| filter.product_id | body | string[] | 否 | 基于参数 `product_id` 的过滤。 可以提交数值列表。 |
| filter.product_id[] | body | string[] | 否 | 基于参数 `product_id` 的过滤。 可以提交数值列表。 |
| filter.visibility | body | productv3GetProductListRequestFilterFilterVisibility | 否 | - |
| last_id | body | string | 否 | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。<br>要检索以下数值，请从上一个查询的响应中指定 `last_id`。 |
| limit | body | integer | 否 | 答复的信息数量。默认设置为1。最大值是1000。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productv3GetProductListResponseResult | - |
| result.items | productv3GetProductListResponseItem[] | 品列表的。 |
| result.items[] | productv3GetProductListResponseItem[] | 品列表的。 |
| result.items[].archived | boolean | 商品已归档。 |
| result.items[].has_fbo_stocks | boolean | FBO 仓库有库存。 |
| result.items[].has_fbs_stocks | boolean | FBS 仓库有库存。 |
| result.items[].is_discounted | boolean | 减价商品。 |
| result.items[].offer_id | string | 经济商品标识符。 |
| result.items[].product_id | integer | 商品识别号. |
| result.items[].quants | productv3GetProductListResponseItemQuant | 量子清单. |
| result.items[].quants.quant_code | string | 经济商品标识符。 |
| result.items[].quants.quant_size | integer | 定量包装大小。 |
| result.last_id | string | 页面上最后一个值的ID。<br>要检索以下数值，请从上一个查询的响应中指定 `last_id`。 |
| result.total | integer | 品牌总数。 |


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
    "items": [
      {
        "archived": true,
        "has_fbo_stocks": true,
        "has_fbs_stocks": true,
        "is_discounted": true,
        "offer_id": "136748",
        "product_id": 223681945,
        "quants": [
          {
            "quant_code": "string",
            "quant_size": 0
          }
        ]
      }
    ],
    "total": 1,
    "last_id": "bnVсbA=="
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863047.md

---

## 按SKU获得商品的内容排名

### 接口说明

一种获得商品内容排名的方法，以及如何提高排名的建议。
[与内容排行有关的更多详细信息](https://docs.ozon.ru/global/zh-hans/products/selling-pdp/content-rating/)

### 接口标题

按SKU获得商品的内容排名

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/rating-by-sku`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetProductRatingBySkuRequest | 否 | 请求体。 |
| skus | body | string[] | 是 | 需要返回内容评级的商品SKU列表。 |
| skus[] | body | string[] | 否 | 需要返回内容评级的商品SKU列表。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| products | GetProductRatingBySkuResponseProductRating[] | 商品内容分级。 |
| products[] | GetProductRatingBySkuResponseProductRating[] | 商品内容分级。 |
| products[].sku | integer | Ozon上的卖家系统中的商品标识符 — `product_id`。 |
| products[].rating | number | 产品内容评级: 从0到100。 |
| products[].groups | GetProductRatingBySkuResponseRatingGroup[] | 构成内容评级的各组特征。 |
| products[].groups[] | GetProductRatingBySkuResponseRatingGroup[] | 构成内容评级的各组特征。 |
| products[].groups[].conditions | GetProductRatingBySkuResponseRatingCondition[] | 增加商品内容评级的条件清单。 |
| products[].groups[].conditions[] | GetProductRatingBySkuResponseRatingCondition[] | 增加商品内容评级的条件清单。 |
| products[].groups[].improve_at_least | integer | 为获得该组特征的最高分，需要完成填写的属性数。 |
| products[].groups[].improve_attributes | GetProductRatingBySkuResponseRatingImproveAttribute[] | 属性列表，完成这些属性可以增加商品的内容等级。 |
| products[].groups[].improve_attributes[] | GetProductRatingBySkuResponseRatingImproveAttribute[] | 属性列表，完成这些属性可以增加商品的内容等级。 |
| products[].groups[].key | string | 小组的识别码。 |
| products[].groups[].name | string | 小组名称。 |
| products[].groups[].rating | number | 小组中的排名。 |
| products[].groups[].weight | number | 小组特征对内容排名的影响比例。 |


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
  "products": [
    {
      "sku": 179737222,
      "rating": 42.5,
      "groups": [
        {
          "key": "media",
          "name": "媒体",
          "rating": 70,
          "weight": 25,
          "conditions": [
            {
              "key": "media_images_2",
              "description": "已添加2张图片",
              "fulfilled": true,
              "cost": 50
            },
            {
              "key": "media_video",
              "description": "已添加视频",
              "fulfilled": false,
              "cost": 15
            }
          ],
          "improve_attributes": [
            {
              "id": 4074,
              "name": "视频码"
            }
          ],
          "improve_at_least": 2
        }
      ]
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998321.md

---

## 根据标识符获取商品信息

### 接口说明

用于根据商品标识符获取商品信息的方法。
请求体应包含同类型标识符的数组，响应中将返回 `items` 数组。
单个请求最多可通过 `offer_id`、`product_id` 和 `sku` 传递总计不超过 1000个商品标识符。

### 接口标题

根据标识符获取商品信息

### 接口地址

`POST https://api-seller.ozon.ru/v3/product/info/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v3GetProductInfoListRequest | 否 | 请求体。 |
| offer_id | body | string[] | 否 | 商品在卖家系统中的标识符 — 货号。 |
| offer_id[] | body | string[] | 否 | 商品在卖家系统中的标识符 — 货号。 |
| product_id | body | string[] | 否 | 商品标识符。 |
| product_id[] | body | string[] | 否 | 商品标识符。 |
| sku | body | string[] | 否 | 商品在 Ozon 系统中的标识符 — SKU。 |
| sku[] | body | string[] | 否 | 商品在 Ozon 系统中的标识符 — SKU。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| items | v3GetProductInfoListResponseItem[] | 数据数组。 |
| items[] | v3GetProductInfoListResponseItem[] | 数据数组。 |
| items[].barcodes | string[] | 商品的所有条形码。 |
| items[].barcodes[] | string[] | 商品的所有条形码。 |
| items[].color_image | string[] | 商品颜色图片。 |
| items[].color_image[] | string[] | 商品颜色图片。 |
| items[].commissions | GetProductInfoListResponseCommission[] | 佣金信息。 |
| items[].commissions[] | GetProductInfoListResponseCommission[] | 佣金信息。 |
| items[].commissions[].delivery_amount | number | 配送费用。 |
| items[].commissions[].percent | number | 佣金比例。 |
| items[].commissions[].return_amount | number | 退货费用。 |
| items[].commissions[].sale_schema | string | 销售模式。 |
| items[].commissions[].value | number | 佣金总额。 |
| items[].created_at | string | 商品的创建日期和时间。 |
| items[].currency_code | string | 货币单位。 |
| items[].description_category_id | integer | 类目标识符。<br>可与 [/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes) 和 [/v1/description-category/attribute/values](#operation/DescriptionCategoryAPI_GetAttributeValues) 方法配合使用。 |
| items[].discounted_fbo_stocks | integer | Ozon 仓库中减价商品的库存。 |
| items[].errors | GetProductInfoListResponseError[] | 创建或验证商品时的错误信息。 |
| items[].errors[] | GetProductInfoListResponseError[] | 创建或验证商品时的错误信息。 |
| items[].errors[].attribute_id | integer | 属性标识符。 |
| items[].errors[].code | string | 错误代码。 |
| items[].errors[].field | string | 出现错误的字段。 |
| items[].errors[].level | ErrorErrorLevel | - |
| items[].errors[].state | string | 发生错误的商品状态。 |
| items[].errors[].texts | ErrorHumanTexts | - |
| items[].has_discounted_fbo_item | boolean | 商品在 Ozon 仓库中是否有减价版的同款商品。 |
| items[].id | integer | 商品标识符。 |
| items[].images | string[] | 图片链接数组。 图片在数组中的顺序与网站上的展示顺序一致。 如果<br>`primary_image` 参数未指定，则数组中的第一张图片为商品主图。 |
| items[].images[] | string[] | 图片链接数组。 图片在数组中的顺序与网站上的展示顺序一致。 如果<br>`primary_image` 参数未指定，则数组中的第一张图片为商品主图。 |
| items[].images360 | string[] | 360° 商品图片数组。 |
| items[].images360[] | string[] | 360° 商品图片数组。 |
| items[].is_archived | boolean | 如果商品是手动归档的，则为 `true`。 |
| items[].is_autoarchived | boolean | 如果商品是自动归档的，则为 `true`。 |
| items[].is_discounted | boolean | 商品是否为减价商品：<br>- 如果商品是由卖家作为减价商品创建的，则为 `true`。<br>- 如果商品不是减价商品或是由Ozon减价的，则为 `false`。 |
| items[].is_kgt | boolean | 超大货物标识。 |
| items[].is_prepayment_allowed | boolean | 如果支持预付款，则为 `true`。 |
| items[].is_super | boolean | 超级商品标识。<br>[有关超级商品的详细信息，请参考卖家知识库](https://seller-edu.ozon.ru/fbo/rabota-so-stokom/super-tovary) |
| items[].marketing_price | string | 商品在 Ozon 橱窗中的最终价格，包含所有促销折扣，但不含Ozon 卡优惠。 |
| items[].min_price | string | 应用促销后的最低价格。 |
| items[].model_info | GetProductInfoListResponseModelInfo | - |
| items[].model_info.count | integer | 响应中的商品数量。 |
| items[].model_info.model_id | integer | 商品型号标识符。 |
| items[].name | string | 名称。 |
| items[].offer_id | string | 商品在卖家系统中的标识符 — 货号。 |
| items[].old_price | string | 不含折扣价格。在商品卡片上显示为划线价。 |
| items[].price | string | 商品的含折扣价格。该值将在商品卡片上显示。 |
| items[].price_indexes | GetProductInfoListResponsePriceIndexes | - |
| items[].price_indexes.color_index | PriceIndexesColorIndex | - |
| items[].price_indexes.external_index_data | PriceIndexesIndexDataExternal | - |
| items[].price_indexes.external_index_data.minimal_price | string | 其他平台上竞争对手的最低商品价格。 |
| items[].price_indexes.external_index_data.minimal_price_currency | string | 货币价格。 |
| items[].price_indexes.external_index_data.price_index_value | number | 价格指数的值。 |
| items[].price_indexes.ozon_index_data | PriceIndexesIndexDataOzon | - |
| items[].price_indexes.ozon_index_data.minimal_price | string | Ozon上竞争对手商品的最低价格。 |
| items[].price_indexes.ozon_index_data.minimal_price_currency | string | 货币价值。 |
| items[].price_indexes.ozon_index_data.price_index_value | number | 价格指数的值。 |
| items[].price_indexes.self_marketplaces_index_data | PriceIndexesIndexDataSelf | - |
| items[].price_indexes.self_marketplaces_index_data.minimal_price | string | 您的商品在其他网站上的最低价格。 |
| items[].price_indexes.self_marketplaces_index_data.minimal_price_currency | string | 货币价格。 |
| items[].price_indexes.self_marketplaces_index_data.price_index_value | number | 价格指数的值。 |
| items[].primary_image | string[] | 商品的主图。 |
| items[].primary_image[] | string[] | 商品的主图。 |
| items[].sources | GetProductInfoListResponseSource[] | 商品创建来源信息。 |
| items[].sources[] | GetProductInfoListResponseSource[] | 商品创建来源信息。 |
| items[].sources[].created_at | string | 商品创建日期。 |
| items[].sources[].quant_code | string | 包含商品的定量包装列表。 |
| items[].sources[].shipment_type | SourceShipmentType | - |
| items[].sources[].sku | integer | Ozon平台上的商品标识符 — SKU。 |
| items[].sources[].source | string | 销售模式：<br>- `SDS` — 适用于 FBO 和 FBS，且 SKU 相同；<br>- `FBO`;<br>- `FBS`。 |
| items[].statuses | GetProductInfoListResponseStatuses | - |
| items[].statuses.is_created | boolean | 如果商品创建正确，则为 `true`。 |
| items[].statuses.moderate_status | string | 审核状态。 |
| items[].statuses.status | string | 商品状态。 |
| items[].statuses.status_description | string | 商品状态描述。 |
| items[].statuses.status_failed | string | 发生错误的商品状态。 |
| items[].statuses.status_name | string | 商品状态名称。 |
| items[].statuses.status_tooltip | string | 状态描述。 |
| items[].statuses.status_updated_at | string | 状态最后变更时间。 |
| items[].statuses.validation_status | string | 验证状态。 |
| items[].stocks | GetProductInfoListResponseStocks | - |
| items[].stocks.has_stock | boolean | 如果库存中有剩余，则为 `true`。 |
| items[].stocks.stocks | GetProductInfoListResponseStocksStock[] | 库存状态。 |
| items[].stocks.stocks[] | GetProductInfoListResponseStocksStock[] | 库存状态。 |
| items[].type_id | integer | 商品类型标识符。 |
| items[].updated_at | string | 商品的最后更新时间。 |
| items[].vat | string | 商品的增值税税率。 |
| items[].visibility_details | GetProductInfoListResponseVisibilityDetails | - |
| items[].visibility_details.has_price | boolean | 如果设置了价格，则为 `true`。 |
| items[].visibility_details.has_stock | boolean | 如果仓库有库存，则为 `true`。 |
| items[].volume_weight | number | 商品的体积重量。 |


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
  "items": [
    {
      "barcodes": [
        "string"
      ],
      "color_image": [
        "string"
      ],
      "commissions": [
        null
      ],
      "created_at": "2026-01-01T00:00:00Z",
      "currency_code": "string",
      "description_category_id": 0,
      "discounted_fbo_stocks": 0,
      "errors": [
        null
      ],
      "has_discounted_fbo_item": false,
      "id": 0,
      "images": [
        "string"
      ],
      "images360": [
        "string"
      ],
      "is_archived": false,
      "is_autoarchived": false,
      "is_discounted": false,
      "is_kgt": false,
      "is_prepayment_allowed": false,
      "is_super": false,
      "marketing_price": "string",
      "min_price": "string",
      "model_info": {
        "count": null,
        "model_id": null
      },
      "name": "string",
      "offer_id": "string",
      "old_price": "string",
      "price": "string",
      "price_indexes": {
        "color_index": null,
        "external_index_data": null,
        "ozon_index_data": null,
        "self_marketplaces_index_data": null
      },
      "primary_image": [
        "string"
      ],
      "sources": [
        null
      ],
      "statuses": {
        "is_created": null,
        "moderate_status": null,
        "status": null,
        "status_description": null,
        "status_failed": null,
        "status_name": null,
        "status_tooltip": null,
        "status_updated_at": null,
        "validation_status": null
      },
      "stocks": {
        "has_stock": null,
        "stocks": null
      },
      "type_id": 0,
      "updated_at": "2026-01-01T00:00:00Z",
      "vat": "string",
      "visibility_details": {
        "has_price": null,
        "has_stock": null
      },
      "volume_weight": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863048.md

---

## 获取商品特征描述

### 接口说明

按其识别码退回商品特征的描述。该商品可以通过`offer_id`或`product_id` 搜索。

### 接口标题

获取商品特征描述

### 接口地址

`POST https://api-seller.ozon.ru/v3/products/info/attributes`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productv3GetProductAttributesV3Request | 否 | 请求体。 |
| filter | body | productv3Filter | 是 | - |
| filter.offer_id | body | string[] | 否 | 基于参数 `offer_id`的过滤。 可以提交数值列表。 |
| filter.offer_id[] | body | string[] | 否 | 基于参数 `offer_id`的过滤。 可以提交数值列表。 |
| filter.product_id | body | string[] | 否 | 基于参数 `product_id`的过滤。 可以提交数值列表。 |
| filter.product_id[] | body | string[] | 否 | 基于参数 `product_id`的过滤。 可以提交数值列表。 |
| filter.visibility | body | productv2GetProductListRequestFilterFilterVisibility | 否 | - |
| last_id | body | string | 否 | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。<br>要检索以下数值，请从上一个查询的响应中指定`last_id`。 |
| limit | body | integer | 是 | 每页的值的数量。最小 —— 1，最大 —— 1000。 |
| sort_by | body | string | 否 | 对商品进行分类的参数。 |
| sort_dir | body | string | 否 | 分类方向。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productv3GetProductAttributesV3ResponseResult[] | 查询结果。 |
| result[] | productv3GetProductAttributesV3ResponseResult[] | 查询结果。 |
| result[].attributes | productGetProductAttributesV3ResponseAttribute[] | 商品特性的数组。 |
| result[].attributes[] | productGetProductAttributesV3ResponseAttribute[] | 商品特性的数组。 |
| result[].attributes[].attribute_id | integer | 特征的识别码。 |
| result[].attributes[].complex_id | integer | 支持嵌入属性的特征的识别码。例如，"处理器" 有嵌入属性的特征 "制造商" 和 "二级缓存"。每个嵌入属性都可以有几个值选项。 |
| result[].attributes[].values | productGetProductAttributesV3ResponseDictionaryValue[] | 特征值的数组。 |
| result[].attributes[].values[] | productGetProductAttributesV3ResponseDictionaryValue[] | 特征值的数组。 |
| result[].barcode | string | 条形码。 |
| result[].category_id | integer | 类别ID。<br>请将其与以下方法结合使用：[/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree), [/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes), [/v1/description-category/attribute/values](#operation/DescriptionCategoryAPI_GetAttributeValues).<br>当上述方法被禁用时，此参数也将被禁用。 |
| result[].description_category_id | integer | 类别ID。<br>请将其与以下方法结合使用：[/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes) и [/v1/description-category/attribute/values](#operation/DescriptionCategoryAPI_GetAttributeValues)。 |
| result[].color_image | string | 市场营销色彩。 |
| result[].complex_attributes | productGetProductAttributesV3ResponseComplexAttribute[] | 已录入的特性的数组。 |
| result[].complex_attributes[] | productGetProductAttributesV3ResponseComplexAttribute[] | 已录入的特性的数组。 |
| result[].complex_attributes[].attributes | GetProductAttributesV3ResponseAttribute[] | 商品特征的数组。 |
| result[].complex_attributes[].attributes[] | GetProductAttributesV3ResponseAttribute[] | 商品特征的数组。 |
| result[].depth | integer | 深度。 |
| result[].dimension_unit | string | 尺寸的测量单位。<br>- `mm` —— 毫米，<br>- `cm` —— 厘米，<br>- `in` —— 英寸。 |
| result[].height | integer | 包装高度。 |
| result[].id | integer | 商品特性的识别码。 |
| result[].image_group_id | string | 用于后续批量下载图像的识别码。 |
| result[].images | GetProductAttributesResponseImage[] | 产品图片链接的数组。 |
| result[].images[] | GetProductAttributesResponseImage[] | 产品图片链接的数组。 |
| result[].images[].default | boolean | - |
| result[].images[].file_name | string | - |
| result[].images[].index | integer | - |
| result[].images360 | GetProductAttributesResponseImage360[] | 图像数组360。 |
| result[].images360[] | GetProductAttributesResponseImage360[] | 图像数组360。 |
| result[].images360[].file_name | string | - |
| result[].images360[].index | integer | - |
| result[].name | string | 商品名称。最多500个字符。 |
| result[].offer_id | string | 卖家系统中的商品识别码是卖家系统中的商品标识符是商品货号。 |
| result[].pdf_list | GetProductAttributesResponsePdf[] | PDF文件的阵列。 |
| result[].pdf_list[] | GetProductAttributesResponsePdf[] | PDF文件的阵列。 |
| result[].pdf_list[].file_name | string | 到PDF文件的路径。 |
| result[].pdf_list[].index | integer | 存储库中的设定了顺序的文件指数。 |
| result[].pdf_list[].name | string | 文件名称。 |
| result[].weight | integer | 商品在包装中的重量。 |
| result[].weight_unit | string | 重量测量单位。 |
| result[].type_id | integer | 商品类型的标识符。 |
| result[].width | integer | 包装宽度。 |
| last_id | string | 页面上最后一个值的ID。运行第一个查询时，将此字段留空。<br>要检索以下数值，请从上一个查询的响应中指定`last_id`。 |
| total | string | 列表中的商品数量。 |


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
      "id": 213761435,
      "barcode": "",
      "category_id": 17038062,
      "name": "Пленка защитная для Xiaomi Redmi Note 10 Pro 5G",
      "offer_id": "21470",
      "height": 10,
      "depth": 210,
      "width": 140,
      "dimension_unit": "mm",
      "weight": 50,
      "weight_unit": "g",
      "images": [
        {
          "file_name": "https://cdn1.ozone.ru/s3/multimedia-f/6190456071.jpg",
          "default": true,
          "index": 0
        },
        {
          "file_name": "https://cdn1.ozone.ru/s3/multimedia-7/6190456099.jpg",
          "default": false,
          "index": 1
        },
        {
          "file_name": "https://cdn1.ozone.ru/s3/multimedia-9/6190456065.jpg",
          "default": false,
          "index": 2
        }
      ],
      "images360": [],
      "pdf_list": [],
      "attributes": [
        {
          "attribute_id": 5219,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 970718176,
              "value": "универсальный"
            }
          ]
        },
        {
          "attribute_id": 11051,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 970736931,
              "value": "Прозрачный"
            }
          ]
        },
        {
          "attribute_id": 10100,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "false"
            }
          ]
        },
        {
          "attribute_id": 11794,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 970860783,
              "value": "safe"
            }
          ]
        },
        {
          "attribute_id": 9048,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "Пленка защитная для Xiaomi Redmi Note 10 Pro 5G"
            }
          ]
        },
        {
          "attribute_id": 5076,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 39638,
              "value": "Xiaomi"
            }
          ]
        },
        {
          "attribute_id": 9024,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "21470"
            }
          ]
        },
        {
          "attribute_id": 10015,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "false"
            }
          ]
        },
        {
          "attribute_id": 85,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 971034861,
              "value": "Brand"
            }
          ]
        },
        {
          "attribute_id": 9461,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 349824787,
              "value": "Защитная пленка для смартфона"
            }
          ]
        },
        {
          "attribute_id": 4180,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "Пленка защитная для Xiaomi Redmi Note 10 Pro 5G"
            }
          ]
        },
        {
          "attribute_id": 4191,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 0,
              "value": "Пленка предназначена для модели Xiaomi Redmi Note 10 Pro 5G. Защитная гидрогелевая пленка обеспечит защиту вашего смартфона от царапин, пыли, сколов и потертостей."
            }
          ]
        },
        {
          "attribute_id": 8229,
          "complex_id": 0,
          "values": [
            {
              "dictionary_value_id": 91521,
              "value": "Защитная пленка"
            }
          ]
        }
      ],
      "complex_attributes": [],
      "color_image": "",
      "last_id": ""
    }
  ],
  "total": 1,
  "last_id": "onVsfA=="
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998323.md

---

## 获取商品详细信息

### 接口说明

暂无接口说明。

### 接口标题

获取商品详细信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/info/description`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productGetProductInfoDescriptionRequest | 否 | 请求体。 |
| value | body | object | 否 | - |
| value | body | string | 否 | - |
| value | body | string | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | productGetProductInfoDescriptionResponseProduct | - |
| result.description | string | 描述。 |
| result.id | integer | 识别码。 |
| result.name | string | 名称。 |
| result.offer_id | string | 卖家系统中的商品识别码是卖家系统中的商品标识符是商品货号。 |


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
    "id": 73453843,
    "offer_id": "5",
    "name": "狗狗训练课程 \"三周内拥有乖顺的狗\"",
    "description": "快速课程为全课程的缩减版 \"狗： 训练教程\", 给予最基础的知识、技能、能力。这是迈出训狗教学第一步的最佳选择！<br/><br/>快速课程带来什么:<ul><li>与狗狗交流 </li></ul>快速课程将要结束之时，您将获得在任何时候都伴您左右的温顺小狗陪伴者。<ul><li>安全信心</li></ul>理想狗狗: 再也不会挣脱狗绳、追赶猫猫、吃街上的食物等。<ul><li>Комфортная жизнь</li></ul>更高水平的沟通、对动物行为没有愤怒、喊叫、不满。"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998324.md

---

## 品类限制、商品的创建和更新

### 接口说明

获取限制信息的方式：
- 品类 —  在您的个人中心可创建多少商品。
- 创建商品 — 一天可以创建多少商品。
- 商品更新 — 一天可以修改多少商品。
如果您有品类限制并将其用完，您将无法创建新商品。

### 接口标题

品类限制、商品的创建和更新

### 接口地址

`POST https://api-seller.ozon.ru/v4/product/info/limit`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1Empty | 否 | 请求体。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| daily_create | GetUploadQuotaResponseDailyCreate | - |
| daily_create.limit | integer | 一天可以创建多少商品。 |
| daily_create.reset_at | string | 当前天数计数器值将被重置时，采用 UTC 格式的时间。 |
| daily_create.usage | integer | 近几天创建了多少商品。 |
| daily_update | GetUploadQuotaResponseDailyUpdate | - |
| daily_update.limit | integer | 每天可以更新多少商品。 |
| daily_update.reset_at | string | 当前天数计数器值将被重置时，采用 UTC 格式的时间。 |
| daily_update.usage | integer | 当前几天更新了多少商品。 |
| total | GetUploadQuotaResponseTotal | - |
| total.limit | integer | 在个人中心一共可以创建多少商品。 |
| total.usage | integer | 多少商品已被创建。 |


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
  "daily_create": {
    "limit": 0,
    "reset_at": "2026-01-01T00:00:00Z",
    "usage": 0
  },
  "daily_update": {
    "limit": 0,
    "reset_at": "2026-01-01T00:00:00Z",
    "usage": 0
  },
  "total": {
    "limit": 0,
    "usage": 0
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998325.md

---

## 从卖家的系统中改变商品货号

### 接口说明

改变附加在商品上的 `offer_id`的方法。您可以改变几个 `offer_id`。
建议在一个数组中最多提交250个值。

### 接口标题

从卖家的系统中改变商品货号

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/update/offer-id`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductUpdateOfferIdRequest | 否 | 请求体。 |
| update_offer_id | body | ProductUpdateOfferIdRequestUpdateOfferId[] | 是 | 具有新旧货号价值的配对列表。 |
| update_offer_id[] | body | ProductUpdateOfferIdRequestUpdateOfferId[] | 否 | 具有新旧货号价值的配对列表。 |
| update_offer_id[].new_offer_id | body | string | 是 | 新货号。至50字符。 |
| update_offer_id[].offer_id | body | string | 是 | 旧货号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| errors | v1ProductUpdateOfferIdResponseError[] | 错误清单。 |
| errors[] | v1ProductUpdateOfferIdResponseError[] | 错误清单。 |
| errors[].message | string | 错误信息。 |
| errors[].offer_id | string | 无法更改的卖家系统中的商品标识符是商品货号。 |


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
  "errors": [
    {
      "message": "string",
      "offer_id": "string"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998326.md

---

## 将商品归档

### 接口说明

暂无接口说明。

### 接口标题

将商品归档

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/archive`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productProductArchiveRequest | 否 | 请求体。 |
| product_id | body | integer[] | 是 | 卖家系统中的商品标识符 — `product_id`。您一次最多可以传递100个标识符。 |
| product_id[] | body | integer[] | 否 | 卖家系统中的商品标识符 — `product_id`。您一次最多可以传递100个标识符。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 查询的处理结果。`true`，如果查询的执行无误。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998327.md

---

## 从档案中还原商品

### 接口说明

该方法适用于中国的卖家。

### 接口标题

从档案中还原商品

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/unarchive`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productProductUnarchiveRequest | 否 | 请求体。 |
| product_id | body | integer[] | 是 | 卖家系统中的商品标识符 — `product_id`。您一次最多可以传递100个标识符。<br>商品识别符。您可以一次性转交100个识别符。<br>在一天内，您最多可以从档案中恢复10件自动归档的商品。<br>如果在同一请求中输入更多，那么<br>`restore quota is exceeded`错误将再次出现。<br>限额在莫斯科时间03：00更新。<br>手动归档的商品没有解除归档的限制。 |
| product_id[] | body | integer[] | 否 | 卖家系统中的商品标识符 — `product_id`。您一次最多可以传递100个标识符。<br>商品识别符。您可以一次性转交100个识别符。<br>在一天内，您最多可以从档案中恢复10件自动归档的商品。<br>如果在同一请求中输入更多，那么<br>`restore quota is exceeded`错误将再次出现。<br>限额在莫斯科时间03：00更新。<br>手动归档的商品没有解除归档的限制。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | boolean | 查询的处理结果。`true`，如果查询的执行无误。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998328.md

---

## 从存档删除没有SKU的商品

### 接口说明

在一次请求中最多可以提交500个识别码。

### 接口标题

从存档删除没有SKU的商品

### 接口地址

`POST https://api-seller.ozon.ru/v2/products/delete`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | productv2DeleteProductsRequest | 否 | 请求体。 |
| products | body | DeleteProductsRequestProduct[] | 是 | 卖家系统中的商品标识符 — `product_id`。 |
| products[] | body | DeleteProductsRequestProduct[] | 否 | 卖家系统中的商品标识符 — `product_id`。 |
| products[].offer_id | body | string | 是 | 卖家系统中的商品识别码是卖家系统中的商品标识符是商品货号。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| status | DeleteProductsResponseDeleteStatus[] | 请求的处理情况。 |
| status[] | DeleteProductsResponseDeleteStatus[] | 请求的处理情况。 |
| status[].error | string | 处理该请求时发生错误的原因。 |
| status[].is_deleted | boolean | 如果查询的执行没有错误且商品被删除 —— `true`。 |
| status[].offer_id | string | 卖家系统中的商品识别码是卖家系统中的商品标识符是商品货号。 |


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
  "status": [
    {
      "offer_id": "033",
      "is_deleted": true,
      "error": ""
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998329.md

---

## 上传服务和数字商品的激活码

### 接口说明

如果您上传数字商品或服务，请上传激活码。激活码与数字商品详情页相连。

### 接口标题

上传服务和数字商品的激活码

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/upload_digital_codes`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductUploadDigitalCodesRequest | 否 | 请求体。 |
| digital_codes | body | string[] | 是 | 数字激活码。 |
| digital_codes[] | body | string[] | 否 | 数字激活码。 |
| product_id | body | integer | 是 | 卖家系统中的商品标识符 — `product_id`。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1ProductUploadDigitalCodesResponseResult | - |
| result.task_id | integer | 用于上传代码的任务代码。 |


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
    "task_id": 172549811
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998331.md

---

## 激活码上传状态

### 接口说明

获取服务和数字商品的激活码的上传状态的方法。

### 接口标题

激活码上传状态

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/upload_digital_codes/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductUploadDigitalCodesRequestInfo | 否 | 请求体。 |
| task_id | body | integer | 是 | 方法的响应中收到的激活码下载任务识别码 [/v1/product/upload_digital_codes](#operation/ProductAPI_UploadDigitalCode)。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1ProductUploadDigitalCodesResponseInfoResult | - |
| result.status | string | 上传状态：<br>- `pending` ——  商品在队列中等待处理，<br>- `imported` ——  商品成功上传，<br>- `failed` —— 该商品被加载时出现了错误。 |


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
    "status": "imported"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998332.md

---

## 订阅该商品的用户数

### 接口说明

获取在商品页面上单击 **获取参与详情** 用户数量的方法。
您可以在一个请求中提交多个商品。

### 接口标题

订阅该商品的用户数

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/info/subscription`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1GetProductInfoSubscriptionRequest | 否 | 请求体。 |
| skus | body | string[] | 是 | Ozon 系统中的 SKU、商品标识符列表。 |
| skus[] | body | string[] | 否 | Ozon 系统中的 SKU、商品标识符列表。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetProductInfoSubscriptionResponseResult[] | 操作方法结果。 |
| result[] | v1GetProductInfoSubscriptionResponseResult[] | 操作方法结果。 |
| result[].count | integer | 订阅用户的数量。 |
| result[].sku | integer | Ozon 系统中的商品ID、SKU。 |


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
      "count": 0,
      "sku": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998333.md

---

## 获取相关SKU

### 接口说明

用于通过旧的SKU FBS和SKU FBO标识符获取统一SKU的方法。
响应中将包含所有与传递的SKU相关的SKU。
该方法可以处理任何SKU，包括隐藏的或已删除的SKU。
在一个请求中最多传递200个SKU。

### 接口标题

获取相关SKU

### 接口地址

`POST https://api-seller.ozon.ru/v1/product/related-sku/get`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1ProductGetRelatedSKURequest | 否 | 请求体。 |
| sku | body | string[] | 是 | SKU列表。 |
| sku[] | body | string[] | 否 | SKU列表。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| items | v1ProductGetRelatedSKUResponseItem[] | 相关SKU信息。 |
| items[] | v1ProductGetRelatedSKUResponseItem[] | 相关SKU信息。 |
| items[].availability | string | SKU商品的可用性表示：<br>- `HIDDEN` —— 隐藏；<br>- `AVAILABLE` —— 可用；<br>- `UNAVAILABLE` —— 不可用，SKU已删除。 |
| items[].deleted_at | string | 删除日期和时间。 |
| items[].delivery_schema | string | 配送计划：<br>- `SDS` — Ozon 通用 SKU 编号；<br>- `FBO` — 来自 Ozon 仓库的商品编号；<br>- `FBS` — 来自 FBS 仓库的商品编号；<br>- `Crossborder` — 跨境销售商品编号。 |
| items[].product_id | integer | 卖家系统中的商品标识符 — `product_id`。 |
| items[].sku | integer | Ozon系统中的商品ID —— SKU。 |
| errors | v1ProductGetRelatedSKUResponseError[] | 错误。 |
| errors[] | v1ProductGetRelatedSKUResponseError[] | 错误。 |
| errors[].code | string | 代码有误。 |
| errors[].sku | integer | 有错误的SKU。 |
| errors[].message | string | 文本错误。 |


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
  "items": [
    {
      "availability": "string",
      "deleted_at": "2026-01-01T00:00:00Z",
      "delivery_schema": "string",
      "product_id": 0,
      "sku": 0
    }
  ],
  "errors": [
    {
      "code": "string",
      "sku": 0,
      "message": "string"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863049.md

---

## 获取商品图片

### 接口说明

暂无接口说明。

### 接口标题

获取商品图片

### 接口地址

`POST https://api-seller.ozon.ru/v2/product/pictures/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v2ProductInfoPicturesRequest | 否 | 请求体。 |
| product_id | body | string[] | 是 | 商品识别码的清单。 |
| product_id[] | body | string[] | 否 | 商品识别码的清单。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| items | v2ProductInfoPicturesResponseItem[] | 商品图片。 |
| items[] | v2ProductInfoPicturesResponseItem[] | 商品图片。 |
| items[].product_id | integer | 商品标识符。 |
| items[].primary_photo | string[] | 主图链接。 |
| items[].primary_photo[] | string[] | 主图链接。 |
| items[].photo | string[] | 商品照片链接。 |
| items[].photo[] | string[] | 商品照片链接。 |
| items[].color_photo | string[] | 上传的颜色样本链接。 |
| items[].color_photo[] | string[] | 上传的颜色样本链接。 |
| items[].photo_360 | string[] | 360度图片链接。 |
| items[].photo_360[] | string[] | 360度图片链接。 |
| items[].errors | v2ProductInfoPicturesResponseError[] | 商品图片相关错误列表。 |
| items[].errors[] | v2ProductInfoPicturesResponseError[] | 商品图片相关错误列表。 |
| items[].errors[].message | string | 错误描述。 |
| items[].errors[].url | string | 图片链接。 |


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
  "items": [
    {
      "product_id": 0,
      "primary_photo": [
        "string"
      ],
      "photo": [
        "string"
      ],
      "color_photo": [
        "string"
      ],
      "photo_360": [
        "string"
      ],
      "errors": [
        null
      ]
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863050.md

---
