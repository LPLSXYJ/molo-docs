# Web 服务部署

本页说明 Molo FastAPI Web 服务的公网部署结构。生产环境建议把源码、运行环境、配置文件、上传目录、输出目录和日志目录分开管理；公开仓库只提交源码、示例配置和部署模板，机器相关路径、密钥和 SMTP 凭据保留在服务器本地。

## 服务组成

生产部署推荐组件：

| 服务 | 队列 | 职责 |
| --- | --- | --- |
| `molo-web` | 无 | FastAPI 页面、验证码、上传、状态、下载 |
| `molo-celery@analysis` | `analysis` | 下游分析 |
| `molo-celery@alignment` | `alignment` | 对齐与整合，通常限制 GPU 并发 |
| `molo-celery@notifications` | `notifications` | 验证码和结果邮件 |
| `molo-celery@packaging` | `packaging` | 结果 ZIP 打包 |
| `molo-celery@maintenance` | `maintenance` | 队列恢复和过期清理 |
| `molo-beat` | 无 | 周期性调度维护任务 |
| `molo-redis` | 无 | Celery broker、result backend、验证码和限流状态 |

## 路径约定

以下示例使用变量表示机器目录。部署时在服务器上设置这些变量，或把等价路径写入 systemd 单元文件、环境文件和 `downstream.yaml`。

```bash
export MOLO_ROOT="<repository-root>"
export MOLO_FASTAPI="$MOLO_ROOT/Molo_FastAPI"
export MOLO_VENV="$MOLO_ROOT/.venv"
export MOLO_ENV_FILE="<runtime-env-file>"
export MOLO_OUTPUT_ROOT="$MOLO_ROOT/outputs/downstream"
```

公开仓库中不要提交以下内容：

- 生产环境 `.env`。
- `Molo_FastAPI/app/config/downstream.yaml`。
- 上传文件、结果目录、SQLite 数据库、Redis AOF、日志和下载包。
- SMTP 密码、token secret、私钥、证书私钥。

## 环境变量

从示例文件创建服务器本地环境文件：

```bash
install -m 0600 "$MOLO_FASTAPI/.env.example" "$MOLO_ENV_FILE"
```

生产环境必须配置：

| 变量 | 说明 |
| --- | --- |
| `APP_ENV=production` | 启用生产校验 |
| `PUBLIC_BASE_URL` | 外部 HTTPS 地址 |
| `DOWNLOAD_TOKEN_SECRET` | 至少 32 字符，不能与验证码 secret 相同 |
| `EMAIL_VERIFICATION_SECRET` | 至少 32 字符 |
| `JOB_DATABASE_PATH` | SQLite WAL 数据库路径 |
| `REDIS_URL` | Redis DB 0 |
| `CELERY_BROKER_URL` | Redis DB 0 |
| `CELERY_RESULT_BACKEND` | Redis DB 1 |
| `MAIL_BACKEND=smtp` | 生产环境不能使用 console/memory |
| `SMTP_*` | SMTP 主机、端口、账号、加密方式 |
| `MAX_UPLOAD_BYTES` | 上传大小限制 |
| `ANALYSIS_TIME_LIMIT_SECONDS` | Celery soft/hard time limit 基准 |

生产启动时会拒绝以下配置：

- `PUBLIC_BASE_URL` 不是 HTTPS。
- secret 过短、仍是 `CHANGE_ME`、或两个 secret 相同。
- SMTP 未启用 TLS/SSL。
- 邮件后端仍是 `console` 或 `memory`。

## 下游配置

`Molo_FastAPI/app/config/downstream.yaml` 是机器相关配置，不应提交到公共仓库。基于 `downstream.example.yaml` 创建服务器本地配置，并把目录改成该服务器可访问的位置。

```yaml
project_root: "<repository-root>"
molo_source_dir: "<repository-root>/Molo_FastAPI/app/core/R"
default_output_root: "<output-root>"

runtime:
  downstream_retention_hours: 48
  cleanup_interval_minutes: 30
  max_concurrent_jobs: 3
  alignment_default_device: "cuda:0"
  alignment_allowed_devices:
    - "cuda:0"
```

路径要求：

- FastAPI 运行用户可读仓库源码。
- 运行用户可写 `Molo_FastAPI/data/`、`Molo_FastAPI/plots/` 和 `default_output_root`。
- 各 `envs.*.rscript` 指向正确的 Rscript。
- ATAC 的 `macs2_env` 指向包含 MACS2 的环境。

## 启停顺序

首次启动建议：

```bash
systemctl start molo-redis
cd "$MOLO_FASTAPI"
"$MOLO_VENV/bin/python" -c 'from app.services.job_repository import get_repository; get_repository()'
systemctl start molo-celery@analysis molo-celery@alignment
systemctl start molo-celery@notifications molo-celery@packaging molo-celery@maintenance
systemctl start molo-beat
systemctl start molo-web
systemctl enable molo.target
```

发布或停机时，先停止 Web 和 Beat，再停止 worker，使 Celery warm shutdown 有机会等待活跃任务结束。

```bash
systemctl stop molo-web molo-beat
systemctl stop 'molo-celery@analysis' 'molo-celery@alignment'
systemctl stop 'molo-celery@notifications' 'molo-celery@packaging' 'molo-celery@maintenance'
```

## Nginx

Nginx 负责 HTTPS 终止、上传大小限制、反向代理和下载接口转发。模板位于：

```text
Molo_FastAPI/deploy/nginx-molo.conf
```

部署时需要检查：

- `server_name` 与 `PUBLIC_BASE_URL` 的域名一致。
- 证书和私钥只保存在服务器本地。
- `client_max_body_size` 不小于 `MAX_UPLOAD_BYTES`。
- `/results/download/`、`/jobs/`、`/analyse/`、`/api/` 都转发到 FastAPI。
- WebSocket 或长轮询相关头部按模板保留。

## 运行监控

```bash
curl --fail "$PUBLIC_BASE_URL/health/live"
curl --fail "$PUBLIC_BASE_URL/health/ready"
redis-cli ping
"$MOLO_VENV/bin/celery" -A app.celery_app:celery_app inspect ping
"$MOLO_VENV/bin/celery" -A app.celery_app:celery_app inspect active
journalctl -u 'molo-*' --since today
df -h "$MOLO_FASTAPI/data"
```

建议告警项：

- readiness failure。
- Redis AOF 错误。
- worker heartbeat 缺失。
- reserved queue 持续增长。
- 分析失败率异常。
- 打包失败。
- SMTP 拒信或重试激增。
- 磁盘空间不足。

## 发布检查

发布前建议执行：

```bash
cd "$MOLO_FASTAPI"
python -m compileall -q app tests
python -m unittest discover -v
python -m pip check
```

公网可访问后检查：

```bash
curl --fail "$PUBLIC_BASE_URL/health/live"
curl --fail "$PUBLIC_BASE_URL/health/ready"
```
