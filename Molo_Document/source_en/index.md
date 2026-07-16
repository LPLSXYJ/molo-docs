# Molo Documentation

Molo is an analysis framework for spatial omics data. It covers multi-slice spatial alignment, pairwise expression integration, downstream biological analysis, web-based submission, and asynchronous job management. The web service uses FastAPI, Celery, and Redis to organize jobs. The core integration algorithm also exposes a Python command-line entry point for batch processing and benchmarking.

## Audience

- Laboratory users who want to submit analyses through the web interface.
- Analysts preparing Visium, Xenium, MERFISH, CosMx, Slide-seq, Stereo-seq, spATAC-seq, CODEX, or custom data.
- Maintainers deploying the Molo FastAPI service on a server.
- Developers automating jobs through the Python CLI, R functions, or HTTP API.

## System Architecture

| Layer | Implementation | Main directory |
| --- | --- | --- |
| Web interface | FastAPI, Jinja2, static JS/CSS | `Molo_FastAPI/app/` |
| Task queue | Celery worker, Redis broker/result backend | `Molo_FastAPI/app/celery_app.py` |
| Job state | SQLite WAL, Redis locks, heartbeat and redelivery | `Molo_FastAPI/app/services/` |
| Spatial alignment and integration | Python deep-learning core, R wrappers for object conversion | `Molo_FastAPI/app/core/python/`, `Molo_FastAPI/app/core/R/` |
| Downstream analysis | R workers orchestrated by FastAPI | `Molo_obj_renv_project/`, `reduction_renv_project/`, `cellchat_renv_project/`, `trajectory_renv_project/`, `atac_renv_project/` |
| Deployment | systemd, Nginx, Redis templates | `Molo_FastAPI/deploy/` |

## Feature Overview

- **Spatial alignment**: Supports multi-slice alignment and pairwise alignment. The default path uses Molo OT/PFGW, with Raw mode also available.
- **Expression integration**: The Python core provides a dual-encoder integration workflow for pairwise integration of two batches.
- **Downstream analysis**: Includes QC, dimensionality reduction and clustering, GO enrichment, cell-cell communication, and trajectory inference. ATAC has an independent ArchR/Signac workflow.
- **Web submission**: Upload a zip/folder or use a server path, then track the job by Job ID.
- **Result delivery**: After a job completes, Molo builds a safe result package, sends the download link to a verified email address, and cleans files automatically after the retention window.
- **Functions and APIs**: Provides R function references, Python CLI usage, email verification, job status, result email resend, and health-check APIs.

## Recommended Reading Order

1. [Getting Started](getting-started.md): Start the web service locally and verify dependencies.
2. [Data Preparation](data-preparation.md): Organize input directories by data type.
3. [Web Workflow](web-workflow.md): Submit alignment, integration, and downstream analyses through the web UI.
4. [Python CLI](python-cli.md): Run the core pairwise integration workflow or benchmark scripts directly.
5. [R Function Reference](r-functions.md): Review object creation, dimensionality reduction and clustering, GO, CellChat, trajectory, and integration functions.
6. [Web Service Deployment](deployment.md): Deploy FastAPI, Celery, Redis, and Nginx.
7. [Documentation Site Deployment](documentation-site.md): Publish this documentation to GitHub Pages or ReadTheDocs.
