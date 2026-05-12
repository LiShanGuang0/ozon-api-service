# FastAPI 转发服务说明

服务代码位于项目根目录的 `app/`，当前已按生产级分层结构组织。

## 目录结构

```text
app/
  main.py                    # FastAPI 应用工厂
  api/
    deps.py                  # FastAPI 依赖注入
    router.py                # 总路由
    routes/                  # 轻量 HTTP 路由层
      categories.py
      health.py
      products.py
      proxy.py
      tasks.py
  clients/
    ozon.py                  # Ozon HTTP 客户端
  core/
    config.py                # 环境配置
    exceptions.py            # 统一异常
    logging.py               # 日志配置
    security.py              # Client-Id / Api-Key 读取与指纹
  db/
    mysql.py                 # MySQL 连接
    redis.py                 # Redis 连接
  repositories/
    api_logs.py              # API 调用日志入库
    products.py              # 商品映射入库
    tasks.py                 # 异步任务入库
  models/
    products.py              # 数据库表模型
    tasks.py
    caches.py
    logs.py
  schemas/
    categories.py            # 请求/响应模型
    products.py
    tasks.py
    common.py
  services/
    categories.py            # 类目业务服务
    credential_store.py      # Redis 短期凭证
    ozon_forwarder.py        # 转发 + 日志
    product_import.py        # 创建/更新商品编排
    products.py              # 商品查询/图片服务
  workers/
    poll_import_tasks.py     # 后台轮询任务入口
  utils/
    json.py
```

## 模型分层

- `app/models/`：数据库表模型，和 `schema.sql` 中的表结构对应，用于表达持久化数据，例如 `OzonProduct`、`OzonImportTask`。
- `app/schemas/`：HTTP 请求/响应模型，用于 Swagger 展示和参数校验，例如 `ProductImportRequest`、`ProductImportResponse`。
- `app/repositories/`：负责 SQL 和表读写。
- `app/services/`：负责业务流程编排，例如创建商品时先查额度、再提交导入、保存任务。
- `app/api/routes/`：只负责 HTTP 入参、依赖注入和调用服务层。

## 启动

安装依赖：

```bash
pip install -r requirements.txt
```

启动服务：

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

接口文档：

- Swagger UI：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health
- API 健康检查：http://127.0.0.1:8000/api/health

## 凭证传递

前端或调用方每次请求都需要传：

```http
Client-Id: <Ozon Client-Id>
Api-Key: <Ozon Api-Key>
Content-Type: application/json
```

服务不会把 `Api-Key` 明文写入 MySQL。创建/更新商品产生异步任务时，服务会把凭证短期写入 Redis，并在 MySQL 的 `ozon_import_tasks.credential_ref` 保存 Redis key。

## Redis 缓存

Redis 当前用于两类数据：

| 用途 | Key 前缀 | 默认 TTL | 说明 |
| --- | --- | --- | --- |
| Ozon 短期凭证 | `ozon:credentials:` | `OZON_CREDENTIAL_TTL_SECONDS=3600` | 创建/更新商品返回 `task_id` 后，用于后续轮询任务，不把明文 Api-Key 写入 MySQL。 |
| 类目树 | `ozon:category-cache:{Client-Id}:tree:` | `OZON_CATEGORY_TREE_TTL_SECONDS=86400` | 缓存 `/v1/description-category/tree` 响应。 |
| 类目属性 | `ozon:category-cache:{Client-Id}:attributes:` | `OZON_CATEGORY_ATTRIBUTES_TTL_SECONDS=43200` | 缓存 `/v1/description-category/attribute` 响应。 |
| 属性字典值 | `ozon:category-cache:{Client-Id}:values:` | `OZON_ATTRIBUTE_VALUES_TTL_SECONDS=21600` | 缓存 `/v1/description-category/attribute/values` 响应。 |
| 属性字典值搜索 | `ozon:category-cache:{Client-Id}:values-search:` | `OZON_ATTRIBUTE_VALUES_TTL_SECONDS=21600` | 缓存 `/v1/description-category/attribute/values/search` 响应。 |

类目相关缓存按 `Client-Id` 隔离，并使用请求参数的稳定 hash 作为 key 的一部分。命中 Redis 时不会再次请求 Ozon，也不会新增 Ozon API 调用日志。

## 已实现接口

### 通用转发

```http
POST /api/ozon/proxy/{endpoint}
```

示例：

```bash
curl -X POST "http://127.0.0.1:8000/api/ozon/proxy/v1/description-category/tree" ^
  -H "Client-Id: xxx" ^
  -H "Api-Key: yyy" ^
  -H "Content-Type: application/json" ^
  -d "{\"language\":\"DEFAULT\"}"
```

### 商品创建/更新流程

| 本地接口 | 转发/整合的 Ozon 接口 | 说明 |
| --- | --- | --- |
| `POST /api/ozon/product/info/limit` | `/v4/product/info/limit` | 查询创建/更新额度 |
| `POST /api/ozon/categories/tree` | `/v1/description-category/tree` | 查询类目树 |
| `POST /api/ozon/categories/attributes` | `/v1/description-category/attribute` | 查询类目特征 |
| `POST /api/ozon/categories/attribute-values` | `/v1/description-category/attribute/values` | 查询属性字典值 |
| `POST /api/ozon/categories/attribute-values/search` | `/v1/description-category/attribute/values/search` | 搜索属性字典值 |
| `POST /api/ozon/products/import` | `/v4/product/info/limit` + `/v3/product/import` | 先查额度，再创建/更新商品，保存任务 |
| `GET /api/ozon/products/import-tasks/{task_id}` | `/v1/product/import/info` | 查询异步任务并回写结果 |
| `POST /api/ozon/products/attributes/update` | `/v1/product/attributes/update` | 仅更新商品属性 |
| `POST /api/ozon/products/pictures/import` | `/v1/product/pictures/import` | 上传或更新商品图片 |
| `POST /api/ozon/products/info/list` | `/v3/product/info/list` | 查询商品信息 |
| `POST /api/ozon/products/info/attributes` | `/v3/products/info/attributes` | 查询商品已填属性 |
| `POST /api/ozon/products/stocks` | `/v2/products/stocks` | 按 `offer_id` 转发设置商品库存 |

## 创建商品示例

```bash
curl -X POST "http://127.0.0.1:8000/api/ozon/products/import" ^
  -H "Client-Id: xxx" ^
  -H "Api-Key: yyy" ^
  -H "Content-Type: application/json" ^
  -d "{\"items\":[{\"offer_id\":\"LOCAL-SKU-001\",\"name\":\"商品名称\",\"description_category_id\":17028922,\"type_id\":91565,\"currency_code\":\"RUB\",\"price\":\"1000\",\"old_price\":\"1100\",\"vat\":\"0.1\",\"depth\":10,\"width\":150,\"height\":250,\"dimension_unit\":\"mm\",\"weight\":100,\"weight_unit\":\"g\",\"images\":[\"https://example.com/image-1.jpg\"],\"attributes\":[]}]}"
```

响应中的 `task_id` 可继续查询：

```bash
curl -X GET "http://127.0.0.1:8000/api/ozon/products/import-tasks/172549793" ^
  -H "Client-Id: xxx" ^
  -H "Api-Key: yyy"
```

## 后台轮询

手动执行一次待处理任务轮询：

```bash
python -m app.workers.poll_import_tasks
```

生产环境可以用计划任务、Supervisor、systemd 或容器定时任务周期性执行该入口。


