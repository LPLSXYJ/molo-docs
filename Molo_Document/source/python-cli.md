# Python 命令行

Molo 提供 Python 命令行入口，适合开发者直接运行核心 pairwise 整合算法、做基准实验或绕过 Web 表单进行批处理。

## 核心入口

```text
Molo_FastAPI/app/core/python/main_process.py
```

该入口读取预先准备好的 parquet 输入目录，运行空间对齐、图构建、双编码器训练、UMAP/iLISI 计算和结果保存。

!!! warning "运行限制"
    `main_process.py` 的双编码器逻辑要求正好两个 batch。若输入目录下不是两个样本，会报出 batch 数量错误。

## 输入目录

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

矩阵 parquet 需要包含 `cells` 列。`spatial.parquet` 与 `meta.parquet` 的行顺序要和矩阵一致。

## 运行示例

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

只做空间对齐、不训练整合模型：

```bash
python -u Molo_FastAPI/app/core/python/main_process.py \
  -data_path examples/molo_input \
  -save_path outputs/alignment_output \
  -device cuda:0 \
  -sp_alignment Molo \
  -alignment_only 1
```

## 常用参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `-data_path` | 必填 | 输入父目录 |
| `-save_path` | 必填 | 输出目录 |
| `-device` | `cuda:1` | PyTorch 设备；无 CUDA 时自动使用 CPU |
| `-sp_alignment` | `Molo` | 空间对齐方法 |
| `-pre_train_epoch` | `200` | 预训练轮数；主流程主要使用训练阶段 |
| `-train_epoch` | `600` | 训练轮数 |
| `-compute_iLISI` | `0` | 是否计算 iLISI |
| `-alignment_only` | `0` | 是否只运行空间对齐 |
| `-edge_type` | `together` | 图边来源：`spatial`、`count` 或 `together` |
| `-edge_sp` | `10` | 空间 KNN 邻居数 |
| `-edge_mtx` | `10` | 表达矩阵 KNN 邻居数 |
| `-h_dims` | `250` | 隐藏层维度 |
| `-r_dims` | `30` | 潜空间维度 |
| `-shared_dims` | `20` | 共享潜空间维度，必须小于 `-r_dims` |
| `-sample_size` | `512` | 采样损失使用的样本数 |

## 输出文件

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

实际文件取决于 `-sp_alignment`、`-alignment_only` 和是否计算指标。

## 从 AnnData 准备 parquet

下面示例将两个 `.h5ad` 文件转换为 Molo Python CLI 所需格式。请按自己的数据列名调整 `batch_name`、空间坐标和归一化矩阵来源。

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

## AD/Normal 基准脚本

仓库中的 `Integrate/` 目录提供了 AD/Normal benchmark，包含 Original、Harmony、Seurat、STAligner 和 Molo 的比较流程。

```bash
cd <repository-root>
conda activate Molo
python -u Integrate/run_molo_ad_normal.py \
  --cache-dir Integrate/results/AD_and_Normal/cache \
  --output-dir Integrate/results/AD_and_Normal/Molo \
  --device cuda:0
```

更完整的 benchmark 说明见 `Integrate/README_AD_Normal_benchmark.md`。
