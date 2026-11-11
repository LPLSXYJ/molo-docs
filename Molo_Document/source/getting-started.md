# 快速开始与安装

## 使用在线网站

1. 进入 [Molo](https://molo.ai4bread.com/)，注册时通过邮箱验证码验证账号，随后登录。
2. 从 Dataset Library 建立项目/数据集，或者在分析表单上传数据。
3. 根据目的选择多切片物理对齐、**恰好两个样本**的整合，或下游分析。
4. 在 My Jobs 追踪已有 Job ID；提交成功不代表分析成功。

**每次分析不再单独索取邮箱验证码。** 审稿访问为只读示例，不能提交分析。更换网站域名需要重新建立会话。

## 本地开发环境

Web 依赖与完整科学环境不是同一件事。R、Python、GPU/CPU、平台读取器、CellChat/Monocle3/ArchR 等按具体流程单独准备。没有已核验的通用 Docker 镜像，不应把示例环境当作保证。

按 [英文安装清单](https://docs.molopipeline.site/en/getting-started/) 核对源码、运行时与依赖，再阅读 [部署](deployment.md)。不要通过运行主分析脚本来做“只读检查”；它可能创建输出和数据库。
