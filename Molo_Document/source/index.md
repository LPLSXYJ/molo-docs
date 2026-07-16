# Molo 使用文档

Molo 是面向空间组学数据的分析框架，覆盖多切片空间对齐、双样本表达整合、下游生物学分析、网页提交与异步任务管理。Web 服务采用 FastAPI、Celery 和 Redis 组织任务；核心整合算法提供 Python 命令行入口，便于开发者进行批处理和基准实验。

## 适用读者

- 只想通过网页提交分析的实验室用户。
- 需要准备 Visium、Xenium、MERFISH、CosMx、Slide-seq、Stereo-seq、spATAC-seq、CODEX 或自定义数据的分析人员。
- 需要在服务器上部署 Molo FastAPI 服务的维护者。
- 需要通过 Python CLI、R 函数或 HTTP API 自动化提交任务的开发者。

## 系统架构

| 层级 | 实现 | 主要目录 |
| --- | --- | --- |
| Web 界面 | FastAPI、Jinja2、静态 JS/CSS | `Molo_FastAPI/app/` |
| 任务队列 | Celery worker、Redis broker/result backend | `Molo_FastAPI/app/celery_app.py` |
| 作业状态 | SQLite WAL、Redis 锁、心跳与重投递 | `Molo_FastAPI/app/services/` |
| 空间对齐与整合 | Python 深度学习核心，R wrapper 负责对象转换 | `Molo_FastAPI/app/core/python/`、`Molo_FastAPI/app/core/R/` |
| 下游分析 | R worker，由 FastAPI 编排调用 | `Molo_obj_renv_project/`、`reduction_renv_project/`、`cellchat_renv_project/`、`trajectory_renv_project/`、`atac_renv_project/` |
| 部署 | systemd、Nginx、Redis 配置模板 | `Molo_FastAPI/deploy/` |

## 功能概览

- **空间对齐**：支持多切片对齐和 pairwise 对齐；默认使用 Molo OT/PFGW 路线，也支持 Raw 模式。
- **表达整合**：Python 核心的双编码器整合逻辑面向两个 batch 的 pairwise 整合。
- **下游分析**：包含 QC、降维聚类、GO 富集、细胞通讯和轨迹推断；ATAC 有独立的 ArchR/Signac 工作流。
- **网页提交**：上传 zip/文件夹或使用服务器路径，提交后通过 Job ID 追踪。
- **结果交付**：任务完成后构建安全结果包，下载链接发送到验证邮箱，并按保留期自动清理。
- **函数与接口**：提供 R 函数参考、Python CLI、邮箱验证、任务状态、结果邮件重发、健康检查等接口。

## 推荐阅读顺序

1. [快速开始](getting-started.md)：本地启动 Web 服务并确认依赖。
2. [数据准备](data-preparation.md)：按数据类型整理输入目录。
3. [Web 工作流](web-workflow.md)：使用网页提交对齐、整合和下游分析。
4. [Python 命令行](python-cli.md)：直接运行核心 pairwise 整合或基准脚本。
5. [R 函数参考](r-functions.md)：查看对象创建、降维聚类、GO、CellChat、轨迹和整合函数。
6. [Web 服务部署](deployment.md)：上线 FastAPI、Celery、Redis 和 Nginx。
7. [文档站部署](documentation-site.md)：将本说明文档发布到 GitHub Pages 或 ReadTheDocs。
