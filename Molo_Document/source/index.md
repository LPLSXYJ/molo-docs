# Molo 使用文档

**源码核查：2026-11-11 · Web 应用 1.6.0**

Molo 以持久化 Molo 对象贯通空间组学数据读取、物理坐标对齐、双样本共享/私有潜空间整合及下游分析。网站采用 **FastAPI、Celery、Redis、SQLite**，不是历史 Shiny 界面。

- 在线网站：[molo.ai4bread.com](https://molo.ai4bread.com/)，备用入口 [molopipeline.site](https://molopipeline.site/)。
- [模型架构](architecture.md)：当前执行的双编码器、损失项、坐标路线和输出边界。
- [Web 工作流](web-workflow.md)：注册登录、项目与数据集、分析及结果。
- [R 函数](r-functions.md)、[Python CLI](python-cli.md)、[HTTP API](api.md)。
- [参数与调参](parameters.md)：不要混淆 R、CLI 和网页默认值。

本站英文内容与 [Read the Docs](https://molo-docs.readthedocs.io/en/latest/) 使用同一份英文源文档；本站保留原页面地址和中文说明。中文说明由维护者同步，精确参数签名以共同生成的参数表为准。构建或源码检查不等于重新完成科学实验。
