# R Function Reference

This page only describes the R-level analysis functions. For web service installation, Nginx, systemd, Redis, and public access configuration, see [Web Service Deployment](deployment.md).

## Function Relationships

| Function | Purpose | Common call site |
| --- | --- | --- |
| `Molo_Create()` | Create a Molo object from a platform directory | Object creation worker, R batch scripts |
| `Molo_reduction_cluster()` | QC, normalization, dimensionality reduction, clustering, and spatial graph | Downstream `cluster` stage |
| `Molo_var_features()` | Spatially variable feature and marker gene analysis | Downstream visualization or batch processing |
| `Molo_top_GO_terms()` | GO enrichment analysis | Downstream `go` stage |
| `Molo_cell_chat()` | CellChat cell-cell communication analysis | Downstream `cellchat` stage |
| `Molo_traj()` | Monocle3 trajectory inference | Downstream `trajectory` stage |
| `Molo_Integrate()` | Multi-object spatial alignment and expression integration | Alignment wrapper, R batch scripts |
| `Molo_Pipeline()` | Chain basic downstream analysis steps | R batch scripts |

## `Molo_Create()`

Create a Molo object from a structured input directory.

| Parameter | Description |
| --- | --- |
| `data_type` | Data platform type, such as `Visium`, `Slide-seq`, `MERFISH`, `CosMx`, `Xenium`, `ATAC`, `CODEX`, `Stereo-seq`, or `Custom` |
| `folder_path` | Input data directory |
| `n_cells` | Optional number of cells/spots to sample |
| `n_features` | Optional number of features to sample |
| `ATAC_dataset` | ATAC reference species, `mouse` or `human` |
| `ATAC_arrow_files` | Optional existing ArchR ArrowFiles to reuse |
| `CODEX_type` | CODEX input type |
| `softmax` | Whether to apply softmax normalization |
| `custom_index` | Cell ID column name in Custom data |

```r
molo_obj <- Molo_Create(
  data_type = "Visium",
  folder_path = "data/visium_sample",
  n_cells = 2000,
  n_features = 3000
)
```

## `Molo_reduction_cluster()`

Run QC, normalization, PCA/UMAP, adjacency graph construction, and clustering on a Molo object.

| Parameter | Description |
| --- | --- |
| `obj` | Input Molo object |
| `only_QC` | Whether to run quality control only |
| `nFeature_range` | Feature-count filtering range |
| `nCount_range` | Count/UMI filtering range |
| `molo_env` | Runtime environment configuration |
| `labeled_ref` | Optional reference annotation object |
| `molo_plot_path` | Image output directory |
| `save_type` | Image save type |
| `run_Banksy` | Whether to enable Banksy spatial clustering |
| `image_alpha` | Spatial image opacity |
| `pt_size` | Spatial point size |
| `atac_steps` | Depth of ATAC analysis steps |
| `resolution` | Clustering resolution |
| `n_neighbors` | Number of KNN/SNN neighbors |
| `show_progress` | Whether to show progress |

```r
molo_obj <- Molo_reduction_cluster(
  obj = molo_obj,
  only_QC = FALSE,
  nFeature_range = c(200, 2500),
  nCount_range = c(500, 15000),
  molo_plot_path = "outputs/plots/visium",
  resolution = 0.5,
  n_neighbors = 30
)
```

## `Molo_var_features()`

Identify spatially variable features and marker genes, and write the corresponding figures.

| Parameter | Description |
| --- | --- |
| `obj` | Input Molo object |
| `features` | Optional feature set to analyze |
| `sp_var_features` | Number of spatially variable features; `FALSE` means no fixed-count selection |
| `molo_plot_path` | Image output directory |
| `save_type` | Image save type |
| `font_size` | Text size configuration in plots |
| `image_alpha` | Spatial image opacity |
| `pt_size` | Expression point size |
| `show_progress` | Whether to show progress |

```r
molo_obj <- Molo_var_features(
  obj = molo_obj,
  sp_var_features = 20,
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_top_GO_terms()`

Run GO enrichment analysis based on clusters or annotations.

| Parameter | Description |
| --- | --- |
| `obj` | Molo object containing cluster or cell-type information |
| `dataset` | Species database, `mouse` or `human` |
| `plot_cols` | Optional custom colors |
| `molo_plot_path` | GO image output directory |
| `font_size` | Text size configuration in plots |
| `show_progress` | Whether to show progress |

```r
molo_obj <- Molo_top_GO_terms(
  obj = molo_obj,
  dataset = "mouse",
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_cell_chat()`

Run CellChat-based cell-cell communication analysis.

| Parameter | Description |
| --- | --- |
| `obj` | Molo object containing cell-type or cluster labels |
| `plot_cols` | Optional custom cell-group colors |
| `dataset` | Species database, `mouse` or `human` |
| `molo_plot_path` | Cell-cell communication image output directory |
| `font_size` | Text size configuration in plots |
| `show_progress` | Whether to show progress |

```r
molo_obj <- Molo_cell_chat(
  obj = molo_obj,
  dataset = "mouse",
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_traj()`

Run trajectory inference with Monocle3.

| Parameter | Description |
| --- | --- |
| `obj` | Molo object containing dimensionality reduction results |
| `plot_cols` | Optional custom trajectory colors |
| `molo_plot_path` | Trajectory image output directory |
| `show_progress` | Whether to show progress |

```r
molo_obj <- Molo_traj(
  obj = molo_obj,
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_Integrate()`

Call the Python core to run spatial alignment and expression integration.

| Parameter | Description |
| --- | --- |
| `obj_list` | Input list of Molo objects |
| `var_features` | Number of highly variable features |
| `py_path` | Python interpreter command or path |
| `device` | Training device, such as `cuda:0` or `cpu` |
| `save_path` | Integration result output directory |
| `pretrain_epoch` | Number of pretraining epochs |
| `train_epoch` | Number of main training epochs |
| `tmp` | Intermediate file directory |
| `sp_alignment` | Spatial alignment method |
| `lpgw_ref_idx` | LPGW reference sample index |
| `gene_align_alpha` | Gene-alignment loss weight |
| `edge_type` | Graph edge source, `spatial`, `count`, or `together` |
| `edge_sp` | Number of spatial KNN neighbors |
| `edge_mtx` | Number of expression KNN neighbors |
| `hidden_dims` | Hidden dimension |
| `reduction_dims` | Latent dimension |
| `shared_dims` | Shared latent dimension |
| `compute_iLISI` | Whether to compute iLISI |
| `alignment_only` | Whether to perform spatial alignment only |
| `verbose` | Whether to print runtime information |

```r
integrated_obj <- Molo_Integrate(
  obj_list = list(sample_1, sample_2),
  var_features = 3000,
  py_path = "python",
  device = "cuda:0",
  save_path = "outputs/integration",
  tmp = "outputs/tmp/integration",
  sp_alignment = "Molo+LPGW",
  train_epoch = 300
)
```

`Molo_Integrate()` locates `Molo_FastAPI/app/core/python/main_process.py` internally. When running outside the repository root, set `MOLO_PROJECT_ROOT` or `MOLO_MAIN_PROCESS`.

## `Molo_Pipeline()`

Chain object QC, dimensionality reduction and clustering, spatially variable features, GO, CellChat, and trajectory analysis.

| Parameter | Description |
| --- | --- |
| `molo_obj` | Input Molo object |
| `only_QC` | Whether to run QC only |
| `steps` | Steps to run, such as `reduction_clustering`, `var_features`, `top_GO_terms`, `cellchat`, `traj_infer` |
| `atac_steps` | Depth of ATAC analysis steps |
| `nCount_range` | Count/UMI filtering range |
| `nFeature_range` | Feature-count filtering range |
| `plot_path` | Image output directory |
| `dataset` | Species database, `mouse` or `human` |
| `molo_env` | Runtime environment configuration |
| `labeled_ref` | Optional reference annotation object |
| `run_Banksy` | Whether to enable Banksy |
| `save_type` | Image save type |
| `image_alpha` | Spatial image opacity |
| `pt_size` | Spatial point size |
| `var_features` | Feature set to analyze |
| `sp_var_features` | Number of spatially variable features |
| `plot_cols` | Optional custom colors |
| `show_progress` | Whether to show progress |
| `return_obj` | Whether to return the processed Molo object |

```r
molo_obj <- Molo_Pipeline(
  molo_obj = molo_obj,
  steps = c("reduction_clustering", "top_GO_terms", "cellchat"),
  nCount_range = c(500, 15000),
  nFeature_range = c(200, 2500),
  plot_path = "outputs/plots/visium",
  dataset = "mouse",
  run_Banksy = FALSE
)
```
