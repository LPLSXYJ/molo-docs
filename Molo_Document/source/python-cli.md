# Python 命令行

当前入口是 `Molo_FastAPI/app/core/python/main_process.py`。使用准备好的环境和 Parquet 输入，必须指定 `-data_path` 与 `-save_path`，不要直接在生产数据上试运行。

当前解析器核对了 **37 个选项**。CLI 默认设备 cuda:1、方法 Molo、pre_train_epoch=200、train_epoch=600、compute_iLISI=0；这些不同于 R 默认值。存在 pretraining 参数不证明当前执行独立预训练阶段。

整合输入必须恰好两个 batch。每个样本目录包含 Count.parquet、SCT.parquet、spatial.parquet、meta.parquet，标识、特征和细胞顺序须严格对应。表达表示来源不可凭文件名直接视为原始 UMI。

`-alignment_only 1` 在空间阶段后退出，latent/UMAP 可以只是零填充占位；不代表训练出整合表示。正式整合导出的表达矩阵是 decoder reconstruction。

[完整 CLI 参数](reference/cli-options.md) · [准备与运行示例](https://docs.molopipeline.site/en/python-cli/) · [模型架构](architecture.md)
