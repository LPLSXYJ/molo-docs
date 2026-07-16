# R 函数参考

本页只说明 R 层分析函数。Web 服务安装、Nginx、systemd、Redis 和公网访问配置见 [Web 服务部署](deployment.md)。

## 函数关系

| 函数 | 用途 | 常见调用位置 |
| --- | --- | --- |
| `Molo_Create()` | 从平台目录创建 Molo 对象 | 对象创建 worker、R 批处理脚本 |
| `Molo_reduction_cluster()` | QC、归一化、降维、聚类和空间图 | 下游 `cluster` stage |
| `Molo_var_features()` | 空间可变特征和 marker gene 分析 | 下游可视化或批处理 |
| `Molo_top_GO_terms()` | GO 富集分析 | 下游 `go` stage |
| `Molo_cell_chat()` | CellChat 细胞通讯分析 | 下游 `cellchat` stage |
| `Molo_traj()` | Monocle3 轨迹推断 | 下游 `trajectory` stage |
| `Molo_Integrate()` | 多对象空间对齐与表达整合 | 对齐 wrapper、R 批处理脚本 |
| `Molo_Pipeline()` | 串联基础下游分析步骤 | R 批处理脚本 |

## `Molo_Create()`

从结构化输入目录创建 Molo 对象。

| 参数 | 说明 |
| --- | --- |
| `data_type` | 数据平台类型，如 `Visium`、`Slide-seq`、`MERFISH`、`CosMx`、`Xenium`、`ATAC`、`CODEX`、`Stereo-seq`、`Custom` |
| `folder_path` | 输入数据目录 |
| `n_cells` | 可选，抽样细胞/spot 数 |
| `n_features` | 可选，抽样 feature 数 |
| `ATAC_dataset` | ATAC 参考物种，`mouse` 或 `human` |
| `ATAC_arrow_files` | 可选，复用已有 ArchR ArrowFiles |
| `CODEX_type` | CODEX 输入类型 |
| `softmax` | 是否进行 softmax 标准化 |
| `custom_index` | Custom 数据中的 cell ID 列名 |

```r
molo_obj <- Molo_Create(
  data_type = "Visium",
  folder_path = "data/visium_sample",
  n_cells = 2000,
  n_features = 3000
)
```

## `Molo_reduction_cluster()`

对 Molo 对象执行 QC、归一化、PCA/UMAP、邻接图构建和聚类。

| 参数 | 说明 |
| --- | --- |
| `obj` | 输入 Molo 对象 |
| `only_QC` | 是否只执行质量控制 |
| `nFeature_range` | feature 数过滤范围 |
| `nCount_range` | count/UMI 数过滤范围 |
| `molo_env` | 运行环境配置 |
| `labeled_ref` | 可选，参考标注对象 |
| `molo_plot_path` | 图像输出目录 |
| `save_type` | 图像保存类型 |
| `run_Banksy` | 是否启用 Banksy 空间聚类 |
| `image_alpha` | 空间图像透明度 |
| `pt_size` | 空间点大小 |
| `atac_steps` | ATAC 分析步骤深度 |
| `resolution` | 聚类分辨率 |
| `n_neighbors` | KNN/SNN 邻居数 |
| `show_progress` | 是否显示进度 |

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

识别空间可变特征和 marker genes，并写出对应图像。

| 参数 | 说明 |
| --- | --- |
| `obj` | 输入 Molo 对象 |
| `features` | 可选，指定分析的 feature 集合 |
| `sp_var_features` | 空间可变特征数量；`FALSE` 表示不筛选固定数量 |
| `molo_plot_path` | 图像输出目录 |
| `save_type` | 图像保存类型 |
| `font_size` | 图中文字大小配置 |
| `image_alpha` | 空间图像透明度 |
| `pt_size` | 表达点大小 |
| `show_progress` | 是否显示进度 |

```r
molo_obj <- Molo_var_features(
  obj = molo_obj,
  sp_var_features = 20,
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_top_GO_terms()`

根据聚类或标注执行 GO 富集分析。

| 参数 | 说明 |
| --- | --- |
| `obj` | 包含聚类或细胞类型信息的 Molo 对象 |
| `dataset` | 物种数据库，`mouse` 或 `human` |
| `plot_cols` | 可选，自定义配色 |
| `molo_plot_path` | GO 图像输出目录 |
| `font_size` | 图中文字大小配置 |
| `show_progress` | 是否显示进度 |

```r
molo_obj <- Molo_top_GO_terms(
  obj = molo_obj,
  dataset = "mouse",
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_cell_chat()`

基于 CellChat 执行细胞通讯分析。

| 参数 | 说明 |
| --- | --- |
| `obj` | 包含细胞类型或聚类标签的 Molo 对象 |
| `plot_cols` | 可选，自定义细胞群配色 |
| `dataset` | 物种数据库，`mouse` 或 `human` |
| `molo_plot_path` | 细胞通讯图像输出目录 |
| `font_size` | 图中文字大小配置 |
| `show_progress` | 是否显示进度 |

```r
molo_obj <- Molo_cell_chat(
  obj = molo_obj,
  dataset = "mouse",
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_traj()`

使用 Monocle3 进行轨迹推断。

| 参数 | 说明 |
| --- | --- |
| `obj` | 包含降维结果的 Molo 对象 |
| `plot_cols` | 可选，自定义轨迹配色 |
| `molo_plot_path` | 轨迹图像输出目录 |
| `show_progress` | 是否显示进度 |

```r
molo_obj <- Molo_traj(
  obj = molo_obj,
  molo_plot_path = "outputs/plots/visium"
)
```

## `Molo_Integrate()`

调用 Python 核心执行空间对齐和表达整合。

| 参数 | 说明 |
| --- | --- |
| `obj_list` | 输入 Molo 对象列表 |
| `var_features` | 高变特征数量 |
| `py_path` | Python 解释器命令或路径 |
| `device` | 训练设备，如 `cuda:0` 或 `cpu` |
| `save_path` | 整合结果输出目录 |
| `pretrain_epoch` | 预训练轮数 |
| `train_epoch` | 主训练轮数 |
| `tmp` | 中间文件目录 |
| `sp_alignment` | 空间对齐方法 |
| `lpgw_ref_idx` | LPGW 参考样本索引 |
| `gene_align_alpha` | 基因对齐损失权重 |
| `edge_type` | 图边来源，`spatial`、`count` 或 `together` |
| `edge_sp` | 空间 KNN 邻居数 |
| `edge_mtx` | 表达 KNN 邻居数 |
| `hidden_dims` | 隐藏层维度 |
| `reduction_dims` | 潜空间维度 |
| `shared_dims` | 共享潜空间维度 |
| `compute_iLISI` | 是否计算 iLISI |
| `alignment_only` | 是否只进行空间对齐 |
| `verbose` | 是否输出运行信息 |

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

`Molo_Integrate()` 会在内部定位 `Molo_FastAPI/app/core/python/main_process.py`。在非仓库根目录运行时，可设置 `MOLO_PROJECT_ROOT` 或 `MOLO_MAIN_PROCESS`。

## `Molo_Pipeline()`

串联对象 QC、降维聚类、空间可变特征、GO、CellChat 和轨迹分析。

| 参数 | 说明 |
| --- | --- |
| `molo_obj` | 输入 Molo 对象 |
| `only_QC` | 是否只执行 QC |
| `steps` | 要运行的步骤，如 `reduction_clustering`、`var_features`、`top_GO_terms`、`cellchat`、`traj_infer` |
| `atac_steps` | ATAC 分析步骤深度 |
| `nCount_range` | count/UMI 数过滤范围 |
| `nFeature_range` | feature 数过滤范围 |
| `plot_path` | 图像输出目录 |
| `dataset` | 物种数据库，`mouse` 或 `human` |
| `molo_env` | 运行环境配置 |
| `labeled_ref` | 可选，参考标注对象 |
| `run_Banksy` | 是否启用 Banksy |
| `save_type` | 图像保存类型 |
| `image_alpha` | 空间图像透明度 |
| `pt_size` | 空间点大小 |
| `var_features` | 指定分析 feature 集合 |
| `sp_var_features` | 空间可变特征数量 |
| `plot_cols` | 可选，自定义配色 |
| `show_progress` | 是否显示进度 |
| `return_obj` | 是否返回处理后的 Molo 对象 |

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
