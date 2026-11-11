# 数据准备

输入平台包括 Visium、Xenium、MERFISH、CosMx、Slide-seq、Stereo-seq、ATAC、CODEX，以及 R/核心流程和对齐支持的 Custom 数据。Custom 不是单独的下游网页入口。

- 保留平台原始矩阵、坐标、特征和细胞/spot 标识的对应关系。
- 双样本整合必须为两个 batch；多切片物理对齐不等价于任意 batch 整合。
- 网页可使用上传、允许范围内的服务器路径、可访问的数据资产，以及兼容的已完成整合结果。
- 服务器路径指服务器磁盘，不是浏览器所在电脑。路径须在管理员白名单中。
- 原始下游上传通常要求 ZIP；对齐表单支持目录/文件或归档。初步文件清单校验不保证平台读取一定成功。
- 需要独立真值的指标应保留真实标签；不要把推断聚类当作真实生物学标注。

完整平台文件清单、Custom 格式和 CLI Parquet 要求与英文主源一致，见 [详细输入规范](https://docs.molopipeline.site/en/data-preparation/) 和 [Python CLI](python-cli.md)。样本顺序、基因顺序、细胞顺序和空间坐标单位都应记录。
