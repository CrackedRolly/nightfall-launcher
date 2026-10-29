#!/usr/bin/env python3
"""Build twice without network in an isolated copy, verify output and local links."""
import hashlib,json,os,pathlib,shutil,subprocess,tempfile
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self): super().__init__();self.links=[];self.keys=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ['href','src']:
            if key in a:self.links.append(a[key])
        if 'data-i18n' in a:self.keys.append(a['data-i18n'])
with tempfile.TemporaryDirectory(prefix='nightfall-site-ci-') as tmp:
    root=pathlib.Path(tmp)/'site'
    shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
    env=dict(os.environ,NF_SITE_OFFLINE='1')
    def build():subprocess.run(['python3','tools/build-site.py'],cwd=root,env=env,check=True)
    build()
    pages=list(root.glob('*.html'));assert len(pages)==10,f'Expected 10 pages, got {len(pages)}'
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pages}
    build();assert hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in pages},'Nondeterministic output'
    en={}
    for p in [root/'tools/i18n/en.json',root/'tools/i18n/v3/en.json']:en.update(json.loads(p.read_text()))
    locales=[]
    for p in sorted((root/'tools/i18n/v3').glob('*.json')):
        data=json.loads((root/'tools/i18n'/p.name).read_text());data.update(json.loads(p.read_text()))
        assert set(en)<=set(data),f'Missing translations in {p.name}: {set(en)-set(data)}'
        locales.append(p.stem)
    for p in pages:
        text=p.read_text();assert '<!doctype html>' in text.lower() and '</html>' in text.lower(),p.name
        page=Page();page.feed(text)
        for link in page.links:
            url=urlsplit(link)
            if url.scheme or url.netloc or not url.path:continue
            target=(p.parent/unquote(url.path)).resolve()
            assert target.is_relative_to(root),f'Escaping local link: {link}'
            assert target.exists(),f'{p.name}: missing {link}'
        for key in page.keys:assert key in en,f'{p.name}: undefined translation {key}'
    print(f'PASS {len(pages)} pages, {len(locales)} locales, local assets/links and deterministic offline generation')
