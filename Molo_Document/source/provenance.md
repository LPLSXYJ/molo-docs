# 版本、来源与核查边界

本轮依据当前工作树核对 Web 1.6.0、11个公共R函数/124参数、37个CLI选项、51条挂载HTTP路由，以及当前双编码器、decoder、translator、损失与空间路线。

源码工作树并不干净，基础 Git commit 不能完整代表当前实现。源文件 SHA-256 在公共 source-contract.json 中记录。没有执行科学训练、重新跑 benchmark、发测试邮件，不能把文档/健康检查成功当成复现结果。

双站英文文档采用同一份明确 Git revision 作为主源；本仓库 canonical-source.json 记录映射和校验。中文按相同架构和接口同步，精确机器生成参数表仍使用原参数名。

[英文来源与限制](https://docs.molopipeline.site/en/provenance/) · [文档同步](documentation-site.md)
