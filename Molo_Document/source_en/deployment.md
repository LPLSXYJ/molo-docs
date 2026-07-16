# Web Service Deployment

This page describes the public deployment structure for the Molo FastAPI web service. In production, keep source code, runtime environments, configuration files, upload directories, output directories, and log directories separated. Public repositories should only contain source code, example configuration, and deployment templates. Machine-specific paths, secrets, and SMTP credentials should stay on the server.

## Service Components

Recommended production components:

| Service | Queue | Responsibility |
| --- | --- | --- |
| `molo-web` | none | FastAPI pages, verification codes, uploads, status, downloads |
| `molo-celery@analysis` | `analysis` | Downstream analysis |
| `molo-celery@alignment` | `alignment` | Alignment and integration, usually with limited GPU concurrency |
| `molo-celery@notifications` | `notifications` | Verification and result emails |
| `molo-celery@packaging` | `packaging` | Result ZIP packaging |
| `molo-celery@maintenance` | `maintenance` | Queue recovery and expiration cleanup |
| `molo-beat` | none | Periodic maintenance scheduling |
| `molo-redis` | none | Celery broker, result backend, verification code state, and rate-limit state |

## Path Conventions

The examples below use variables for machine directories. Set these variables on the server, or write equivalent paths into systemd units, environment files, and `downstream.yaml`.

```bash
export MOLO_ROOT="<repository-root>"
export MOLO_FASTAPI="$MOLO_ROOT/Molo_FastAPI"
export MOLO_VENV="$MOLO_ROOT/.venv"
export MOLO_ENV_FILE="<runtime-env-file>"
export MOLO_OUTPUT_ROOT="$MOLO_ROOT/outputs/downstream"
```

Do not commit the following to a public repository:

- Production `.env`.
- `Molo_FastAPI/app/config/downstream.yaml`.
- Upload files, result directories, SQLite database, Redis AOF, logs, and download packages.
- SMTP passwords, token secrets, private keys, and certificate private keys.

## Environment Variables

Create a server-local environment file from the example:

```bash
install -m 0600 "$MOLO_FASTAPI/.env.example" "$MOLO_ENV_FILE"
```

Production must configure:

| Variable | Description |
| --- | --- |
| `APP_ENV=production` | Enables production validation |
| `PUBLIC_BASE_URL` | External HTTPS address |
| `DOWNLOAD_TOKEN_SECRET` | At least 32 characters; must differ from verification secret |
| `EMAIL_VERIFICATION_SECRET` | At least 32 characters |
| `JOB_DATABASE_PATH` | SQLite WAL database path |
| `REDIS_URL` | Redis DB 0 |
| `CELERY_BROKER_URL` | Redis DB 0 |
| `CELERY_RESULT_BACKEND` | Redis DB 1 |
| `MAIL_BACKEND=smtp` | Production must not use console/memory |
| `SMTP_*` | SMTP host, port, account, and encryption settings |
| `MAX_UPLOAD_BYTES` | Upload size limit |
| `ANALYSIS_TIME_LIMIT_SECONDS` | Base Celery soft/hard time limit |

Production startup rejects these configurations:

- `PUBLIC_BASE_URL` is not HTTPS.
- Secrets are too short, still `CHANGE_ME`, or both secrets are identical.
- SMTP does not enable TLS/SSL.
- The mail backend is still `console` or `memory`.

## Downstream Configuration

`Molo_FastAPI/app/config/downstream.yaml` is machine-specific and should not be committed to a public repository. Create it from `downstream.example.yaml` and adjust directories to paths available on the server.

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

Path requirements:

- The FastAPI runtime user can read the repository source.
- The runtime user can write to `Molo_FastAPI/data/`, `Molo_FastAPI/plots/`, and `default_output_root`.
- Each `envs.*.rscript` points to the correct Rscript.
- The ATAC `macs2_env` points to an environment containing MACS2.

## Start and Stop Order

Recommended first startup:

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

During releases or shutdowns, stop Web and Beat first, then stop workers so Celery warm shutdown has a chance to wait for active jobs.

```bash
systemctl stop molo-web molo-beat
systemctl stop 'molo-celery@analysis' 'molo-celery@alignment'
systemctl stop 'molo-celery@notifications' 'molo-celery@packaging' 'molo-celery@maintenance'
```

## Nginx

Nginx handles HTTPS termination, upload size limits, reverse proxying, and download endpoint forwarding. The template is:

```text
Molo_FastAPI/deploy/nginx-molo.conf
```

Check these items during deployment:

- `server_name` matches the domain in `PUBLIC_BASE_URL`.
- Certificates and private keys stay only on the server.
- `client_max_body_size` is no smaller than `MAX_UPLOAD_BYTES`.
- `/results/download/`, `/jobs/`, `/analyse/`, and `/api/` are all proxied to FastAPI.
- WebSocket or long-polling headers from the template are preserved.

## Runtime Monitoring

```bash
curl --fail "$PUBLIC_BASE_URL/health/live"
curl --fail "$PUBLIC_BASE_URL/health/ready"
redis-cli ping
"$MOLO_VENV/bin/celery" -A app.celery_app:celery_app inspect ping
"$MOLO_VENV/bin/celery" -A app.celery_app:celery_app inspect active
journalctl -u 'molo-*' --since today
df -h "$MOLO_FASTAPI/data"
```

Recommended alert items:

- Readiness failure.
- Redis AOF errors.
- Missing worker heartbeat.
- Reserved queue keeps growing.
- Abnormal analysis failure rate.
- Packaging failure.
- SMTP rejection or retry spike.
- Insufficient disk space.

## Release Checks

Before release, run:

```bash
cd "$MOLO_FASTAPI"
python -m compileall -q app tests
python -m unittest discover -v
python -m pip check
```

After the public site is reachable, check:

```bash
curl --fail "$PUBLIC_BASE_URL/health/live"
curl --fail "$PUBLIC_BASE_URL/health/ready"
```
