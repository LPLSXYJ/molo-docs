# Web 服务部署

部署组件包括 FastAPI Web、专用 Redis，以及 analysis、alignment、packaging、notifications 队列。Beat/maintenance 是定期 reconcile/保留期清理组件，不运行就不会自动完成对应定时任务。

生产环境应配置 `APP_ENV`、HTTPS 的 `PUBLIC_BASE_URL`、独立 `AUTH_SECRET` 与 `DOWNLOAD_TOKEN_SECRET`、数据库路径、Redis broker/result backend 和 SMTP。**旧 EMAIL_VERIFICATION_SECRET 不是当前账号认证密钥的替代。** 密钥和机器目录只能放服务器私有环境，不能提交到公共文档。

源码内 systemd 模板使用 /opt/molo 等示例路径，不能原样覆盖现有机器。当前恢复的主机实际使用用户级 systemd：`molo.target`、Web、Redis 和四类 worker，配合 linger 实现无登录自启；Beat/maintenance 为保护旧结果保持关闭。这里描述当前部署，不保证其它主机完全相同。

先核对持久化数据库、Redis AOF、队列和活跃任务，再做受控维护；不要 flush Redis、重跑提交、盲删旧数据。只读健康检查不能替代科学/邮件全链路测试。

[可移植部署清单](https://docs.molopipeline.site/en/deployment/) · [当前架构](architecture.md) · [结果与保留](results.md)
