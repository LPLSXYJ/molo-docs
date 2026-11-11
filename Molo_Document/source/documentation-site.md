# 文档维护与双站同步

两个入口暂时保留：自建双语站 docs.molopipeline.site 和 Read the Docs。应用导航以可选择的下拉菜单展示，两项均在新标签页打开。

**英文内容唯一主源：AI4Bread/Molo-tutorial 的 docs/**。自建站英文是从明确的 Git revision 导出的镜像，保留旧目录；不再独立修改第二套英文参数或接口说明。canonical-source.json 记录源 revision、URL 映射和 SHA-256，CI 检查镜像与指定主源是否一致。中文说明是人工同步版本；精确签名表与英文共享。

[英文维护步骤](https://docs.molopipeline.site/en/documentation-site/) 给出导出和检查命令。两套页面中的 api.md 含义不同：自建是 HTTP，RTD 是 R，必须使用明确映射。发布后分别确认 CI、Pages/RTD 的实际部署和线上内容，不把本地构建成功当作上线。

如未来仅保留 RTD，应保留自建旧地址到对应 RTD 页面的逐页跳转，不应整体删除后让已有链接失效。本次不删域名、不做该迁移。
