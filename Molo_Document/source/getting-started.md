# 快速开始

本页用于在开发机或服务器上启动 FastAPI 版 Molo。只预览页面时只需要 Python 依赖；真正运行分析任务时还需要 R/Conda/renv worker 和 `downstream.yaml` 配置。

以下命令默认从仓库根目录运行。

## 环境要求

| 项目 | 建议 |
| --- | --- |
| 操作系统 | Linux 服务器或 Linux 工作站 |
| Python | 3.12 优先；CI 使用 Python 3.12 |
| R | 与各 `*_renv_project` lockfile 匹配的 R 环境 |
| Redis | 6.2+；生产建议 Redis 7.2 |
| GPU | 可选；空间对齐/整合建议 NVIDIA GPU |
| 内存 | 小数据 8 GB 起步，实际分析建议 32 GB+ |
| 磁盘 | 预留上传、输出、Redis AOF、SQLite WAL 和结果包空间 |

## 安装 Python Web 依赖

```bash
cd Molo_FastAPI
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

开发环境可以使用控制台邮件后端。生产环境必须配置真实 SMTP、HTTPS `PUBLIC_BASE_URL` 和足够长且不同的密钥。

```bash
export APP_ENV=development
export PUBLIC_BASE_URL=http://127.0.0.1:8000
export DOWNLOAD_TOKEN_SECRET=development-download-secret-at-least-32-chars
export EMAIL_VERIFICATION_SECRET=development-email-secret-at-least-32-chars
export MAIL_BACKEND=console
export REDIS_URL=redis://127.0.0.1:6379/0
export CELERY_BROKER_URL=redis://127.0.0.1:6379/0
export CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

## 准备下游配置

复制示例配置并按服务器目录调整。

```bash
cp app/config/downstream.example.yaml app/config/downstream.yaml
```

需要重点检查：

- `project_root`：仓库根目录。
- `molo_source_dir`：`Molo_FastAPI/app/core/R`。
- `default_output_root`：下游结果输出目录，运行用户必须可写。
- `runtime.alignment_default_device` 与 `runtime.alignment_allowed_devices`：允许使用的 GPU。
- `envs.*.rscript`、`envs.*.conda_path`、`envs.*.r_lib`：各 worker 的 R/Conda 路径。
- `workers.*`：对象创建、降维、CellChat、轨迹、ATAC worker 脚本。
- `orchestrators.*`：不同数据类型使用的编排脚本。

## 启动开发服务

至少需要 Redis、FastAPI、Celery worker。为了接近生产行为，建议同时启动 worker 和 beat。

```bash
redis-server --daemonize yes
```

终端 1：

```bash
cd Molo_FastAPI
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

终端 2：

```bash
cd Molo_FastAPI
source .venv/bin/activate
celery -A app.celery_app:celery_app worker \
  -Q analysis,alignment,notifications,packaging,maintenance \
  --loglevel=INFO
```

终端 3：

```bash
cd Molo_FastAPI
source .venv/bin/activate
celery -A app.celery_app:celery_app beat --loglevel=INFO
```

访问：

- 首页：`http://127.0.0.1:8000/`
- 对齐与整合：`http://127.0.0.1:8000/analyse/alignment/`
- Visium 下游分析：`http://127.0.0.1:8000/analyse/downstream/visium`
- 健康检查：`http://127.0.0.1:8000/health/live`、`http://127.0.0.1:8000/health/ready`

## 基础检查

```bash
cd Molo_FastAPI
python -m compileall -q app tests
python -m unittest discover -v
python -m pip check
```

如果只启动 FastAPI 而未启动 Celery，页面可以打开，但提交的分析不会被 worker 消费。若未配置真实 SMTP，开发环境下验证码和结果邮件会输出到控制台邮件后端。
