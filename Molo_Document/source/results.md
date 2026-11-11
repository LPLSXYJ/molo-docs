# 结果与解释边界

| 文件/状态 | 含义 |
|---|---|
| matrix.parquet | 整合模式为 decoder 重建表达；alignment-only 为输入表示，不保证是原始 UMI |
| embedding.parquet | 整合时包含完整 shared+private latent；alignment-only 可为零占位 |
| umap.parquet | 可视化表示，alignment-only 可为零占位 |
| spatial.csv / meta.csv | 坐标与元数据 |
| manifest.json | 阶段状态和可预览产物 |
| analysis_status | 分析状态 |
| package_status | 安全打包状态 |
| delivery_status | 邮件/投递状态 |

分析完成不等于打包或邮件成功；GO/CellChat/轨迹缺图可能是输入、依赖、资源或失败，不能直接解释为负的生物学结果。例示 48 小时保留策略只有在维护调度/消费者运行时才执行自动清理；下载前应确认真实政策。

当前兼容 checkpoint 仅保存 enc_a，并非完整双编码器、decoder、translator 模型，不能宣称可完整无训练恢复。顶部种子函数未调用，不保证所有训练固定种子。

伪标签不同于独立真值，AD/Normal 示例缺真实标签。不同 iLISI 归一化、不同双向/覆盖惩罚 Accuracy 不能拼为同一种指标。默认权重来自 DLPFC 选择，不是跨平台通用最优或新验证。

[完整产物说明](https://docs.molopipeline.site/en/results/) · [模型架构](architecture.md)
