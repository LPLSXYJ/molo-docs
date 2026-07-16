# HTTP API

The web pages use the same HTTP API. When calling the API directly, you still need to request an email verification code before submitting an analysis form.

The examples below use Python `requests`.

```bash
python -m pip install requests
```

## Health Checks

```python
import requests

base = "http://127.0.0.1:8000"

print(requests.get(f"{base}/health/live").json())
print(requests.get(f"{base}/health/ready").json())
```

`/health/ready` checks the database, Redis, disk space, and configuration separately.

## Request an Email Verification Code

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

In development, if `MAIL_BACKEND=console` is used, the verification code appears in the server log. Production should use SMTP.

## Submit an Alignment/Integration Job

Example with zip upload:

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

Example with server paths:

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

## Submit a Downstream Analysis Job

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

Server path:

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

## Query Status

General status:

```python
job_id = "00000000-0000-0000-0000-000000000000"
status = requests.get(f"{base}/jobs/{job_id}", timeout=30).json()
print(status)
```

Alignment status:

```python
status = requests.get(f"{base}/analyse/alignment/status/{job_id}", timeout=30).json()
```

Downstream status:

```python
status = requests.get(f"{base}/analyse/downstream/status/{job_id}", timeout=30).json()
```

## Preview Downstream Artifacts

```python
artifacts = requests.get(f"{base}/analyse/downstream/artifacts/{job_id}", timeout=30).json()
print(artifacts)
```

An image file can be accessed through:

```text
/analyse/downstream/preview/{job_id}/{filename}
```

`filename` must be listed in the artifacts section of `manifest.json`.

## Resend Result Email

```python
resp = requests.post(f"{base}/jobs/{job_id}/resend-email", timeout=30)
resp.raise_for_status()
print(resp.json())
```

Email can be resent only when the job has completed or failed and the result has not expired.

## Download Results

The download link is not returned by the public status API. It is sent in the result email:

```text
/results/download/{token}
```

Anyone who has the token can download the result package, so do not forward the email link.
