# HTTP API

Web 页面使用同一套 HTTP API。直接调用 API 时，仍需要先申请邮箱验证码，再提交分析表单。

下面示例使用 Python `requests`。

```bash
python -m pip install requests
```

## 健康检查

```python
import requests

base = "http://127.0.0.1:8000"

print(requests.get(f"{base}/health/live").json())
print(requests.get(f"{base}/health/ready").json())
```

`/health/ready` 会分别检查 database、Redis、磁盘空间和配置。

## 申请邮箱验证码

```python
import requests

base = "http://127.0.0.1:8000"
email = "user@example.org"

resp = requests.post(
    f"{base}/api/email-verifications",
    json={"email": email},
    timeout=30,
)
resp.raise_for_status()
challenge = resp.json()
print(challenge["verification_id"], challenge["expires_in"])
```

在开发环境中，如果 `MAIL_BACKEND=console`，验证码会出现在服务端日志里。生产环境应使用 SMTP。

## 提交对齐/整合任务

上传 zip 的示例：

```python
from pathlib import Path

import requests

base = "http://127.0.0.1:8000"
email = "user@example.org"

challenge = requests.post(
    f"{base}/api/email-verifications",
    json={"email": email},
    timeout=30,
).json()

code = input("Verification code: ").strip()
archive = Path("alignment_input.zip")

with archive.open("rb") as handle:
    files = [
        ("files", (archive.name, handle, "application/zip")),
    ]
    data = {
        "mode": "integrate",
        "data_type": "Visium,Visium",
        "sp_alignment": "Molo",
        "input_type": "upload",
        "email": email,
        "verification_id": challenge["verification_id"],
        "verification_code": code,
    }
    resp = requests.post(
        f"{base}/analyse/alignment/run",
        data=data,
        files=files,
        timeout=60,
    )
    resp.raise_for_status()

job = resp.json()
print(job["task_id"])
```

使用服务器路径的示例：

```python
    data = {
        "mode": "align_only",
        "data_type": "Visium",
        "sp_alignment": "Molo",
        "input_type": "server",
        "server_path": "server_data/project/slice_1,server_data/project/slice_2,server_data/project/slice_3",
        "email": email,
        "verification_id": challenge["verification_id"],
        "verification_code": code,
}
resp = requests.post(f"{base}/analyse/alignment/run", data=data, timeout=60)
resp.raise_for_status()
```

## 提交下游分析任务

```python
from pathlib import Path

import requests

base = "http://127.0.0.1:8000"
email = "user@example.org"

challenge = requests.post(
    f"{base}/api/email-verifications",
    json={"email": email},
    timeout=30,
).json()
code = input("Verification code: ").strip()

archive = Path("visium_sample.zip")
data = [
    ("data_source", "upload"),
    ("analysis_steps", "cluster"),
    ("analysis_steps", "go"),
    ("resolution", "0.5"),
    ("n_neighbors", "30"),
    ("species", "mouse"),
    ("n_feature_min", "2500"),
    ("email", email),
    ("verification_id", challenge["verification_id"]),
    ("verification_code", code),
]

with archive.open("rb") as handle:
    files = {"file": (archive.name, handle, "application/zip")}
    resp = requests.post(
        f"{base}/analyse/downstream/visium/submit",
        data=data,
        files=files,
        timeout=60,
    )
    resp.raise_for_status()

print(resp.json()["task_id"])
```

服务器路径：

```python
data = [
    ("data_source", "server"),
    ("server_path", "server_data/project/visium_sample"),
    ("analysis_steps", "cluster"),
    ("analysis_steps", "cell_chat"),
    ("resolution", "0.5"),
    ("n_neighbors", "30"),
    ("species", "mouse"),
    ("n_feature_min", "2500"),
    ("email", email),
    ("verification_id", challenge["verification_id"]),
    ("verification_code", code),
]
resp = requests.post(f"{base}/analyse/downstream/visium/submit", data=data, timeout=60)
resp.raise_for_status()
```

## 查询状态

通用状态：

```python
job_id = "00000000-0000-0000-0000-000000000000"
status = requests.get(f"{base}/jobs/{job_id}", timeout=30).json()
print(status)
```

对齐状态：

```python
status = requests.get(f"{base}/analyse/alignment/status/{job_id}", timeout=30).json()
```

下游状态：

```python
status = requests.get(f"{base}/analyse/downstream/status/{job_id}", timeout=30).json()
```

## 预览下游 artifact

```python
artifacts = requests.get(f"{base}/analyse/downstream/artifacts/{job_id}", timeout=30).json()
print(artifacts)
```

某个图片文件可通过：

```text
/analyse/downstream/preview/{job_id}/{filename}
```

访问。`filename` 必须在 `manifest.json` 的 artifacts 列表中。

## 重发结果邮件

```python
resp = requests.post(f"{base}/jobs/{job_id}/resend-email", timeout=30)
resp.raise_for_status()
print(resp.json())
```

只有任务已经完成或失败、且结果仍未过期时可以重发。

## 下载结果

下载链接不会通过公开状态接口直接返回，而是在结果邮件中发送：

```text
/results/download/{token}
```

任何持有 token 的人都能下载结果包，因此不要转发邮件中的链接。
