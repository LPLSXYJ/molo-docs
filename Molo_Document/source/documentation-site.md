# 文档站部署

本文档站使用 MkDocs Material 构建。源码位于 `Molo_Document/source/`，配置文件为 `Molo_Document/mkdocs.yml`，依赖写在 `Molo_Document/requirements-docs.txt`。

## 本地预览

从仓库根目录运行：

```bash
cd Molo_Document
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt
mkdocs serve -f mkdocs.yml
```

启动后访问终端输出的本地地址。

## 静态构建

```bash
cd Molo_Document
mkdocs build -f mkdocs.yml --strict
```

构建产物写入：

```text
Molo_Document/site/
```

`site/` 是生成目录，不需要提交到 Git。

## GitHub Pages

仓库提供 `.github/workflows/docs.yml`。发布步骤：

1. 将源码推送到 GitHub。
2. 在仓库设置中打开 Pages。
3. Source 选择 `GitHub Actions`。
4. 推送到 `main` 或 `master`，或手动运行 `Documentation` workflow。

workflow 会执行：

```bash
python -m pip install -r Molo_Document/requirements-docs.txt
mkdocs build -f Molo_Document/mkdocs.yml --strict
```

然后把 `Molo_Document/site/` 上传为 Pages artifact 并发布。

## ReadTheDocs

仓库根目录提供 `.readthedocs.yaml`：

```yaml
version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.12"

mkdocs:
  configuration: Molo_Document/mkdocs.yml

python:
  install:
    - requirements: Molo_Document/requirements-docs.txt
```

在 ReadTheDocs 项目中连接 GitHub 仓库后，构建器会读取该配置并构建 `Molo_Document/source/`。

## 仓库结构

文档目录建议保持以下结构：

```text
Molo_Document/
  README.md
  mkdocs.yml
  requirements-docs.txt
  source/
    index.md
    getting-started.md
    data-preparation.md
    web-workflow.md
    python-cli.md
    r-functions.md
    results.md
    api.md
    deployment.md
    documentation-site.md
    faq.md
    assets/
      molo.svg
      stylesheets/
        extra.css
```

提交前检查：

```bash
mkdocs build -f Molo_Document/mkdocs.yml --strict
git status --short Molo_Document .github/workflows/docs.yml .readthedocs.yaml
```

应提交源码、配置和 workflow；不要提交 `.venv/`、`site/`、生产环境 `.env` 或机器相关配置。
