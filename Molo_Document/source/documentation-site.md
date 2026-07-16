# 文档站部署

本文档站使用 MkDocs Material 构建。中文源码位于 `Molo_Document/source/`，英文源码位于 `Molo_Document/source_en/`，依赖写在 `Molo_Document/requirements-docs.txt`。

中文站点使用 `Molo_Document/mkdocs.yml`，发布在站点根路径；英文站点使用 `Molo_Document/mkdocs.en.yml`，发布在 `/en/`。

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

启动后访问终端输出的本地地址，即可预览中文站点。

如需预览英文站点，可使用另一个端口：

```bash
mkdocs serve -f mkdocs.en.yml -a 127.0.0.1:8001
```

## 静态构建

```bash
cd Molo_Document
rm -rf site
mkdocs build -f mkdocs.yml --strict
mkdocs build -f mkdocs.en.yml --strict
```

构建产物写入：

```text
Molo_Document/site/      # 中文根站点
Molo_Document/site/en/   # 英文站点
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
mkdocs build -f Molo_Document/mkdocs.en.yml --strict
```

然后把 `Molo_Document/site/` 上传为 Pages artifact 并发布。页面顶部的语言选择器会在中文根站点和英文 `/en/` 站点之间切换。

## 站点地址

当前配置假定 GitHub Pages 地址为：

```text
https://lplsxyj.github.io/Molo-docs/
```

如果仓库所有者或仓库名发生变化，发布前需要同步修改：

- `Molo_Document/mkdocs.yml` 中的 `site_url`。
- `Molo_Document/mkdocs.en.yml` 中的 `site_url`。
- 两个 MkDocs 配置文件里的 `extra.alternate[*].link`。

例如仓库为 `<user>/<repo>` 时，应使用：

```text
https://<user>.github.io/<repo>/
https://<user>.github.io/<repo>/en/
```

语言切换链接对应写成：

```text
/<repo>/
/<repo>/en/
```

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

在 ReadTheDocs 项目中连接 GitHub 仓库后，构建器会读取该配置并构建中文 `Molo_Document/source/`。如果要在 ReadTheDocs 发布英文站点，可为英文站点创建单独项目或版本，并把配置指向 `Molo_Document/mkdocs.en.yml`。

## 仓库结构

文档目录建议保持以下结构：

```text
Molo_Document/
  README.md
  mkdocs.yml
  mkdocs.en.yml
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
  source_en/
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
mkdocs build -f Molo_Document/mkdocs.en.yml --strict
git status --short Molo_Document .github/workflows/docs.yml .readthedocs.yaml
```

应提交源码、配置和 workflow；不要提交 `.venv/`、`site/`、生产环境 `.env` 或机器相关配置。
