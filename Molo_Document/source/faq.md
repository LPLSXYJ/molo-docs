# FAQ

## 为什么文档以 FastAPI Web 为主？

Molo 的用户入口以 FastAPI Web、HTTP API 和 Python CLI 为主。R 仍然用于部分后端 worker，例如对象创建、降维聚类、CellChat、Monocle3 和 ATAC 分析；需要直接调用 R 函数时，可查看 [R 函数参考](r-functions.md)。

## 页面能打开，但提交后任务一直不动

通常是 Celery worker 没有启动或队列不匹配。检查：

```bash
celery -A app.celery_app:celery_app inspect ping
celery -A app.celery_app:celery_app inspect reserved
redis-cli ping
```

对齐任务需要 `alignment` 队列，下游分析需要 `analysis` 队列，打包需要 `packaging` 队列，邮件需要 `notifications` 队列。

## 收不到验证码

开发环境下如果 `MAIL_BACKEND=console`，验证码只会出现在服务端日志里。生产环境检查：

- `MAIL_BACKEND=smtp`。
- `SMTP_HOST`、`SMTP_PORT`、账号和密码正确。
- `SMTP_USE_TLS` 与 `SMTP_USE_SSL` 不能同时为 true。
- `PUBLIC_BASE_URL` 是外部可访问 HTTPS 地址。
- Redis 可用，因为验证码状态存储在 Redis 中。

## 验证码输入正确但提交失败

验证码是一次性的，并且有过期时间。默认 TTL 为：

```bash
EMAIL_VERIFICATION_TTL_SECONDS=600
```

每个分析任务都需要新验证码。如果更换邮箱，需要重新发送验证码。

## 上传 zip 后提示输入无效

检查：

- 下游分析只接受 `.zip` 上传。
- zip 内部最好只有一个顶层数据目录。
- 目录文件名必须符合 [数据准备](data-preparation.md) 中的要求。
- zip 不能超过 `MAX_UPLOAD_BYTES`。
- 解压后不能包含路径穿越、过多文件或异常压缩比。

## 服务器路径模式找不到样本

服务器路径是运行 FastAPI/Celery 的机器路径，不是浏览器所在电脑的路径。对齐页面支持父目录或逗号分隔样本目录；下游页面要求单个数据目录。

## Pairwise 整合报 batch 数量错误

`main_process.py` 的双编码器逻辑要求两个 batch。请确认输入父目录下只包含两个样本目录，并且排序后分别是两个批次。

## `truth.txt` 是必需的吗？

不是所有场景强制。存在 `truth.txt` 时，后端会把标签写入 `cell_type_truth` 并用于更完整的预览/评估。没有 `truth.txt` 时，wrapper 会运行基础预处理和聚类，用聚类标签补充元数据。

## 下游 GO、CellChat 或轨迹没有结果图

这些步骤依赖聚类、基因标注、物种数据库、表达矩阵质量和细胞类型标签。任务可能完成，但某个可选 stage 不产生有效图像。先检查：

- 是否运行了 `cluster`。
- `species` 是否选对。
- marker genes 是否足够。
- `manifest.json` 中对应 stage 的状态。
- worker 日志中是否有可选步骤失败信息。

## 结果邮件发出后链接打不开

可能原因：

- 结果已过期。
- `PUBLIC_BASE_URL` 配置错误。
- token 已过期。
- 结果包未构建成功。
- 反向代理没有正确转发 `/results/download/{token}`。

先查状态：

```bash
curl https://molo.example.org/jobs/{job_id}
```

再检查 packaging 和 notifications worker 日志。

## 文档构建失败

本目录使用 MkDocs：

```bash
python -m pip install -r Molo_Document/requirements-docs.txt
mkdocs build -f Molo_Document/mkdocs.yml --strict
```

`--strict` 会把坏链接、缺失页面、配置错误视为失败。添加页面后需要同步维护 `Molo_Document/mkdocs.yml` 的 `nav`。
