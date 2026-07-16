# 结果文件

Molo 结果分为三类：对齐/整合任务输出、下游分析输出、邮件下载包。Web 页面只展示部分预览图，完整结果以下载包为准。

## 对齐与整合结果

对齐任务的工作目录位于：

```text
Molo_FastAPI/data/tasks/{job_id}/
```

核心结果位于：

```text
Molo_FastAPI/data/tasks/{job_id}/results/
```

常见文件：

| 文件 | 说明 |
| --- | --- |
| `Raw_Alignment_3D.png/.pdf` | 原始坐标 3D 预览 |
| `Molo_Alignment_3D.png/.pdf` | Molo 对齐后 3D 预览 |
| `matrix.parquet` | 重建或整合后的表达矩阵 |
| `embedding.parquet` | 低维表示 |
| `umap.parquet` | UMAP 坐标 |
| `spatial.csv` | 对齐后的空间坐标 |
| `meta.csv` | 合并后的元数据 |
| `integrated_molo.rds` | 整合后的 Molo 对象 |
| `alignment_info.txt` | 空间对齐方法和参数摘要 |

Web 会把部分图片复制到：

```text
Molo_FastAPI/plots/tmp/{job_id}/
```

用于页面预览。

## 下游分析结果

下游分析输出根目录由 `app/config/downstream.yaml` 控制：

```yaml
default_output_root: "outputs/downstream"
```

单个任务目录：

```text
outputs/downstream/{job_id}/
  config.json
  manifest.json
  logs/
  intermediate/
  plots/
```

| 目录/文件 | 说明 |
| --- | --- |
| `manifest.json` | 作业 stage 状态和可预览 artifact 列表 |
| `logs/orchestrator.log` | 编排脚本日志，不会进入用户下载包 |
| `intermediate/*.rds` | worker 间传递的中间 Molo 对象 |
| `plots/*.png`、`plots/*.pdf` | 页面预览和下载包中的主要图像 |

### manifest 示例

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

## 下载包

打包任务会在：

```text
Molo_FastAPI/data/packages/{job_id}/
```

生成：

```text
molo-results-{job_id}-{sha256}.zip
```

下载包内包含：

```text
README.txt
manifest.json
results/
  ...
```

允许进入下载包的后缀：

```text
.rds .h5ad .parquet .png .pdf .csv .tsv .txt .json
```

以下内容会被排除：

- 原始上传文件。
- 内部配置 `config.json`、运行日志、stdout/stderr、traceback。
- 包含路径、邮箱、token、secret、password 等敏感字段的参数。
- 非白名单后缀文件。

## 状态字段

公开状态接口返回的主要字段：

| 字段 | 说明 |
| --- | --- |
| `analysis_status` | `queued`、`running`、`completed`、`failed`、`expired` 等 |
| `package_status` | `pending`、`running`、`ready`、`failed` 或 `not_applicable` |
| `delivery_status` | `pending`、`sent`、`retrying`、`failed`、`unknown` |
| `progress` | 0-100 的粗略进度 |
| `current_stage` | 正在执行的阶段 |
| `stages` | 下游 manifest 中的 stage 状态 |
| `output_available` | 下载包是否可用 |
| `retained_until` | 结果保留到期时间 |

状态排查优先级：

1. `analysis_status=failed`：先看对应 task 的 worker 日志和 Job ID。
2. `analysis_status=completed` 但 `package_status=failed`：看 packaging worker。
3. `package_status=ready` 但 `delivery_status=failed`：检查 SMTP 和重发接口。
4. `status=expired`：结果已按保留策略清理，需要重新运行。
