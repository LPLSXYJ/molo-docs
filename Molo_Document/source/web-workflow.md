# Web 工作流

## 账号、项目与输入

注册使用邮箱验证码；普通任务使用登录会话，结果邮件取账号邮箱，**没有逐任务验证码字段**。审稿账号仅用于只读查看。会话不跨两个网站域名共享。

通过 `/projects` 管理项目与 Dataset Library。兼容的输入包括上传、受限服务器目录、用户可访问的数据资产，以及完成且兼容的整合结果。记录项目、资产和 Job ID，避免为了找回任务重复提交。

## 分析模式

| 模式 | 样本 | 含义 |
|---|---|---|
| `align_only` | 至少两个 | 仅物理坐标对齐，不训练完整整合模型 |
| `integrate` | 恰好两个 | 坐标对齐与潜空间/表达整合 |

网页方法值为 `Molo` 或 `Raw`。R/CLI 的组合方法和内部空间路线不能直接当作表单选项。双样本调参预设为 default/quick/standard/robust，对应 **0/10/50/100** 次试验，并受管理员上限约束。

## 下游和追踪

下游类型：visium、atac、slideseq、xenium、cosmx、merfish、codex、stereoseq。
步骤标识为 `qc`、`cluster`、`go`、`cell_chat`、`traj`；QC 会自动补入。R 流水线的步骤名称不同，不应互换。

HTTP 默认 resolution=0.5、n_neighbors=30、species=mouse、n_feature_min=2500。这些是接口默认值，不是所有数据的最优 QC 标准；R generic 的 n_neighbors 默认是 20。

My Jobs 显示分析、打包、发送的独立状态；项目/资产/任务可通过分析链追溯。任务提交排队不等于训练成功。结果保留时限由管理员决定，只有调度器和维护消费者运行时才执行自动清理。

[完整英文流程](https://docs.molopipeline.site/en/web-workflow/) · [HTTP API](api.md) · [结果边界](results.md)
