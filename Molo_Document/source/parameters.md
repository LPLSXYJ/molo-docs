# 默认值与调参

| 设置 | R Molo_Integrate | CLI |
|---|---|---|
| 设备 | cuda:1 | cuda:1 |
| 方法 | Molo+LPGW | Molo |
| 预训练参数 | 100 | 200 |
| 训练 epochs | 300 | 600 |
| iLISI | TRUE | 0 |
| latent/shared | 30/20 | 30/20 |
| 距离阈值 | NULL | None |

网页/包装器可以覆盖值。HTTP 下游 n_neighbors=30，R generic 为20。不要把设备号或 QC 参数当通用科学推荐。

当前权重：mse=1、rec=1、mnn=0.9086822346479394、nc=8.21865755284329、gme=0.2881476150721262、la=0.9340807418916036、shared_scale=0.06947880705627452、private_scale=0.3844879738634757。后两者是共享/私有 KL 项系数。它们来自 DLPFC Full Model trial377 的选择，不是所有平台的通用最优。

网页 default/quick/standard/robust 对应0/10/50/100 trials。只有双样本整合适用，管理员还控制是否允许及试验上限。不可把调参用到的同一数据当成独立测试集。

[完整搜索空间、目标和不同入口](https://docs.molopipeline.site/en/parameters/) · [R 完整表](reference/r-parameters.md) · [CLI 完整表](reference/cli-options.md)
