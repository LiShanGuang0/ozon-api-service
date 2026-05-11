# ChatAPI

接口数量：7

## 接口列表

- [发送信息](#发送信息) - `POST /v1/chat/send/message`
- [发送文件](#发送文件) - `POST /v1/chat/send/file`
- [创建新聊天](#创建新聊天) - `POST /v1/chat/start`
- [聊天清单](#聊天清单) - `POST /v2/chat/list`
- [聊天历史记录](#聊天历史记录) - `POST /v2/chat/history`
- [聊天历史记录](#聊天历史记录) - `POST /v3/chat/history`
- [将信息标记为已读](#将信息标记为已读) - `POST /v2/chat/read`

## 发送信息

### 接口说明

通过识别码向现有聊天发送消息。

### 接口标题

发送信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/chat/send/message`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | chatChatSendMessageRequest | 否 | 请求体。 |
| chat_id | body | string | 是 | 聊天识别码。 |
| text | body | string | 是 | plain文本格式的信息文本1到1000个字符。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | string | 请求的处理结果。 |


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
  "result": "success"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998399.md

---

## 发送文件

### 接口说明

通过文件的识别码将文件发送到现有的聊天。

### 接口标题

发送文件

### 接口地址

`POST https://api-seller.ozon.ru/v1/chat/send/file`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | chatChatSendFileRequest | 否 | 请求体。 |
| base64_content | body | string | 否 | 文件为 base64 行形式。 |
| chat_id | body | string | 是 | 聊天识别码。 |
| name | body | string | 否 | 带有扩展名的文件名。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | string | 请求的处理结果。 |


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
  "result": "success"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998400.md

---

## 创建新聊天

### 接口说明

与买家建立关于的快递的新聊天。例如，为了确定地址或商品型号。

### 接口标题

创建新聊天

### 接口地址

`POST https://api-seller.ozon.ru/v1/chat/start`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | chatChatStartRequest | 否 | 请求体。 |
| posting_number | body | string | 是 | 发货识别码。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| result | ChatStartResponseResult | - |
| result.chat_id | string | 聊天识别码。 |


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
    "chat_id": "5969c331-2e64-44b7-8a0e-ff9526762c62"
  }
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998403.md

---

## 聊天清单

### 接口说明

根据指定的过滤器发回关于聊天的信息。

### 接口标题

聊天清单

### 接口地址

`POST https://api-seller.ozon.ru/v2/chat/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | ChatList | 否 | 请求体。 |
| filter | body | ChatListRequestFilter | 否 | - |
| filter.chat_status | body | string | 否 | 按聊天状态过滤：<br>- `All` — 所有聊天。<br>- `Opened` — 开放的聊天。<br>- `Closed` — 不开放的聊天。<br>默认值：`All`。 |
| filter.unread_only | body | boolean | 否 | 按有未读信息的聊天过滤。 |
| limit | body | integer | 是 | 回答中值的数量。默认值为30。最大值是1000。 |
| offset | body | integer | 否 | 回答中要跳过的元素的数量。例如，如果 `offset=10`，回答将从找到的第11个元素开始。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| chats | ChatInfo[] | 聊天数据。 |
| chats[] | ChatInfo[] | 聊天数据。 |
| chats[].chat_id | string | 聊天识别码。 |
| chats[].chat_status | string | 聊天状态：<br>- `All` — 所有聊天。<br>- `Opened` — 开放的聊天。<br>- `Closed` — 不开放的聊天。 |
| chats[].chat_type | string | 聊天类型：<br>- `Seller_Support` — 与帮助中心聊天。<br>- `Buyer_Sueller` — 与买家聊天。 |
| chats[].created_at | string | 聊天的创建日期。 |
| chats[].first_unread_message_id | integer | 第一条未读聊天信息的识别码。 |
| chats[].last_message_id | integer | 最后一条聊天信息的识别码。 |
| chats[].unread_count | integer | 聊天中未读消息的数量。 |
| total_chats_count | integer | 聊天总数。 |
| total_unread_count | integer | 未读信息总数。 |


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
  "chats": [
    {
      "chat": {
        "created_at": "2022-07-22T08:07:19.581Z",
        "chat_id": "5e767w03-b400-4y1b-a841-75319ca8a5c8",
        "chat_status": "Opened",
        "chat_type": "Seller_Support"
      },
      "first_unread_message_id": "3000000000118021931",
      "last_message_id": "30000000001280042740",
      "unread_count": 1
    }
  ],
  "total_chats_count": 25,
  "total_unread_count": 5
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998404.md

---

## 聊天历史记录

### 接口说明

2025年7月13日，旧方法将被停用。请切换到/v3/chat/history。
恢复聊天室消息历史记录。默认顺序为从最新消息到之前的消息。

### 接口标题

聊天历史记录

### 接口地址

`POST https://api-seller.ozon.ru/v2/chat/history`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | ChatHistory | 否 | 请求体。 |
| chat_id | body | string | 是 | 聊天识别码。 |
| direction | body | string | 否 | 信息排序方向：<br>- `Forward` — 从旧到新。<br>- `Backward` — 从新到旧。<br>默认值是 — `Backward`。消息的数量可以在 `limit`参数中设置。 |
| from_message_id | body | integer | 否 | 从该信息开始整理聊天记录的消息识别码。默认为从最后 — 条可见信息。 |
| limit | body | integer | 是 | 答复的信息数量。默认设置为50。最大值是1000。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| has_next | boolean | 表示不是所有信息都在答复中返回。 |
| messages | v2ChatMessage[] | 根据请求正文中的`direction`参数排序的信息数组。 |
| messages[] | v2ChatMessage[] | 根据请求正文中的`direction`参数排序的信息数组。 |
| messages[].created_at | string | 信息创建日期。 |
| messages[].data | string[] | Markdown格式的带有信息内容的数组。 |
| messages[].data[] | string[] | Markdown格式的带有信息内容的数组。 |
| messages[].is_read | boolean | 表示信息已读。 |
| messages[].messageId | integer | 信息识别码。 |
| messages[].user | v2User | - |
| messages[].user.id | string | 聊天参与者的身份。 |
| messages[].user.type | string | 聊天参与者类型：<br>- `customer` — 买家，<br>- `seller` — 卖家，<br>- `crm` — 系统信息，<br>- `courier` — 快递员，<br>- `support` — 客服。 |


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
  "has_next": true,
  "messages": [
    {
      "message_id": "3000000000817031942",
      "user": {
        "id": "115568",
        "type": "Сustomer"
      },
      "created_at": "2022-07-18T20:58:04.528Z",
      "is_read": true,
      "data": [
        "Здравствуйте, у меня вопрос по вашему товару \"Стекло защитное для смартфонов\", артикул 11223. Подойдет ли он на данную [ модель ](https://www.ozon.ru/product/smartfon-samsung-galaxy-a03s-4-64-gb-chernyy) телефона?"
      ]
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998405.md

---

## 聊天历史记录

### 接口说明

恢复聊天室消息历史记录。默认顺序为从最新消息到之前的消息。

### 接口标题

聊天历史记录

### 接口地址

`POST https://api-seller.ozon.ru/v3/chat/history`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | v3ChatHistoryRequest | 否 | 请求体。 |
| chat_id | body | string | 是 | 聊天识别码。 |
| direction | body | string | 否 | 信息排序方向：<br>- `Forward` — 从旧到新。<br>- `Backward` — 从新到旧。<br>默认值是 — `Backward`。消息的数量可以在 `limit`参数中设置。 |
| filter | body | ChatHistoryRequestFilter | 否 | - |
| filter.message_ids | body | string[] | 否 | 消息标识符。 |
| filter.message_ids[] | body | string[] | 否 | 消息标识符。 |
| from_message_id | body | integer | 否 | 从该信息开始整理聊天记录的消息识别码。默认为从最后 — 条可见信息。 |
| limit | body | integer | 否 | 答复的信息数量。默认设置为50。最大值是1000。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| has_next | boolean | 表示不是所有信息都在答复中返回。 |
| messages | v3ChatMessage[] | 根据请求正文中的`direction`参数排序的信息数组。 |
| messages[] | v3ChatMessage[] | 根据请求正文中的`direction`参数排序的信息数组。 |
| messages[].context | ChatMessageContext | - |
| messages[].context.order_number | string | 订单编号。 |
| messages[].context.sku | string | Ozon系统中的商品识别码是SKU。 |
| messages[].created_at | string | 信息创建日期。 |
| messages[].data | string[] | Markdown格式的带有信息内容的数组。 |
| messages[].data[] | string[] | Markdown格式的带有信息内容的数组。 |
| messages[].is_image | boolean | 消息包含图片的标志。 |
| messages[].is_read | boolean | 表示信息已读。 |
| messages[].messageId | integer | 信息识别码。 |
| messages[].moderate_image_status | ChatMessageModerateImageStatus | - |
| messages[].user | v3User | - |
| messages[].user.id | string | 聊天参与者的身份。 |
| messages[].user.type | string | 聊天参与者类型：<br>- `customer` — 买家，<br>- `seller` — 卖家，<br>- `crm` — 系统信息，<br>- `courier` — 快递员，<br>- `support` — 客服。 |


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
  "has_next": true,
  "messages": [
    {
      "context": {
        "order_number": "123456789",
        "sku": "987654321"
      },
      "created_at": "2019-08-24T14:15:22Z",
      "data": [
        "Здравствуйте, у меня вопрос по вашему товару \"Стекло защитное для смартфонов\", артикул 11223. Подойдет ли он на данную [ модель ](https://www.ozon.ru/product/smartfon-samsung-galaxy-a03s-4-64-gb-chernyy) телефона?"
      ],
      "is_image": true,
      "is_read": true,
      "message_id": "3000000000817031942",
      "moderate_image_status": "SUCCESS",
      "user": {
        "id": "115568",
        "type": "Сustomer"
      }
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863062.md

---

## 将信息标记为已读

### 接口说明

一种将选定的信息和其之前的信息标记为已读的方法。

### 接口标题

将信息标记为已读

### 接口地址

`POST https://api-seller.ozon.ru/v2/chat/read`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| Client-Id | header | string | 是 | 用户识别号。 |
| Api-Key | header | string | 是 | API-密钥。 |
| body | body | ChatRead | 否 | 请求体。 |
| chat_id | body | string | 是 | 聊天识别码。 |
| from_message_id | body | integer | 否 | 信息识别码。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| unread_count | integer | 聊天中未读消息的数量。 |


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
  "unread_count": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-121998406.md

---
