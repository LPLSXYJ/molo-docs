# 数据准备

Molo Web 支持上传 zip 或填写服务器可访问的数据目录。上传 zip 时，压缩包内部建议只有一个顶层数据目录；服务器目录必须能被运行 FastAPI/Celery 的进程读取。

!!! warning "文件命名"
    本页列出的文件名来自 `Molo_Create`、对齐 wrapper 和 Web worker。准备数据时请以这里的目录结构为准。

## Web 下游分析输入

| 数据类型 | Web 路径 | 读取方式 | 推荐目录内容 |
| --- | --- | --- | --- |
| 10X Visium | `/analyse/downstream/visium` | `Seurat::Load10X_Spatial()` | `filtered_feature_bc_matrix.h5` 与 `spatial/` |
| Slide-seq | `/analyse/downstream/slideseq` | `counts.*.gz` + `spatial.csv(.gz)` | `counts.csv.gz`/`counts.tsv.gz`/`counts.txt.gz`，`spatial.csv` 或 `spatial.csv.gz` |
| Vizgen MERFISH | `/analyse/downstream/merfish` | `Seurat::LoadVizgen()` | Vizgen 标准输出目录，如 `cell_by_gene.csv`、细胞边界/元数据文件 |
| Nanostring CosMx | `/analyse/downstream/cosmx` | `Seurat::LoadNanostring()` | CosMx 平台输出的表达矩阵、metadata、FOV、polygon、transcript 等文件 |
| Akoya CODEX | `/analyse/downstream/codex` | `LoadAkoya()` | `codex.csv` |
| 10X Xenium | `/analyse/downstream/xenium` | `Seurat::LoadXenium()` | Xenium 标准输出目录，如 `cell_feature_matrix.h5`、cells、transcripts、boundaries 文件 |
| Stereo-seq | `/analyse/downstream/stereoseq` | `SeuratDisk` + `rhdf5` | `stereo_seq.h5ad`，其中包含 `obsm/spatial` 与 `obs/cell_name` |
| spatial ATAC-seq | `/analyse/downstream/atac` | ArchR/Signac worker | `fragments.tsv.gz`、`fragments.tsv.gz.tbi` 与 `spatial/` |

### Visium

```text
visium_sample/
  filtered_feature_bc_matrix.h5
  spatial/
    scalefactors_json.json
    tissue_lowres_image.png
    tissue_hires_image.png
    tissue_positions.csv            # 或 tissue_positions_list.csv
    aligned_fiducials.jpg
    detected_tissue_image.jpg
```

### Slide-seq

```text
slideseq_sample/
  counts.csv.gz        # 或 counts.tsv.gz / counts.txt.gz
  spatial.csv.gz       # 或 spatial.csv
```

`counts` 文件第一列应为 feature/gene ID，其余列为 beads/cells。`spatial.csv` 使用 Seurat `ReadSlideSeq()` 可读取的坐标格式。

### MERFISH

```text
merfish_sample/
  cell_by_gene.csv
  cell_metadata.csv
  cell_boundaries/
    feature_data_0.hdf5
    feature_data_1.hdf5
```

实际目录以 Vizgen 标准输出为准，能够被 `Seurat::LoadVizgen(data.dir=...)` 读取即可。

### CosMx

```text
cosmx_sample/
  *_exprMat_file.csv
  *_metadata_file.csv
  *_fov_positions_file.csv
  *-polygons.csv
  *_tx_file.csv
```

实际目录以 `Seurat::LoadNanostring(data.dir=...)` 支持的 CosMx 输出为准。

### Xenium

```text
xenium_sample/
  cell_feature_matrix.h5
  cells.csv.gz
  transcripts.csv.gz
  cell_boundaries.csv.gz
  nucleus_boundaries.csv.gz
```

实际目录以 10X Xenium Explorer/Onboard Analysis 输出为准，能够被 `Seurat::LoadXenium()` 读取即可。

### Stereo-seq

```text
stereoseq_sample/
  stereo_seq.h5ad
```

worker 会读取：

- `obsm/spatial`：空间坐标。
- `obs/cell_name`：细胞/spot 名称。

### spatial ATAC-seq

```text
atac_sample/
  fragments.tsv.gz
  fragments.tsv.gz.tbi
  spatial/
    scalefactors_json.json
    tissue_lowres_image.png
    tissue_positions_list.csv
```

ATAC worker 会为 `fragments.tsv.gz` 构建或复用 ArchR ArrowFiles，并在输入目录的 `tmp/web_arrow_cache/` 下维护缓存。服务器部署时要保证该目录可写。

## 对齐与整合输入

网页对齐与整合页面支持上传文件/文件夹或填写服务器路径。服务器路径可以是父目录，也可以是用英文逗号分隔的样本目录列表。

```text
alignment_parent/
  slice_1/
    filtered_feature_bc_matrix.h5
    spatial/
    truth.txt        # 推荐，不是所有场景都强制
  slice_2/
    filtered_feature_bc_matrix.h5
    spatial/
    truth.txt
```

`truth.txt` 推荐使用两列、制表符分隔：

```text
barcode_1    CellTypeA
barcode_2    CellTypeB
```

当存在 `truth.txt` 时，wrapper 会把标签写入 `cell_type_truth`。当没有 `truth.txt` 时，wrapper 会先运行 SCTransform/PCA/UMAP/聚类，并用聚类标签补充元数据。

## Python 核心整合输入

直接运行 `Molo_FastAPI/app/core/python/main_process.py` 时，输入目录需要提前整理成 Molo parquet 格式。Python 双编码器逻辑要求正好两个 batch。

```text
molo_input/
  Molo1/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
    image.png          # 可选
  Molo2/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
    image.png          # 可选
```

文件要求：

- `Count.parquet`：原始或计数矩阵，每行一个 cell/spot，每列一个 feature，必须有 `cells` 列。
- `SCT.parquet`：归一化/筛选后的特征矩阵，结构同 `Count.parquet`。
- `spatial.parquet`：至少包含两列空间坐标，保存流程使用 `x`、`y`。
- `meta.parquet`：细胞元数据，行顺序需要与矩阵一致。

## Custom 数据

下游 `Custom` 对象创建没有独立页面，但 `Molo_Create(data_type="Custom")` 支持以下文件。若需要通过自定义数据进入 Web，可以先转换为支持的平台目录，或由开发者补充自定义页面。

```text
custom_sample/
  matrix.parquet      # 必需
  embedding.parquet   # 可选
  umap.parquet        # 可选
  meta.csv            # 可选
  spatial.csv         # 可选
```

`matrix.parquet` 每行一个细胞、每列一个 feature，并包含 `__index_level_0__` 作为 cell ID。`meta.csv` 可包含 `GroundTruth`、`Prediction`、`Batch`。`spatial.csv` 可使用 `x,y` 两列，或 `barcodes,xcoord,ycoord` 三列。
