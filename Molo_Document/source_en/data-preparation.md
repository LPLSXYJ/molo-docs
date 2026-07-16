# Data Preparation

Molo Web supports zip uploads and server-accessible data directories. When uploading a zip file, the archive should usually contain a single top-level data directory. Server directories must be readable by the FastAPI/Celery process.

!!! warning "File names"
    The file names listed here come from `Molo_Create`, the alignment wrappers, and web workers. Use these directory structures as the source of truth when preparing data.

## Web Downstream Analysis Input

| Data type | Web path | Reader | Recommended directory contents |
| --- | --- | --- | --- |
| 10X Visium | `/analyse/downstream/visium` | `Seurat::Load10X_Spatial()` | `filtered_feature_bc_matrix.h5` and `spatial/` |
| Slide-seq | `/analyse/downstream/slideseq` | `counts.*.gz` + `spatial.csv(.gz)` | `counts.csv.gz`/`counts.tsv.gz`/`counts.txt.gz`, `spatial.csv` or `spatial.csv.gz` |
| Vizgen MERFISH | `/analyse/downstream/merfish` | `Seurat::LoadVizgen()` | Vizgen standard output, such as `cell_by_gene.csv`, cell boundary files, and metadata files |
| Nanostring CosMx | `/analyse/downstream/cosmx` | `Seurat::LoadNanostring()` | CosMx expression matrix, metadata, FOV, polygon, transcript, and related files |
| Akoya CODEX | `/analyse/downstream/codex` | `LoadAkoya()` | `codex.csv` |
| 10X Xenium | `/analyse/downstream/xenium` | `Seurat::LoadXenium()` | Xenium standard output, such as `cell_feature_matrix.h5`, cells, transcripts, and boundaries files |
| Stereo-seq | `/analyse/downstream/stereoseq` | `SeuratDisk` + `rhdf5` | `stereo_seq.h5ad`, containing `obsm/spatial` and `obs/cell_name` |
| spatial ATAC-seq | `/analyse/downstream/atac` | ArchR/Signac worker | `fragments.tsv.gz`, `fragments.tsv.gz.tbi`, and `spatial/` |

### Visium

```text
visium_sample/
  filtered_feature_bc_matrix.h5
  spatial/
    scalefactors_json.json
    tissue_lowres_image.png
    tissue_hires_image.png
    tissue_positions.csv            # or tissue_positions_list.csv
    aligned_fiducials.jpg
    detected_tissue_image.jpg
```

### Slide-seq

```text
slideseq_sample/
  counts.csv.gz        # or counts.tsv.gz / counts.txt.gz
  spatial.csv.gz       # or spatial.csv
```

The first column of the `counts` file should contain feature/gene IDs, and the remaining columns should be beads/cells. `spatial.csv` should use a coordinate format readable by Seurat `ReadSlideSeq()`.

### MERFISH

```text
merfish_sample/
  cell_by_gene.csv
  cell_metadata.csv
  cell_boundaries/
    feature_data_0.hdf5
    feature_data_1.hdf5
```

Use the actual Vizgen standard output layout, as long as `Seurat::LoadVizgen(data.dir=...)` can read it.

### CosMx

```text
cosmx_sample/
  *_exprMat_file.csv
  *_metadata_file.csv
  *_fov_positions_file.csv
  *-polygons.csv
  *_tx_file.csv
```

Use the actual CosMx output supported by `Seurat::LoadNanostring(data.dir=...)`.

### Xenium

```text
xenium_sample/
  cell_feature_matrix.h5
  cells.csv.gz
  transcripts.csv.gz
  cell_boundaries.csv.gz
  nucleus_boundaries.csv.gz
```

Use the actual output from 10X Xenium Explorer/Onboard Analysis, as long as `Seurat::LoadXenium()` can read it.

### Stereo-seq

```text
stereoseq_sample/
  stereo_seq.h5ad
```

The worker reads:

- `obsm/spatial`: spatial coordinates.
- `obs/cell_name`: cell/spot names.

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

The ATAC worker builds or reuses ArchR ArrowFiles for `fragments.tsv.gz` and keeps a cache under `tmp/web_arrow_cache/` inside the input directory. Make sure this directory is writable in server deployments.

## Alignment and Integration Input

The web alignment and integration page supports file/folder uploads and server paths. A server path can be a parent directory or a comma-separated list of sample directories.

```text
alignment_parent/
  slice_1/
    filtered_feature_bc_matrix.h5
    spatial/
    truth.txt        # recommended, not required in every scenario
  slice_2/
    filtered_feature_bc_matrix.h5
    spatial/
    truth.txt
```

`truth.txt` is recommended as a two-column, tab-separated file:

```text
barcode_1    CellTypeA
barcode_2    CellTypeB
```

When `truth.txt` is present, the wrapper writes labels to `cell_type_truth`. When `truth.txt` is absent, the wrapper first runs SCTransform/PCA/UMAP/clustering and then supplements metadata with cluster labels.

## Python Core Integration Input

When running `Molo_FastAPI/app/core/python/main_process.py` directly, the input directory must already be organized in Molo parquet format. The Python dual-encoder logic requires exactly two batches.

```text
molo_input/
  Molo1/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
    image.png          # optional
  Molo2/
    Count.parquet
    SCT.parquet
    spatial.parquet
    meta.parquet
    image.png          # optional
```

File requirements:

- `Count.parquet`: raw or count matrix, one cell/spot per row and one feature per column, with a required `cells` column.
- `SCT.parquet`: normalized/filtered feature matrix with the same structure as `Count.parquet`.
- `spatial.parquet`: contains at least two spatial coordinate columns. The save workflow uses `x` and `y`.
- `meta.parquet`: cell metadata. Row order must match the matrices.

## Custom Data

Downstream `Custom` object creation does not have a separate page, but `Molo_Create(data_type="Custom")` supports the files below. To use custom data through the web UI, either convert it to a supported platform directory or add a custom page in development.

```text
custom_sample/
  matrix.parquet      # required
  embedding.parquet   # optional
  umap.parquet        # optional
  meta.csv            # optional
  spatial.csv         # optional
```

`matrix.parquet` has one cell per row and one feature per column, and includes `__index_level_0__` as the cell ID. `meta.csv` may contain `GroundTruth`, `Prediction`, and `Batch`. `spatial.csv` can use two columns `x,y` or three columns `barcodes,xcoord,ycoord`.
