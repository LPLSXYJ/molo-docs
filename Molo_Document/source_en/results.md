# Result Files

Molo results fall into three categories: alignment/integration outputs, downstream analysis outputs, and email download packages. The web page only shows selected preview figures. Complete results are delivered through the download package.

## Alignment and Integration Results

The working directory for an alignment job is:

```text
Molo_FastAPI/data/tasks/{job_id}/
```

Core results are stored in:

```text
Molo_FastAPI/data/tasks/{job_id}/results/
```

Common files:

| File | Description |
| --- | --- |
| `Raw_Alignment_3D.png/.pdf` | 3D preview of original coordinates |
| `Molo_Alignment_3D.png/.pdf` | 3D preview after Molo alignment |
| `matrix.parquet` | Reconstructed or integrated expression matrix |
| `embedding.parquet` | Low-dimensional representation |
| `umap.parquet` | UMAP coordinates |
| `spatial.csv` | Aligned spatial coordinates |
| `meta.csv` | Merged metadata |
| `integrated_molo.rds` | Integrated Molo object |
| `alignment_info.txt` | Summary of spatial alignment method and parameters |

The web service copies selected images to:

```text
Molo_FastAPI/plots/tmp/{job_id}/
```

for page previews.

## Downstream Analysis Results

The downstream analysis output root is controlled by `app/config/downstream.yaml`:

```yaml
default_output_root: "outputs/downstream"
```

Single-job directory:

```text
outputs/downstream/{job_id}/
  config.json
  manifest.json
  logs/
  intermediate/
  plots/
```

| Directory/File | Description |
| --- | --- |
| `manifest.json` | Job stage status and previewable artifact list |
| `logs/orchestrator.log` | Orchestration log; not included in user download packages |
| `intermediate/*.rds` | Intermediate Molo objects passed between workers |
| `plots/*.png`, `plots/*.pdf` | Main figures shown in the page preview and included in download packages |

### Manifest Example

```json
{
  "job_id": "00000000-0000-0000-0000-000000000000",
  "status": "completed",
  "stages": {
    "creation": "completed",
    "reduction": "completed",
    "go": "completed"
  },
  "artifacts": {
    "reduction": ["Molo_clusters_UMAP.png"],
    "go": ["Molo_GO_Enrichment/example.png"]
  },
  "error": null
}
```

## Download Package

The packaging job generates:

```text
Molo_FastAPI/data/packages/{job_id}/
```

containing:

```text
molo-results-{job_id}-{sha256}.zip
```

The download package contains:

```text
README.txt
manifest.json
results/
  ...
```

Allowed suffixes in download packages:

```text
.rds .h5ad .parquet .png .pdf .csv .tsv .txt .json
```

The following content is excluded:

- Original uploaded files.
- Internal `config.json`, runtime logs, stdout/stderr, traceback.
- Parameters containing paths, emails, tokens, secrets, passwords, or similar sensitive fields.
- Files with non-allowlisted suffixes.

## Status Fields

Main fields returned by public status APIs:

| Field | Description |
| --- | --- |
| `analysis_status` | `queued`, `running`, `completed`, `failed`, `expired`, and similar states |
| `package_status` | `pending`, `running`, `ready`, `failed`, or `not_applicable` |
| `delivery_status` | `pending`, `sent`, `retrying`, `failed`, `unknown` |
| `progress` | Coarse progress from 0 to 100 |
| `current_stage` | Currently running stage |
| `stages` | Stage status from the downstream manifest |
| `output_available` | Whether the download package is available |
| `retained_until` | Result retention expiration time |

Status troubleshooting priority:

1. `analysis_status=failed`: first check the worker log for the corresponding task and Job ID.
2. `analysis_status=completed` but `package_status=failed`: check the packaging worker.
3. `package_status=ready` but `delivery_status=failed`: check SMTP and the resend API.
4. `status=expired`: results have been removed according to the retention policy and must be regenerated.
