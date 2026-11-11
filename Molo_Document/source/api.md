# HTTP API

**HTTP API 使用已登录账号会话。不要使用旧 `/api/email-verifications` 接口或逐任务验证码示例。**

| 接口 | 用途 |
|---|---|
| POST /api/auth/register/start | JSON：username、email、password、password_confirm |
| POST /api/auth/register/complete | JSON：challenge_id、email、code，建立会话 |
| POST /auth/login | 表单：identity、password、可选 next_url |
| GET /api/auth/me | 查询当前账号 |
| POST /auth/logout | 退出当前会话 |
| POST /analyse/alignment/run | multipart/form；对齐或整合 |
| POST /analyse/downstream/{analysis_type}/submit | 下游表单提交 |
| GET /jobs/{job_id} | 分析/打包/投递状态 |
| GET /health/live 与 /health/ready | 存活与依赖就绪，不证明科学任务或 SMTP 成功 |

账号所有权控制适用于项目、数据资产和作业；审稿会话不能提交、重试、克隆等写操作。使用同一应用域名和 requests.Session 保存会话。请求不是 JSON 的表单接口不能误传 JSON。

项目、资产与分析链入口为 `/api/projects`、`/api/datasets` 和 `/chains/...`。取消、重试、克隆、重发邮件均为受权限/状态约束的 POST，不应当作健康探针。

[完整 HTTP 路由与字段](reference/http-routes.md) · [可参考的英文客户端示例](https://docs.molopipeline.site/en/api/)

注意地址区别：**本站 `/api/` 是 HTTP 文档；Read the Docs 的 `/api/` 是 R 文档**，其 HTTP 页面是 `/http-api/`。不要只按同名 URL 做站点间重定向。
