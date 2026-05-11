# ReviewAPI

接口数量：7

## 接口列表

- [对评价留下评论](#对评价留下评论) - `POST /v1/review/comment/create`
- [删除对评价的评论](#删除对评价的评论) - `POST /v1/review/comment/delete`
- [评价的评论列表](#评价的评论列表) - `POST /v1/review/comment/list`
- [更改评价状态](#更改评价状态) - `POST /v1/review/change-status`
- [根据状态统计的评价数量](#根据状态统计的评价数量) - `POST /v1/review/count`
- [获取评价信息](#获取评价信息) - `POST /v1/review/info`
- [获取评价列表](#获取评价列表) - `POST /v1/review/list`

## 对评价留下评论

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。

### 接口标题

对评价留下评论

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/comment/create`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1CommentCreateRequest | 否 | 请求体。 |
| mark_review_as_processed | body | boolean | 否 | 更新评论状态：<br>- `true` — 状态将变更为 `Processed`（已处理）；<br>- `false` — 状态不变。 |
| parent_comment_id | body | string | 否 | 父级评论的标识符（您要回复的评论）。 |
| review_id | body | string | 是 | 评价标识符。 |
| text | body | string | 是 | 评论内容。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| comment_id | string | 评论标识符。 |


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
  "comment_id": "string"
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863097.md

---

## 删除对评价的评论

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。

### 接口标题

删除对评价的评论

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/comment/delete`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1CommentDeleteRequest | 否 | 请求体。 |
| comment_id | body | string | 是 | 评论标识符。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863098.md

---

## 评价的评论列表

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。
该方法返回已通过审核的评价评论信息。

### 接口标题

评价的评论列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/comment/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1CommentListRequest | 否 | 请求体。 |
| limit | body | integer | 是 | 限制回复中的值数量。<br>最少 — 20；最多 — 100。 |
| offset | body | integer | 否 | 从列表开头跳过的元素数量：例如，如果 `offset = 10`，那么回复将从找到的第11个元素开始。 |
| review_id | body | string | 是 | 评价标识符。 |
| sort_dir | body | v1CommentSort | 否 | - |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| comments | CommentListResponseComment[] | 评论信息。 |
| comments[] | CommentListResponseComment[] | 评论信息。 |
| comments[].id | string | 评论标识符。 |
| comments[].is_official | boolean | `true`：评论是由官方人员留下的；`false`：评论是由买家留下的。 |
| comments[].is_owner | boolean | `true`：评论是由卖家留下的；`false`：评论是由买家留下的。 |
| comments[].parent_comment_id | string | 父级评论的标识符（需要对此评论进行回复）。 |
| comments[].published_at | string | 评论发布日期。 |
| comments[].text | string | 评论内容。 |
| offset | integer | 搜索结果中的元素数量。 |


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
  "comments": [
    {
      "id": "string",
      "is_official": false,
      "is_owner": false,
      "parent_comment_id": "string",
      "published_at": "2026-01-01T00:00:00Z",
      "text": "string"
    }
  ],
  "offset": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863099.md

---

## 更改评价状态

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。

### 接口标题

更改评价状态

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/change-status`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ReviewChangeStatusRequest | 否 | 请求体。 |
| review_ids | body | string[] | 是 | 包含评价标识符的数组（数量在1到100之间）。 |
| review_ids[] | body | string[] | 否 | 包含评价标识符的数组（数量在1到100之间）。 |
| status | body | string | 是 | 评价状态：<br>- `PROCESSED` — 已处理。<br>- `UNPROCESSED` — 未处理。 |


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


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863100.md

---

## 根据状态统计的评价数量

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。

### 接口标题

根据状态统计的评价数量

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/count`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | QuestionAPI_GetQuestionCountBody | 否 | 请求体。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| processed | integer | 已处理评价的数量。 |
| total | integer | 评价的总数量。 |
| unprocessed | integer | 未处理评价的数量。 |


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
  "processed": 0,
  "total": 0,
  "unprocessed": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863101.md

---

## 获取评价信息

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。

### 接口标题

获取评价信息

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/info`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ReviewInfoRequest | 否 | 请求体。 |
| review_id | body | string | 是 | 评价标识符。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| comments_amount | integer | 评价的回复数量。 |
| dislikes_amount | integer | 评价的踩数量。 |
| id | string | 评价标识符。 |
| is_rating_participant | boolean | `true`：评论是由官方人员留下的；`false`：评论是由买家留下的。 |
| likes_amount | integer | 评价的点赞数量。 |
| order_status | string | 买家留下评价的订单状态：<br>- `DELIVERED`— 已送达，<br>- `CANCELLED` — 已取消。 |
| photos | ReviewInfoResponsePhoto[] | 图片信息。 |
| photos[] | ReviewInfoResponsePhoto[] | 图片信息。 |
| photos[].height | integer | 高度。 |
| photos[].url | string | 图片链接。 |
| photos[].width | integer | 宽度。 |
| photos_amount | integer | 评价中的图片数量。 |
| published_at | string | 评价的发布日期。 |
| rating | integer | 评价评分。 |
| sku | integer | Ozon系统中的商品识别符——SKU。 |
| status | string | 评价状态：<br>- `UNPROCESSED` — 未处理，<br>- `PROCESSED` — 已处理。 |
| text | string | 评价文字。 |
| videos | ReviewInfoResponseVideo[] | 视频信息。 |
| videos[] | ReviewInfoResponseVideo[] | 视频信息。 |
| videos[].height | integer | 高度。 |
| videos[].preview_url | string | 预览视频链接。 |
| videos[].short_video_preview_url | string | 短视频链接。 |
| videos[].url | string | 视频链接。 |
| videos[].width | integer | 宽度。 |
| videos_amount | integer | 评价中的视频数量。 |


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
  "comments_amount": 0,
  "dislikes_amount": 0,
  "id": "string",
  "is_rating_participant": false,
  "likes_amount": 0,
  "order_status": "string",
  "photos": [
    {
      "height": 0,
      "url": "string",
      "width": 0
    }
  ],
  "photos_amount": 0,
  "published_at": "2026-01-01T00:00:00Z",
  "rating": 0,
  "sku": 0,
  "status": "string",
  "text": "string",
  "videos": [
    {
      "height": 0,
      "preview_url": "string",
      "short_video_preview_url": "string",
      "url": "string",
      "width": 0
    }
  ],
  "videos_amount": 0
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863102.md

---

## 获取评价列表

### 接口说明

仅适用于拥有 Premium Plus 订阅的卖家。
您可以在开发者社区 Ozon for dev 的[讨论](https://dev.ozon.ru/community/1190-Metody-dlia-raboty-s-otzyvami)区中，留下对此方法的反馈。
该方法不会返回商品评价中的“优点”和“缺点”参数（如果有）。 这些参数已过时，新的评价中不再包含这些参数。

### 接口标题

获取评价列表

### 接口地址

`POST https://api-seller.ozon.ru/v1/review/list`

### 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| body | body | v1ReviewListRequest | 否 | 请求体。 |
| last_id | body | string | 否 | 页面中最后一个评价的标识符。 |
| limit | body | integer | 是 | 限制回复中的值数量。最少 — 20；最多 — 100。 |
| sort_dir | body | string | 否 | 排序方向：<br>- `ASC` — 按升序。<br>- `DESC` — 按降序。 |
| status | body | string | 否 | 评价状态：<br>- `ALL` — 全部，<br>- `UNPROCESSED` — 未处理的，<br>- `PROCESSED` — 已处理的。 |


### 响应参数

#### 200 成功

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| has_next | boolean | `true`：回复中未返回所有评价。 |
| last_id | string | 页面中最后一个评价的标识符。 |
| reviews | ReviewListResponseReview[] | 评价信息。 |
| reviews[] | ReviewListResponseReview[] | 评价信息。 |
| reviews[].comments_amount | integer | 评价的评论数量。 |
| reviews[].id | string | 评价标识符。 |
| reviews[].is_rating_participant | boolean | `true`：如果评价被计入评级计算。 |
| reviews[].order_status | string | 买家留下评价的订单状态：<br>- `DELIVERED`— 已送达，<br>- `CANCELLED` — 已取消。 |
| reviews[].photos_amount | integer | 评价中的图片数量。 |
| reviews[].published_at | string | 评价的发布时间。 |
| reviews[].rating | integer | 评价的评分。 |
| reviews[].sku | integer | Ozon系统中的商品识别符——SKU。 |
| reviews[].status | string | 评价状态：<br>- `UNPROCESSED` — 未处理，<br>- `PROCESSED` — 已处理。 |
| reviews[].text | string | 评价文字。 |
| reviews[].videos_amount | integer | 评价的视频数量。 |


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
  "last_id": "string",
  "reviews": [
    {
      "comments_amount": 0,
      "id": "string",
      "is_rating_participant": false,
      "order_status": "string",
      "photos_amount": 0,
      "published_at": "2026-01-01T00:00:00Z",
      "rating": 0,
      "sku": 0,
      "status": "string",
      "text": "string",
      "videos_amount": 0
    }
  ]
}
```


来源：https://s.apifox.cn/apidoc/docs-site/3531025/api-306863103.md

---
