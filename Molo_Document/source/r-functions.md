# R 函数参考

当前核对了 **11 个公共函数、124 个形式参数**，包括 S4 generic 的真实默认值。函数签名由同一份源码契约生成，不从旧示例猜测。

| 函数 | 职责 |
|---|---|
| Molo_Create / Molo_Convert | 创建和转换对象 |
| Molo_reduction_1 / Molo_reduction_cluster | 降维、QC 和聚类 |
| Molo_var_features | 特征/空间变异分析 |
| Molo_top_GO_terms / Molo_cell_chat / Molo_traj | GO、细胞通讯、轨迹 |
| Molo_Integrate | R 到 Python 的对齐/双样本整合桥 |
| Molo_Pipeline / Molo_save_data | 下游流水线与保存 |

`sp_var_features` 是逻辑控制开关；不要把旧示例 `20` 当作要选择的特征数。Molo_Integrate 当前有 43 个参数，默认设备 cuda:1、方法 Molo+LPGW、pretrain_epoch=100、train_epoch=300、shared_dims=20、总 latent=30、dist_threshold=NULL。Python CLI 有不同默认值。

旧 tri_loss、ggae_loss、cos_loss、bce_loss、kl_loss、K_h、edge 并非当前 Molo_Integrate 的形式参数；图选择参数是 edge_type。采样参数不意味着整条图模型是 mini-batch 训练。

[完整参数表](reference/r-parameters.md) · [英文示例](https://docs.molopipeline.site/en/r-functions/) · [模型架构](architecture.md)
