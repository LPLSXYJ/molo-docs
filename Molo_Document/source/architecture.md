# 模型架构与系统设计

**按 2026-11-11 当前源码核查，Web 1.6.0。不是把历史类、论文设想或研究 CUDA 版全部当作现用模型。**

## 从输入到交付

登录账号/项目/数据资产 → 输入校验 → FastAPI 记录 SQLite 作业 → Redis/Celery → R 平台读取与 Molo 对象 → 空间配准 → 仅对齐或双样本整合 → 可选 R 下游 → manifest、打包、邮件链接。HTTP 提交成功只代表排队。

## 空间配准与整合是两层

当前导出的 Molo_img_trans 路线由 V1 栅格全局搜索、Stage2 表达约束平移候选、P2 保守局部残差场组成。v1_p2 执行 V1→P2；three_stage 才执行三段；ra2_three_stage 的历史名字实际是 Stage2→P2。

auto 按 RA2/小样本栈选择 Stage2→P2，否则通常为 V1→P2，显式配置可优先完整三段。记录 requested/resolved route；不要声称 auto 一定跑三段。内部路线不等于网页 Molo/Raw 字段。对齐拟合不把真值标签当监督；标签可以另用于评价。

## 双流变分图模型

完整整合要求**恰好两个 batch**。空间/表达 KNN 图按 batch 取内部边、重编号和无向化，分别送入独立 GNNEncoder：enc_a、enc_b。图注意力层与 mu/logvar 双头产生后验，用重参数化采样 z。

默认总 latent=30，前20维 shared，后10维 private。分区设计不证明已完美解耦。每个 batch 一个 FeatureDecoder MLP 从完整 latent 重建表达；两个 Translator MLP 在 shared posterior mean 上执行 A→B→A、B→A→B 循环。

```text
L = rec * edge_BCE + mse * feature_MSE
    + shared_scale * KL_shared + private_scale * KL_private
    + la * translator_cycle_MSE
    + mnn * MNN + nc * NC + gme * GME
```

MNN/NC 利用共享表达的邻域约束，GME 保持批内输入与 latent 成对几何关系。shared_scale/private_scale 是 **KL 权重**，不是输出坐标缩放。当前循环没有训练 GAN 判别器；保留的辅助函数不能当作执行证据。

每 epoch 的统一采样为 min(sample_size,n_A,n_B)，默认512，用于部分损失；图边重构和 KL 仍用全图/后验，不是全流程 mini-batch GNN。pretraining 参数存在不证明独立预训练已执行。

## 输出边界

推理使用 mu，导出完整 shared+private embedding；整合矩阵是 decoder reconstruction，不是原始 UMI。alignment-only 提前退出，矩阵保持输入表示、latent/UMAP 可为零占位。checkpoint 只存 enc_a，不是完整可恢复模型。种子函数在顶部未调用。

[详细英文架构](https://docs.molopipeline.site/en/architecture/) · [参数与调参](parameters.md) · [来源核查](provenance.md)
