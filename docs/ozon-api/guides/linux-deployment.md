# Linux 部署文档

本文说明如何在 Linux 服务器上部署 `ozon-api-service` 小服务。推荐使用 Docker Compose 部署。

## 1. 推荐环境

| 项 | 推荐 |
| --- | --- |
| 系统 | Ubuntu 22.04 / Ubuntu 24.04 / Debian 12 / CentOS Stream 9 |
| 部署方式 | Docker + Docker Compose |
| 服务端口 | `8000` |
| 运行入口 | `gunicorn + uvicorn worker` |
| 配置文件 | `.env` |

服务启动后对外接口示例：

```text
http://服务器IP:8000/api/health
```

## 2. 安装 Docker

Ubuntu / Debian 示例：

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

验证：

```bash
docker --version
docker compose version
```

## 3. 上传项目

示例目录：

```bash
mkdir -p /opt/ozon-api-service
```

把项目上传到：

```text
/opt/ozon-api-service
```

目录中至少应包含：

```text
app/
requirements.txt
Dockerfile
docker-compose.yml
.env
```

## 4. 配置 .env

如果服务器上还没有 `.env`：

```bash
cp .env.example .env
```

编辑：

```bash
nano .env
```

示例：

```text
APP_NAME=ozon-api-service
APP_ENV=prod

MYSQL_HOST=182.92.251.60
MYSQL_PORT=13306
MYSQL_DATABASE=ozon-service
MYSQL_USER=root
MYSQL_PASSWORD=你的密码

REDIS_HOST=182.92.251.60
REDIS_PORT=6379
REDIS_DB=3
REDIS_PASSWORD=你的密码

OZON_BASE_URL=https://api-seller.ozon.ru
OZON_CREDENTIAL_TTL_SECONDS=3600
OZON_CATEGORY_TREE_TTL_SECONDS=86400
OZON_CATEGORY_ATTRIBUTES_TTL_SECONDS=43200
OZON_ATTRIBUTE_VALUES_TTL_SECONDS=21600
```

注意：

- 如果 MySQL / Redis 是远程服务器，直接写远程 IP。
- 如果 MySQL / Redis 也在同一个 Docker Compose 中，`MYSQL_HOST` / `REDIS_HOST` 要写服务名，不要写 `127.0.0.1`。
- 如果 MySQL / Redis 在宿主机上，容器里的 `127.0.0.1` 指的是容器自己，不是宿主机。

## 5. 启动服务

进入项目目录：

```bash
cd /opt/ozon-api-service
```

构建并启动：

```bash
docker compose up -d --build
```

查看状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs -f ozon-api
```

## 6. 健康检查

在服务器本机测试：

```bash
curl http://127.0.0.1:8000/api/health
```

正常响应：

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

从外部机器访问：

```bash
curl http://服务器IP:8000/api/health
```

如果外部访问失败，检查安全组和防火墙是否放行 `8000` 端口。

## 7. 测试 Ozon 网络

在 Linux 服务器上执行：

```bash
curl -I https://api-seller.ozon.ru
```

或者：

```bash
curl -v https://api-seller.ozon.ru
```

如果能看到 `Connected to api-seller.ozon.ru` 或 HTTPS 响应头，说明服务器可以访问 Ozon。

## 8. 更新服务

上传新代码后：

```bash
cd /opt/ozon-api-service
docker compose up -d --build
```

重启：

```bash
docker compose restart ozon-api
```

停止：

```bash
docker compose down
```

## 9. 常见问题

### 9.1 容器启动后访问不到

检查容器状态：

```bash
docker compose ps
docker compose logs -f ozon-api
```

检查端口：

```bash
ss -lntp | grep 8000
```

### 9.2 连不上 MySQL

进入服务器测试：

```bash
nc -vz MYSQL_HOST MYSQL_PORT
```

示例：

```bash
nc -vz 182.92.251.60 13306
```

如果不通，检查：

- MySQL 安全组或防火墙
- MySQL 用户是否允许当前服务器 IP 访问
- `.env` 中端口是否正确

### 9.3 连不上 Redis

测试端口：

```bash
nc -vz REDIS_HOST REDIS_PORT
```

如果 Redis 有密码，确认 `.env` 中 `REDIS_PASSWORD` 正确。

### 9.4 修改 .env 不生效

修改 `.env` 后需要重启容器：

```bash
docker compose restart ozon-api
```

如果镜像里有代码变更，使用：

```bash
docker compose up -d --build
```

### 9.5 查看容器内环境变量

```bash
docker compose exec ozon-api env | grep -E "MYSQL|REDIS|OZON"
```

### 9.6 Permission denied: /app/app/__init__.py

如果日志出现：

```text
PermissionError: [Errno 13] Permission denied: '/app/app/__init__.py'
```

说明容器内运行用户没有读取代码文件的权限。当前 Dockerfile 已通过 `COPY --chown=appuser:appuser` 和 `chmod -R a+rX /app` 处理。

更新 Dockerfile 后重新构建：

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 10. Nginx 可选代理

如果希望通过 `80` 端口访问，可以在服务器安装 Nginx。

示例配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

重载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

访问：

```text
http://your-domain.com/api/health
```
