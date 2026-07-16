# Web Workflow

The web entry point is provided by FastAPI, and all analysis jobs are sent to Celery queues. Before submitting a job, users must enter a result email address and a one-time 6-digit verification code. After submission, the page can be closed; results are downloaded through a secure link sent by email.

## Alignment and Integration

Entry point:

```text
/analyse/alignment/
```

The page contains two workspaces.

### Multi-Slice Alignment

Purpose: spatially align multiple slices only, without full expression integration.

Form fields:

| Field | Description |
| --- | --- |
| Input Source | `Upload Files` or `Server Path` |
| Upload Slices | Upload a folder or zip containing multiple samples |
| Server Path(s) | Parent directory or comma-separated sample directories |
| Data Type | Visium, Xenium, Stereo-seq, Slide-seq, MerFISH, CosMx, CODEX, Custom |
| Result email | Email address for verification code and result email |

The default spatial alignment method is Molo OT/PFGW. Keeping `truth.txt` in each slice directory improves label and evaluation completeness.

### Pairwise Alignment & Integration

Purpose: spatial alignment, expression integration, and basic result preview for two samples.

Form fields:

| Field | Description |
| --- | --- |
| Input Source | `Upload Files` or `Server Path` |
| Upload Slices | Select two samples, or a zip/directory containing two samples |
| Data Type (Sample 1/2) | Specify the data type of each sample |
| Alignment Method | `Molo` or `Raw` |
| Result email | Email address for verification code and result email |

The Python core integration logic requires two batches. For more than two samples, use Multi-Slice Alignment or extend the integration logic on the development side.

### Alignment Preview Outputs

After the job completes, the page can display:

- `Raw_Alignment_3D.png`
- `Molo_Alignment_3D.png`
- `umap_batch_celltype_DLPFC.png`, generated only in some integration modes

The complete results are delivered through the email download package.

## Downstream Analysis

Entry template:

```text
/analyse/downstream/{analysis_type}
```

Supported `analysis_type` values:

| Type | Path |
| --- | --- |
| Visium | `/analyse/downstream/visium` |
| ATAC | `/analyse/downstream/atac` |
| Slide-seq | `/analyse/downstream/slideseq` |
| Xenium | `/analyse/downstream/xenium` |
| CosMx | `/analyse/downstream/cosmx` |
| MERFISH | `/analyse/downstream/merfish` |
| CODEX | `/analyse/downstream/codex` |
| Stereo-seq | `/analyse/downstream/stereoseq` |

### Input Sources

| Source | Description |
| --- | --- |
| Upload Local File | Upload one `.zip` containing the complete data directory for the selected data type |
| Server File Path | Enter a data directory accessible to FastAPI/Celery |

The HTTP API can also read input from completed integration jobs, but the web page primarily exposes upload and server-path modes.

### Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| Species | `mouse` | `mouse` or `human`; ATAC maps to mm10/hg38 |
| Clustering Resolution | `0.5` | Seurat clustering resolution |
| Number of Neighbors | `30` | Number of KNN/SNN neighbors |
| Min Features (QC) | Visium `2500`, ATAC `1000` | Minimum feature filter during object creation |

### Analysis Steps

| Step | Web name | Backend stage |
| --- | --- | --- |
| QC | Required | `creation` or `atac_analysis` |
| Clustering | Louvain/Leiden or Dimensionality Reduction | `reduction` |
| GO Enrichment | GO enrichment | `go` |
| Cell Communication | CellChat | `cellchat` |
| Trajectory Inference | Monocle3 | `trajectory` |

GO, CellChat, and Trajectory are optional steps. If data quality or annotation is insufficient, an optional step may produce no valid images. In that case, the job may still complete, but the corresponding gallery can be empty.

## Email Verification Code

Each job submission requires a fresh verification code:

1. Enter an email address.
2. Click `Send code`.
3. Check the 6-digit code.
4. Enter the code and submit the job.

In development, if `MAIL_BACKEND=console` is used, the verification code is written to the service log instead of being sent as a real email.

## Job ID and Recovery

After a successful submission, the page displays the Job ID. Save it immediately for:

- Restoring state after reopening the page.
- Copying the return link.
- Resending the result email after completion.
- Reporting issues to maintainers.

Downstream pages support recovery through `?task_id=<job_id>`. The alignment page also supports entering a Job ID in the upper-right area.

## Result Retention

The default retention window comes from `app/config/downstream.yaml`:

```yaml
runtime:
  downstream_retention_hours: 48
```

After expiration, result directories and download packages are removed by maintenance jobs. The Job ID may still exist in the state database, but output files can no longer be downloaded.
