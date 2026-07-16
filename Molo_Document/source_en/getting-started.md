# Getting Started

This page explains how to start the FastAPI version of Molo on a development machine or server. If you only want to preview pages, Python dependencies are enough. To run real analysis jobs, you also need the R/Conda/renv workers and a `downstream.yaml` configuration.

The commands below assume that you are running them from the repository root.

## Requirements

| Item | Recommendation |
| --- | --- |
| Operating system | Linux server or Linux workstation |
| Python | Python 3.12 preferred; CI uses Python 3.12 |
| R | An R environment matching each `*_renv_project` lockfile |
| Redis | 6.2+; Redis 7.2 recommended for production |
| GPU | Optional; NVIDIA GPU recommended for spatial alignment/integration |
| Memory | 8 GB minimum for small data; 32 GB+ recommended for real analysis |
| Disk | Reserve space for uploads, outputs, Redis AOF, SQLite WAL, and result packages |

## Install Python Web Dependencies

```bash
cd Molo_FastAPI
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For development, you can use the console mail backend. Production must use a real SMTP service, an HTTPS `PUBLIC_BASE_URL`, and long, distinct secrets.

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

## Prepare Downstream Configuration

Copy the example configuration and adjust it to the server directories.

```bash
cp app/config/downstream.example.yaml app/config/downstream.yaml
```

Pay special attention to:

- `project_root`: repository root directory.
- `molo_source_dir`: `Molo_FastAPI/app/core/R`.
- `default_output_root`: downstream result output directory; the runtime user must be able to write to it.
- `runtime.alignment_default_device` and `runtime.alignment_allowed_devices`: GPUs allowed for use.
- `envs.*.rscript`, `envs.*.conda_path`, `envs.*.r_lib`: R/Conda paths for each worker.
- `workers.*`: worker scripts for object creation, dimensionality reduction, CellChat, trajectory, and ATAC.
- `orchestrators.*`: orchestration scripts for different data types.

## Start the Development Service

At minimum, Redis, FastAPI, and a Celery worker are required. To match production behavior more closely, start both worker and beat.

```bash
redis-server --daemonize yes
```

Terminal 1:

```bash
cd Molo_FastAPI
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
cd Molo_FastAPI
source .venv/bin/activate
celery -A app.celery_app:celery_app worker \
  -Q analysis,alignment,notifications,packaging,maintenance \
  --loglevel=INFO
```

Terminal 3:

```bash
cd Molo_FastAPI
source .venv/bin/activate
celery -A app.celery_app:celery_app beat --loglevel=INFO
```

Open:

- Home: `http://127.0.0.1:8000/`
- Alignment and integration: `http://127.0.0.1:8000/analyse/alignment/`
- Visium downstream analysis: `http://127.0.0.1:8000/analyse/downstream/visium`
- Health checks: `http://127.0.0.1:8000/health/live`, `http://127.0.0.1:8000/health/ready`

## Basic Checks

```bash
cd Molo_FastAPI
python -m compileall -q app tests
python -m unittest discover -v
python -m pip check
```

If only FastAPI is running and Celery is not running, pages can be opened, but submitted analyses will not be consumed by workers. If real SMTP is not configured, verification codes and result emails are written to the console mail backend in development.
