# Docker 部署说明

本文说明如何把 Ozon API 服务作为 Docker 小服务部署。

如果是在 Linux 服务器上部署，可同时参考 [Linux 部署文档](./linux-deployment.md)。

## 文件结构

项目根目录新增：

```text
Dockerfile
docker-compose.yml
.dockerignore
```

`.env` 只在运行时由 `docker compose` 读取，不会被打进镜像。

## 构建并启动

```bash
docker compose up -d --build
```

查看日志：

```bash
docker compose logs -f ozon-api
```

健康检查：

```bash
curl http://127.0.0.1:8000/api/health
```

正常返回：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "status": "ok",
    "service": "ozon-api-service"
  }
}
```

## 配置说明

运行前确认 `.env` 中的配置是目标环境可访问的地址：

```text
MYSQL_HOST=182.92.251.60
MYSQL_PORT=13306
MYSQL_DATABASE=ozon-service
MYSQL_USER=root
MYSQL_PASSWORD=******

REDIS_HOST=182.92.251.60
REDIS_PORT=6379
REDIS_DB=3
REDIS_PASSWORD=******
```

如果 MySQL 或 Redis 在同一个 `docker-compose.yml` 里，`MYSQL_HOST` 和 `REDIS_HOST` 应该写服务名，例如 `mysql`、`redis`。

如果 MySQL 或 Redis 在 Linux 宿主机上，容器内的 `127.0.0.1` 指的是容器自己，不是宿主机；建议改用宿主机内网 IP。

## 常用命令

停止服务：

```bash
docker compose down
```

重启服务：

```bash
docker compose restart ozon-api
```

重新构建：

```bash
docker compose up -d --build
```

查看容器状态：

```bash
docker compose ps
```
