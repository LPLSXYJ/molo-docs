# Molo bilingual documentation

English is exported from **AI4Bread/Molo-tutorial/docs/** at the exact Git SHA in
`canonical-source.json`. Do not independently edit `source_en/` or generated
reference tables. The current English guide covers the active dual-encoder
shared/private model, actual losses, spatial routes, account-based web workflow,
projects/assets/chains, parameters, outputs and scientific limitations.
Chinese pages in `source/` are manually aligned summaries; exact signature tables
are shared, and detailed English pages remain available. Both domains are retained.

## Refresh from the canonical repository

```bash
# Run in an authorized, reviewed checkout of AI4Bread/Molo-tutorial:
python scripts/export_selfhosted.py --destination /path/to/molo-docs/Molo_Document
# Review source_en/, config and canonical-source.json together.
# In this repository:
python -m pip install -r Molo_Document/requirements-docs.txt
mkdocs build -f Molo_Document/mkdocs.yml --strict
mkdocs build -f Molo_Document/mkdocs.en.yml --strict
python scripts/check_documentation.py
```

Review Chinese translations when refreshing. CI also checks the mirror against
the pinned canonical revision. No scientific application code or secrets are
required for docs builds. A PR builds without deploying; only an upstream merged
push can publish Pages. Confirm the deployed Pages commit and live pages rather
than assuming a local build or source upload published the custom domain.

Legacy English paths are mapped explicitly: `/en/api/` remains HTTP while
`/en/r-functions/` remains R. RTD `/api/` instead means R; do not redirect by name
alone if eventually retaining only Read the Docs. Current update removes neither
site nor language. No source data, scientific runtime, credentials or databases
belong here.
