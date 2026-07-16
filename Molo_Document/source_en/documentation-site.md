# Documentation Site Deployment

This documentation site is built with MkDocs Material. The Chinese source is in `Molo_Document/source/`, the English source is in `Molo_Document/source_en/`, and the dependency file is `Molo_Document/requirements-docs.txt`.

The Chinese site uses `Molo_Document/mkdocs.yml` and is published at the site root. The English site uses `Molo_Document/mkdocs.en.yml` and is published under `/en/`.

## Local Preview

From the repository root:

```bash
cd Molo_Document
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-docs.txt
mkdocs serve -f mkdocs.yml
```

Open the local address printed by the terminal to preview the Chinese site.

Preview the English site on another port:

```bash
mkdocs serve -f mkdocs.en.yml -a 127.0.0.1:8001
```

## Static Build

```bash
cd Molo_Document
rm -rf site
mkdocs build -f mkdocs.yml --strict
mkdocs build -f mkdocs.en.yml --strict
```

Build outputs:

```text
Molo_Document/site/      # Chinese root site
Molo_Document/site/en/   # English site
```

`site/` is generated and does not need to be committed to Git.

## GitHub Pages

The repository provides `.github/workflows/docs.yml`. Release steps:

1. Push the source to GitHub.
2. Open Pages in repository settings.
3. Set Source to `GitHub Actions`.
4. Push to `main` or `master`, or manually run the `Documentation` workflow.

The workflow runs:

```bash
python -m pip install -r Molo_Document/requirements-docs.txt
mkdocs build -f Molo_Document/mkdocs.yml --strict
mkdocs build -f Molo_Document/mkdocs.en.yml --strict
```

Then it uploads `Molo_Document/site/` as the Pages artifact. The language selector in the page header links between the Chinese root site and the English `/en/` site.

## Site URL

The current configuration assumes this GitHub Pages URL:

```text
https://lplsxyj.github.io/Molo-docs/
```

If the repository owner or repository name changes, update these fields before publishing:

- `site_url` in `Molo_Document/mkdocs.yml`
- `site_url` in `Molo_Document/mkdocs.en.yml`
- `extra.alternate[*].link` in both MkDocs configuration files

For example, a repository named `<user>/<repo>` should use:

```text
https://<user>.github.io/<repo>/
https://<user>.github.io/<repo>/en/
```

and language links such as:

```text
/<repo>/
/<repo>/en/
```

## ReadTheDocs

The repository root provides `.readthedocs.yaml`:

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

This ReadTheDocs configuration currently builds the Chinese MkDocs configuration. To publish English there as a separate project or version, point ReadTheDocs to `Molo_Document/mkdocs.en.yml`.

## Repository Structure

Recommended documentation structure:

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

Before committing, check:

```bash
mkdocs build -f Molo_Document/mkdocs.yml --strict
mkdocs build -f Molo_Document/mkdocs.en.yml --strict
git status --short Molo_Document .github/workflows/docs.yml .readthedocs.yaml
```

Commit source, configuration, and workflow files. Do not commit `.venv/`, `site/`, production `.env`, or machine-specific configuration.
