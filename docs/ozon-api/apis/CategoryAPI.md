# CategoryAPI

接口数量：4

## 接口列表

- [商品类别和类型的树形图](#商品类别和类型的树形图) - `POST /v1/description-category/tree`
- [类别特征列表](#类别特征列表) - `POST /v1/description-category/attribute`
- [特征值指南](#特征值指南) - `POST /v1/description-category/attribute/values`
- [根据属性的参考值进行搜索](#根据属性的参考值进行搜索) - `POST /v1/description-category/attribute/values/search`

## 商品类别和类型的树形图

### 接口说明

返回商品的类别和类型的树形图。
只有在最后级别的类别中可以创建商品，请对比它们，是否与平台上的类别相符合。
类别不会根据用户请求而创建。
请慎重为商品选择类别：不同的类别会有不同的佣金。

### 接口标题

商品类别和类型的树形图

### 接口地址

`POST https://api-seller.ozon.ru/v1/description-category/tree`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetTreeRequest | 否 | 请求体。 |
| language | body | languageLanguage | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetTreeResponseItem[] | 类别清单。 |
| result[] | v1GetTreeResponseItem[] | 类别清单。 |
| result[].description_category_id | integer | 类别ID。 |
| result[].category_name | string | 类别名称。 |
| result[].children | v1GetTreeResponseItem[] | 子类别树形图。 |
| result[].children[] | v1GetTreeResponseItem[] | 子类别树形图。 |
| result[].disabled | boolean | 如果无法在类别中创建商品，则为`true`。 如果可能，为`false`。 |
| result[].type_id | integer | 商品类型ID。 |
| result[].type_name | string | 商品类型名称。 |


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
      "description_category_id": 0,
      "category_name": "string",
      "disabled": false,
      "children": [
        {
          "description_category_id": 0,
          "category_name": "string",
          "disabled": false,
          "children": [
            {
              "type_name": "sting",
              "type_id": 0,
              "disabled": false,
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998307.md

---

## 类别特征列表

### 接口说明

获取指定类别和类型的商品特征。
如果`dictionary_id` 的值为`0`，则该属性没有嵌套指南。
如果值不同，还有指南。使用[/v1/description-category/attribute/values](#operation/DescriptionCategoryAPI_GetAttributeValues)方法请求。

### 接口标题

类别特征列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/description-category/attribute`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetAttributesRequest | 否 | 请求体。 |
| description_category_id | body | integer | 是 | 类别ID。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |
| language | body | languageLanguage | 否 | - |
| type_id | body | integer | 是 | 商品类型ID。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | v1GetAttributesResponseAttribute[] | 请求结果。 |
| result[] | v1GetAttributesResponseAttribute[] | 请求结果。 |
| result[].category_dependent | boolean | 字典属性值取决于类别的标志：<br>- `true` — 该属性对每个类别都有不一样的值。<br>- `false` — 该属性对所有类别都有相同的值。 |
| result[].description | string | 特征描述。 |
| result[].dictionary_id | integer | 目录ID。 |
| result[].group_id | integer | 组别特征ID。 |
| result[].group_name | string | 特征组别名称。 |
| result[].id | integer | 形成文件的任务量。 |
| result[].is_aspect | boolean | 方面属性特征。方面属性：用于区分同类商品不同特征的属性。<br>例如，同款衣服和鞋子具有不同的颜色和尺寸，即：颜色、尺寸为方面属性。<br>字段值：<br>- `true` — 方面属性，在货物交付到仓库或出仓销售后不能更改。<br>- `false` — 非方面属性，可在任何时间改变。 |
| result[].is_collection | boolean | 标志、特征 — 值集：<br>- `true` — 特征 — 值集,<br>- `false` — 特性由单个值组成。 |
| result[].is_required | boolean | 强制性特征标志:<br>- `true` — 强制性特征,<br>- `false` — 可不指出特征。 |
| result[].name | string | 名称。 |
| result[].type | string | 特征类型。 |
| result[].attribute_complex_id | integer | 复合属性的标识符。 |
| result[].max_value_count | integer | 属性的最大值数量。 |
| result[].complex_is_collection | boolean | 标志某个复合特征是否为值集合：<br>- `true` 表示该复合特征是一个值集合；<br>- `false` 表示该复合特征只有一个值。 |


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
      "category_dependent": false,
      "description": "string",
      "dictionary_id": 0,
      "group_id": 0,
      "group_name": "string",
      "id": 0,
      "is_aspect": false,
      "is_collection": false,
      "is_required": false,
      "name": "string",
      "type": "string",
      "attribute_complex_id": 0,
      "max_value_count": 0,
      "complex_is_collection": false
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998309.md

---

## 特征值指南

### 接口说明

返回特征值指南。
通过方法[/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes)可以查询是否存在嵌套指南。

### 接口标题

特征值指南

### 接口地址

`POST https://api-seller.ozon.ru/v1/description-category/attribute/values`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1GetAttributeValuesRequest | 否 | 请求体。 |
| attribute_id | body | integer | 是 | 特性ID。可以使用方法 [/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes)获取。 |
| description_category_id | body | integer | 是 | 类别ID。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |
| language | body | languageLanguage | 否 | - |
| last_value_id | body | integer | 否 | 启动响应的指南 ID。 如果`last_value_id`为 10，则响应将包含从第十一个开始的指南。 |
| limit | body | integer | 是 | 响应中值的数量：<br>- 最多 —— 2000，<br>- 最少 —— 1。 |
| type_id | body | integer | 是 | 商品类型ID。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| has_next | boolean | 该特征表示响应中只返回了部分特性值：<br>- `true` —— 请用新参数 `last_value_id` 再次请求以获取其它值；<br>- `false` —— 响应包含了所有特性值。 |
| result | v1GetAttributeValuesResponseDictionaryValue[] | 特性值。 |
| result[] | v1GetAttributeValuesResponseDictionaryValue[] | 特性值。 |
| result[].id | integer | 特性值ID。 |
| result[].info | string | 附加描述。 |
| result[].picture | string | 图片链接。 |
| result[].value | string | 商品特性值。 |


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
  "has_next": false,
  "result": [
    {
      "id": 0,
      "info": "string",
      "picture": "string",
      "value": "string"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998311.md

---

## 根据属性的参考值进行搜索

### 接口说明

根据请求中的指定值`value`返回属性的参考值。
是否存在嵌套参考表，可以通过方法 [/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes) 进行查询。

### 接口标题

根据属性的参考值进行搜索

### 接口地址

`POST https://api-seller.ozon.ru/v1/description-category/attribute/values/search`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v1SearchAttributeValuesRequest | 否 | 请求体。 |
| attribute_id | body | integer | 是 | 属性的标识符。可以使用方法 [/v1/description-category/attribute](#operation/DescriptionCategoryAPI_GetAttributes)获取。 |
| description_category_id | body | integer | 是 | 类目的标识符。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |
| limit | body | integer | 是 | 返回结果中的值数量：:<br>- 最大值 — 100，<br>- 最小值 — 1。 |
| type_id | body | integer | 是 | 商品类型的标识符。可以使用方法 [/v1/description-category/tree](#operation/DescriptionCategoryAPI_GetTree)获取。 |
| value | body | string | 是 | 系统将根据此值搜索参考值。最少需要2个字符。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | SearchAttributeValuesResponseValue[] | 属性值。 |
| result[] | SearchAttributeValuesResponseValue[] | 属性值。 |
| result[].id | integer | 属性值的标识符。 |
| result[].info | string | 额外信息。 |
| result[].picture | string | 图片链接。 |
| result[].value | string | - |


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
      "id": 0,
      "info": "string",
      "picture": "string",
      "value": "string"
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863045.md

---
