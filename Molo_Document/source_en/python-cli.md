# Python CLI

Molo provides a Python command-line entry point for developers who want to run the core pairwise integration algorithm directly, benchmark methods, or bypass the web form for batch processing.

## Core Entry Point

```text
Molo_FastAPI/app/core/python/main_process.py
```

This entry point reads a preformatted parquet input directory, runs spatial alignment, graph construction, dual-encoder training, UMAP/iLISI calculation, and result saving.

!!! warning "Runtime limitation"
    The dual-encoder logic in `main_process.py` requires exactly two batches. If the input directory does not contain exactly two samples, it raises a batch-count error.

## Input Directory

```text
molo_input/
  Molo1/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
  Molo2/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
```

Matrix parquet files must include a `cells` column. The row order of `spatial.parquet` and `meta.parquet` must match the matrices.

## Example Run

```bash
cd <repository-root>
conda activate Molo

python -u Molo_FastAPI/app/core/python/main_process.py \
  -data_path examples/molo_input \
  -save_path outputs/molo_output \
  -device cuda:0 \
  -sp_alignment Molo \
  -pre_train_epoch 100 \
  -train_epoch 300 \
  -compute_iLISI 1 \
  -use_harmony 0 \
  -edge_sp 10 \
  -edge_mtx 10 \
  -h_dims 250 \
  -r_dims 30 \
  -shared_dims 20 \
  -sample_size 512
```

Run spatial alignment only without training the integration model:

```bash
python -u Molo_FastAPI/app/core/python/main_process.py \
  -data_path examples/molo_input \
  -save_path outputs/alignment_output \
  -device cuda:0 \
  -sp_alignment Molo \
  -alignment_only 1
```

## Common Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `-data_path` | required | Input parent directory |
| `-save_path` | required | Output directory |
| `-device` | `cuda:1` | PyTorch device; automatically falls back to CPU when CUDA is unavailable |
| `-sp_alignment` | `Molo` | Spatial alignment method |
| `-pre_train_epoch` | `200` | Number of pretraining epochs; the main workflow primarily uses the training phase |
| `-train_epoch` | `600` | Number of training epochs |
| `-compute_iLISI` | `0` | Whether to compute iLISI |
| `-alignment_only` | `0` | Whether to run spatial alignment only |
| `-edge_type` | `together` | Graph edge source: `spatial`, `count`, or `together` |
| `-edge_sp` | `10` | Number of spatial KNN neighbors |
| `-edge_mtx` | `10` | Number of expression-matrix KNN neighbors |
| `-h_dims` | `250` | Hidden dimension |
| `-r_dims` | `30` | Latent dimension |
| `-shared_dims` | `20` | Shared latent dimension; must be smaller than `-r_dims` |
| `-sample_size` | `512` | Sample count used by the sampling loss |

## Output Files

```text
molo_output/
  matrix.parquet
  embedding.parquet
  umap.parquet
  spatial.csv
  meta.csv
  alignment_info.txt
  Molo_Alignment_3D.png
  Raw_Alignment_3D.png
  iLISI.txt
  ilisi_values.csv
  Molo1/
    matrix.parquet
    embedding.parquet
    umap.parquet
    spatial.csv
    meta.csv
  Molo2/
    ...
```

The actual files depend on `-sp_alignment`, `-alignment_only`, and whether metrics are computed.

## Prepare Parquet Files from AnnData

The example below converts two `.h5ad` files into the format required by the Molo Python CLI. Adjust `batch_name`, spatial coordinates, and normalized matrix source according to your data.

```python
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc
import scipy.sparse as sp


def _dense(matrix):
    return matrix.toarray() if sp.issparse(matrix) else np.asarray(matrix)


def write_sample(adata, out_dir: Path, layer=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    genes = list(map(str, adata.var_names))
    cells = list(map(str, adata.obs_names))

    count_matrix = adata.layers[layer] if layer else adata.X
    count = pd.DataFrame(_dense(count_matrix), columns=genes)
    count["cells"] = cells
    count.to_parquet(out_dir / "Count.parquet", index=False)

    sct = pd.DataFrame(_dense(adata.X), columns=genes)
    sct["cells"] = cells
    sct.to_parquet(out_dir / "SCT.parquet", index=False)

    spatial = pd.DataFrame(adata.obsm["spatial"], columns=["x", "y"])
    spatial.to_parquet(out_dir / "spatial.parquet", index=False)

    meta = adata.obs.reset_index(names="cell_id")
    meta.to_parquet(out_dir / "meta.parquet", index=False)


root = Path("molo_input")
write_sample(sc.read_h5ad("sample_1.h5ad"), root / "Molo1")
write_sample(sc.read_h5ad("sample_2.h5ad"), root / "Molo2")
```

## AD/Normal Benchmark Script

The repository `Integrate/` directory provides an AD/Normal benchmark, including comparison workflows for Original, Harmony, Seurat, STAligner, and Molo.

```bash
cd <repository-root>
conda activate Molo
python -u Integrate/run_molo_ad_normal.py \
  --cache-dir Integrate/results/AD_and_Normal/cache \
  --output-dir Integrate/results/AD_and_Normal/Molo \
  --device cuda:0
```

For the complete benchmark notes, see `Integrate/README_AD_Normal_benchmark.md`.
