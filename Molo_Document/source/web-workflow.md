# Web 工作流

Web 入口由 FastAPI 提供，所有分析任务都会进入 Celery 队列。提交前必须填写结果邮箱并输入一次性 6 位验证码；任务提交后可以关闭页面，结果会通过邮件中的安全链接下载。

## 对齐与整合

入口：

```text
/analyse/alignment/
```

页面包含两个工作区。

### Multi-Slice Alignment

用途：多切片空间对齐，仅运行空间对齐，不做完整表达整合。

表单字段：

| 字段 | 说明 |
| --- | --- |
| Input Source | `Upload Files` 或 `Server Path` |
| Upload Slices | 上传包含多个样本的文件夹或 zip |
| Server Path(s) | 父目录，或逗号分隔的多个样本目录 |
| Data Type | Visium、Xenium、Stereo-seq、Slide-seq、MerFISH、CosMx、CODEX、Custom |
| Result email | 接收验证码和结果邮件 |

默认空间对齐方法为 Molo OT/PFGW。每个切片目录保留 `truth.txt` 会提升标签和评估信息的完整性。

### Pairwise Alignment & Integration

用途：两个样本的空间对齐、表达整合和基础结果预览。

表单字段：

| 字段 | 说明 |
| --- | --- |
| Input Source | `Upload Files` 或 `Server Path` |
| Upload Slices | 选择两个样本，或包含两个样本的 zip/目录 |
| Data Type (Sample 1/2) | 分别指定两个样本的数据类型 |
| Alignment Method | `Molo` 或 `Raw` |
| Result email | 接收验证码和结果邮件 |

Python 核心整合逻辑要求两个 batch。多样本场景请使用 Multi-Slice Alignment 或在开发侧扩展整合逻辑。

### 对齐输出预览

任务完成后页面会显示：

- `Raw_Alignment_3D.png`
- `Molo_Alignment_3D.png`
- `umap_batch_celltype_DLPFC.png`，仅整合模式可能生成

完整结果仍以邮件下载包为准。

## 下游分析

入口模板：

```text
/analyse/downstream/{analysis_type}
```

支持的 `analysis_type`：

| 类型 | 路径 |
| --- | --- |
| Visium | `/analyse/downstream/visium` |
| ATAC | `/analyse/downstream/atac` |
| Slide-seq | `/analyse/downstream/slideseq` |
| Xenium | `/analyse/downstream/xenium` |
| CosMx | `/analyse/downstream/cosmx` |
| MERFISH | `/analyse/downstream/merfish` |
| CODEX | `/analyse/downstream/codex` |
| Stereo-seq | `/analyse/downstream/stereoseq` |

### 输入来源

| 来源 | 说明 |
| --- | --- |
| Upload Local File | 上传一个 `.zip`，内部包含该数据类型的完整数据目录 |
| Server File Path | 填写 FastAPI/Celery 可访问的数据目录 |

HTTP API 还支持从已完成整合任务读取输入，但页面主要暴露 upload/server 两种方式。

### 参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| Species | `mouse` | 可选 `mouse` 或 `human`；ATAC 对应 mm10/hg38 |
| Clustering Resolution | `0.5` | Seurat 聚类分辨率 |
| Number of Neighbors | `30` | KNN/SNN 邻居数 |
| Min Features (QC) | Visium `2500`，ATAC `1000` | 创建对象阶段的最小 feature 过滤 |

### 分析步骤

| 步骤 | Web 名称 | 后端 stage |
| --- | --- | --- |
| QC | Required | `creation` 或 `atac_analysis` |
| Clustering | Louvain/Leiden 或 Dimensionality Reduction | `reduction` |
| GO Enrichment | GO 富集 | `go` |
| Cell Communication | CellChat | `cellchat` |
| Trajectory Inference | Monocle3 | `trajectory` |

GO、CellChat、Trajectory 是可选步骤。某些数据质量或标注不足时，可选步骤可能不产生有效图像；此时任务仍可能完成，但对应 gallery 为空。

## 邮箱验证码

每次提交任务都需要新的验证码：

1. 输入邮箱。
2. 点击 `Send code`。
3. 查收 6 位验证码。
4. 输入验证码后提交任务。

开发环境若使用 `MAIL_BACKEND=console`，验证码会写入服务日志，而不会真的发送邮件。

## Job ID 与恢复

提交成功后页面会显示 Job ID。建议立即保存 Job ID，用于：

- 重新打开页面后恢复状态。
- 复制返回链接。
- 任务完成后重发结果邮件。
- 向维护者报告问题。

下游页面支持通过 `?task_id=<job_id>` 恢复；对齐页面也支持在右上角输入 Job ID。

## 结果保留

默认结果保留时间来自 `app/config/downstream.yaml`：

```yaml
runtime:
  downstream_retention_hours: 48
```

过期后结果目录和下载包会被维护任务清理。Job ID 仍可能存在于状态数据库中，但输出文件不可再下载。
