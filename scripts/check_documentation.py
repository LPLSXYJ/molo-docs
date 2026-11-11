#!/usr/bin/env python3
"""Check committed mirror digests and both built languages, without network/app calls."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'Molo_Document'
manifest=json.loads((DOCS/'canonical-source.json').read_text())
for name,digest in manifest['files_sha256'].items():
    assert hashlib.sha256((DOCS/name).read_bytes()).hexdigest()==digest, 'Mirror drift: '+name

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        if tag=='a' and 'href' in attrs:self.links.append(attrs['href'])
site=(DOCS/'site').resolve();pages={}
for path in site.rglob('*.html'):
    parser=Page();parser.feed(path.read_text());pages[path]=parser
assert len(pages)>=35,'Build Chinese and English first'
failures=[]
for path,page in pages.items():
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        local=unquote(u.path)
        target=(site/local.lstrip('/')).resolve() if local.startswith('/') else (path.parent/local).resolve() if local else path
        if target.is_dir():target=target/'index.html'
        if not target.is_relative_to(site) or not target.exists():failures.append((str(path.relative_to(site)),link,'missing file'))
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:failures.append((str(path.relative_to(site)),link,'missing anchor'))
if failures:raise SystemExit(json.dumps(failures,indent=2))
print(f'Mirror digests and {len(pages)} bilingual HTML pages/anchors passed')
