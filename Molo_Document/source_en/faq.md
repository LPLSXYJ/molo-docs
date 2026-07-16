# FAQ

## Why does the documentation focus on FastAPI Web?

Molo's main user entry points are FastAPI Web, HTTP API, and Python CLI. R is still used by several backend workers, including object creation, dimensionality reduction and clustering, CellChat, Monocle3, and ATAC analysis. If you need to call R functions directly, see [R Function Reference](r-functions.md).

## The page opens, but jobs never start after submission

Usually Celery workers are not running or queues do not match. Check:

```bash
celery -A app.celery_app:celery_app inspect ping
celery -A app.celery_app:celery_app inspect reserved
redis-cli ping
```

Alignment jobs require the `alignment` queue, downstream analysis requires the `analysis` queue, packaging requires the `packaging` queue, and email delivery requires the `notifications` queue.

## I cannot receive the verification code

In development, if `MAIL_BACKEND=console` is used, the verification code only appears in the server log. In production, check:

- `MAIL_BACKEND=smtp`.
- `SMTP_HOST`, `SMTP_PORT`, account, and password are correct.
- `SMTP_USE_TLS` and `SMTP_USE_SSL` are not both true.
- `PUBLIC_BASE_URL` is an externally reachable HTTPS address.
- Redis is available, because verification state is stored in Redis.

## The verification code is correct, but submission fails

Verification codes are one-time codes and expire. The default TTL is:

```bash
EMAIL_VERIFICATION_TTL_SECONDS=600
```

Each analysis job needs a fresh code. If the email address changes, send a new verification code.

## The uploaded zip is reported as invalid

Check:

- Downstream analysis only accepts `.zip` uploads.
- The zip should preferably contain only one top-level data directory.
- Directory file names must match the requirements in [Data Preparation](data-preparation.md).
- The zip must not exceed `MAX_UPLOAD_BYTES`.
- After extraction, it must not contain path traversal, too many files, or an abnormal compression ratio.

## Server path mode cannot find samples

Server paths are paths on the machine running FastAPI/Celery, not paths on the browser user's computer. The alignment page supports a parent directory or comma-separated sample directories. Downstream pages require a single data directory.

## Pairwise integration reports a batch-count error

The dual-encoder logic in `main_process.py` requires two batches. Confirm that the input parent directory contains exactly two sample directories and that, after sorting, they represent the two batches.

## Is `truth.txt` required?

It is not mandatory in every scenario. When `truth.txt` exists, the backend writes labels to `cell_type_truth` and uses them for more complete preview/evaluation outputs. Without `truth.txt`, the wrapper runs basic preprocessing and clustering, then supplements metadata with cluster labels.

## Downstream GO, CellChat, or trajectory has no result figures

These steps depend on clustering, gene annotation, species databases, expression matrix quality, and cell-type labels. A job may complete even when an optional stage does not produce valid images. First check:

- Whether `cluster` was run.
- Whether `species` was selected correctly.
- Whether there are enough marker genes.
- The corresponding stage status in `manifest.json`.
- Whether worker logs include optional-step failure messages.

## The result email was sent, but the link cannot be opened

Possible causes:

- Results have expired.
- `PUBLIC_BASE_URL` is configured incorrectly.
- The token has expired.
- The result package was not built successfully.
- The reverse proxy does not forward `/results/download/{token}` correctly.

Check status first:

```bash
curl https://molo.example.org/jobs/{job_id}
```

Then check packaging and notifications worker logs.

## Documentation build fails

This directory uses MkDocs:

```bash
python -m pip install -r Molo_Document/requirements-docs.txt
mkdocs build -f Molo_Document/mkdocs.yml --strict
mkdocs build -f Molo_Document/mkdocs.en.yml --strict
```

`--strict` treats broken links, missing pages, and configuration errors as failures. After adding a page, update the `nav` section in both MkDocs configuration files.
