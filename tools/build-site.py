#!/usr/bin/env python3
"""Builds index.html, faq.html, changelog.html, privacy.html, terms.html and i18n/*.json.
English text is baked into the HTML; assets/i18n.js swaps in other languages.
Run: python3 tools/build-site.py"""
import json, os, re, html, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'i18n')
INVITE = 'https://discord.gg/PGanscBPUt'
REPO = 'https://github.com/CrackedRolly/nightfall-launcher'
LATEST = REPO + '/releases/latest'
SITE = 'https://crackedrolly.github.io/nightfall-launcher/'
LANGS = [('en','English'),('ro','Română (Romanian)'),('es','Español (Spanish)'),('pt-BR','Português (Portuguese, Brazil)'),
         ('de','Deutsch (German)'),('fr','Français (French)'),('it','Italiano (Italian)'),('pl','Polski (Polish)'),
         ('ru','Русский (Russian)'),('tr','Türkçe (Turkish)')]
EN = json.load(open(os.path.join(SRC, 'en.json'), encoding='utf-8'))

def t(k, tag='span', attrs=''):
    return f'<{tag} data-i18n="{k}"{attrs}>{EN[k]}</{tag}>'
def tx(k): return f'<span data-i18n="{k}">{EN[k]}</span>'

I = {  # 24px stroke icons
 'dl':'<path d="M12 3v12m0 0l-5-5m5 5l5-5M4 21h16"/>',
 'discord':'<path d="M8 8.5c2.6-.9 5.4-.9 8 0M7.5 16c2.9 1.2 6.1 1.2 9 0M9 4.5c-1.6.3-3 .8-4.3 1.6C2.8 9.3 2.3 12.4 2.6 15.5c1.5 1.2 3.1 2 4.8 2.5l1-1.8M15 4.5c1.6.3 3 .8 4.3 1.6 1.9 3.2 2.4 6.3 2.1 9.4-1.5 1.2-3.1 2-4.8 2.5l-1-1.8"/><circle cx="9" cy="12" r="1.2"/><circle cx="15" cy="12" r="1.2"/>',
 'perf':'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'modrinth':'<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18M3 12h18"/>',
 'toggle':'<rect x="2" y="7" width="20" height="10" rx="5"/><circle cx="16" cy="12" r="3"/>',
 'update':'<path d="M21 12a9 9 0 1 1-3-6.7L21 8M21 3v5h-5"/>',
 'crash':'<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.01"/>',
 'simple':'<circle cx="12" cy="12" r="9"/><path d="M10 8l6 4-6 4z"/>',
 'shared':'<path d="M4 6h16M4 12h10M4 18h6"/><circle cx="18" cy="16" r="3"/>',
 'loaders':'<path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/>',
 'access':'<circle cx="12" cy="4.5" r="1.8"/><path d="M5 8l7 1.5L19 8M12 9.5V15l-3 6M12 15l3 6"/>',
 'menu':'<path d="M4 7h16M4 12h16M4 17h16"/>',
 'github':'<path d="M9 19c-4 1.5-4-2-6-2.5M15 21v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12 12 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
}
def svg(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

def head(title_key, desc_key, path, title_override=None):
    title = title_override or EN[title_key]
    alts = ''.join(f'<link rel="alternate" hreflang="{c}" href="{SITE}{path}?lang={c}">' for c,_ in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{SITE}{path}">'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(EN[desc_key])}">
<meta name="theme-color" content="#0a0a0b"><meta name="color-scheme" content="dark">
<link rel="icon" href="assets/star.svg" type="image/svg+xml"><link rel="icon" href="favicon.png" sizes="64x64"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/space-grotesk-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="site.css">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(EN[desc_key])}">
<meta property="og:image" content="{SITE}assets/Nightfall-Launcher-Banner.png"><meta property="og:url" content="{SITE}{path}"><meta name="twitter:card" content="summary_large_image">
{alts}
<script src="assets/i18n.js" defer></script></head>
<body data-title-key="{title_key if not title_override else ''}">
<a class="skip" href="#main">Skip to content</a>'''

def nav(current):
    opts = ''.join(f'<option value="{c}">{html.escape(n)}</option>' for c,n in LANGS)
    def a(href, key, cur): return f'<a href="{href}" data-i18n="{key}"{" aria-current=\"page\"" if cur==current else ""}>{EN[key]}</a>'
    return f'''<nav id="nav"><div class="w">
<a class="brand" href="./"><img src="assets/star.svg" alt="" width="22" height="22"><span>NIGHTFALL</span></a>
<div class="links" id="links">{a("./#features","nav.features","")}{a("./#compare","nav.compare","")}{a("changelog.html","nav.changelog","log")}{a("faq.html","nav.faq","faq")}{a("crash-help.html","nav.crash","crash")}</div>
<div class="right">
<label class="lang"><span class="sr" data-i18n="nav.lang">{EN["nav.lang"]}</span><select id="lang" aria-label="Language">{opts}</select></label>
<a class="btn sm discord" href="{INVITE}" rel="noopener">{svg("discord")}<span data-i18n="nav.discord">Discord</span></a>
<button class="menu-btn" id="menu" aria-label="Menu" aria-expanded="false" aria-controls="links">{svg("menu")}</button>
</div></div></nav>'''

def footer():
    return f'''<footer><div class="w">
<div><a class="brand" href="./" style="margin:0 0 12px"><img src="assets/star.svg" alt="" width="22" height="22"><span>NIGHTFALL</span></a>{t("foot.tagline","p")}</div>
<div><h4 data-i18n="foot.product">{EN["foot.product"]}</h4><a href="{LATEST}" class="dl-link" data-i18n="nav.download">{EN["nav.download"]}</a><a href="./#features" data-i18n="nav.features">{EN["nav.features"]}</a><a href="changelog.html" data-i18n="nav.changelog">{EN["nav.changelog"]}</a><a href="crash-help.html" data-i18n="nav.crash">{EN["nav.crash"]}</a></div>
<div><h4 data-i18n="foot.community">{EN["foot.community"]}</h4><a href="{INVITE}" rel="noopener">Discord</a><a href="{REPO}" rel="noopener">GitHub</a><a href="faq.html" data-i18n="nav.faq">{EN["nav.faq"]}</a></div>
<div><h4 data-i18n="foot.legal">{EN["foot.legal"]}</h4><a href="privacy.html" data-i18n="foot.privacy">{EN["foot.privacy"]}</a><a href="terms.html" data-i18n="foot.terms">{EN["foot.terms"]}</a></div>
<div class="fine"><span>{tx("foot.disclaimer")} © 2026 Nightfall Launcher</span>{t("foot.translated","span",' class="tnote"')}</div>
</div></footer>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Screenshot"><img alt=""></div>
<script src="assets/site.js" defer></script>
</body></html>
'''

def hero():
    return f'''<header class="hero"><div class="w">
<img class="star" src="assets/star.svg" alt="" width="84" height="84">
<div class="tag rv"><b>v<span class="ver">0.1.1</span></b>{tx("hero.tag")}</div>
<h1 class="rv" data-i18n="hero.title">{EN["hero.title"]}</h1>
<p class="lead rv" data-i18n="hero.lead">{EN["hero.lead"]}</p>
<div class="cta rv"><a class="btn primary dl-link" href="{LATEST}">{svg("dl")}<span data-i18n="hero.download">{EN["hero.download"]}</span></a>
<a class="btn" href="{INVITE}" rel="noopener">{svg("discord")}<span data-i18n="hero.discord">{EN["hero.discord"]}</span></a></div>
<p class="meta rv"><span data-i18n="hero.meta" data-v>{EN["hero.meta"].replace("{v}","0.1.1")}</span></p>
<p class="meta small rv" data-i18n="hero.smartscreen">{EN["hero.smartscreen"]}</p>
<p class="meta small rv" data-i18n="hero.signin">{EN["hero.signin"]}</p>
<div class="frame rv"><img src="assets/shots/home.webp" width="1600" height="1000" alt="{EN["hero.shotAlt"]}" data-i18n-alt="hero.shotAlt" fetchpriority="high"></div>
</div></header>'''

FEATS = [('perf','perf',0),('modrinth','modrinth',0),('toggle','toggle',0),('update','update',0),('crash','crash',1),('simple','simple',1),('shared','shared',1),('loaders','loaders',0),('access','access',1)]
def features():
    cards = ''.join(f'<div class="card rv"><div class="ic">{svg(ic)}</div><h3>{tx(f"feat.{k}.t")}{"<span class=soon>0.2</span>" if soon else ""}</h3>{t(f"feat.{k}.d","p")}</div>' for k,ic,soon in FEATS)
    return f'''<section id="features"><div class="w">
<div class="head rv"><span class="mono" data-i18n="feat.kicker">{EN["feat.kicker"]}</span><h2 data-i18n="feat.title">{EN["feat.title"]}</h2>{t("feat.sub","p")}</div>
<div class="grid">{cards}</div>
<p class="note rv">{tx("feat.soonNote")}</p>
</div></section>'''

def fig(k, cls=''):
    return f'<figure class="rv {cls}"><img src="assets/shots/{k}.webp" loading="lazy" width="1600" height="1000" alt="{EN[f"shots.{k}.t"]}" data-i18n-alt="shots.{k}.t" title="{EN["shots.zoom"]}"><figcaption><b data-i18n="shots.{k}.t">{EN[f"shots.{k}.t"]}</b>{tx(f"shots.{k}.d")}</figcaption></figure>'
def shots():
    return f'''<section id="screens"><div class="w">
<div class="head rv"><span class="mono" data-i18n="shots.kicker">{EN["shots.kicker"]}</span><h2 data-i18n="shots.title">{EN["shots.title"]}</h2>{t("shots.sub","p")}</div>
<div class="shots">{fig("mods","tall")}<div class="side">{fig("simple")}{fig("crash")}</div></div>
<div class="strip">{fig("instance")}{fig("access")}{fig("home")}</div>
</div></section>'''

# Y yes, P partial, N no, S 0.2, X 0.2 experimental, K pending Mojang approval
CMP_COLS = ['Nightfall','Official','Prism','Modrinth App','CurseForge','ATLauncher','GDLauncher']
CMP = [('signin','K','YYYYYY'),('instances','Y','PYYYYY'),('fabric','Y','NYYYYY'),('forge','X','NYYYYY'),('java','Y','YYYYYY'),
       ('modrinth','Y','NYYNPY'),('mrpack','Y','NYYNPY'),('perf','Y','NNNNNN'),('toggle','Y','NNNNNN'),('crash','S','NPPNNP'),
       ('shared','S','PNNNNN'),('simple','S','YNNNNN'),('update','Y','YYYYYY'),('ads','Y','YYNNYP'),('bedrock','N','YNNNNN')]
def cell(c, nf=False):
    cls = ' class="nf"' if nf else ''
    if c=='Y': return f'<td{cls}><span class="y" data-i18n="cmp.yes">Yes</span></td>'
    if c=='P': return f'<td{cls}><span class="p" data-i18n="cmp.partial">Partial</span></td>'
    if c=='N': return f'<td{cls}><span class="n">—</span></td>'
    if c=='S': return f'<td{cls}><span class="y" data-i18n="cmp.yes">Yes</span><span class="soon">0.2</span></td>'
    if c=='X': return f'<td{cls}><span class="p" data-i18n="cmp.experimental">experimental</span><span class="soon">0.2</span></td>'
    if c=='K': return f'<td{cls}><span class="y" data-i18n="cmp.yes">Yes</span><span class="soon">*</span></td>'
def compare():
    th = ''.join(f'<th{" class=nf" if i==0 else ""} scope="col">{c}</th>' for i,c in enumerate(CMP_COLS))
    rows = ''.join(f'<tr><th scope="row" data-i18n="cmp.r.{k}">{EN["cmp.r."+k]}</th>{cell(nf,True)}{"".join(cell(c) for c in rest)}</tr>' for k,nf,rest in CMP)
    return f'''<section id="compare"><div class="w">
<div class="head rv"><span class="mono" data-i18n="cmp.kicker">{EN["cmp.kicker"]}</span><h2 data-i18n="cmp.title">{EN["cmp.title"]}</h2>{t("cmp.sub","p")}</div>
<div class="tbl rv" tabindex="0"><table><thead><tr><th scope="col" data-i18n="cmp.feature">{EN["cmp.feature"]}</th>{th}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">* {tx("cmp.note")}</p>
</div></section>'''

def band():
    return f'''<section><div class="w"><div class="band rv">
<h2 data-i18n="band.title">{EN["band.title"]}</h2>{t("band.text","p")}
<div class="cta"><a class="btn primary dl-link" href="{LATEST}">{svg("dl")}<span data-i18n="hero.download">{EN["hero.download"]}</span></a><a class="btn" href="{INVITE}" rel="noopener">{svg("discord")}<span data-i18n="hero.discord">{EN["hero.discord"]}</span></a></div>
</div></div></section>'''

def faq_list(n=9):
    return '<div class="faq">' + ''.join(f'<details><summary data-i18n="faq.q{i}">{EN[f"faq.q{i}"]}</summary><div class="a" data-i18n="faq.a{i}">{EN[f"faq.a{i}"]}</div></details>' for i in range(1,n+1)) + '</div>'

def write(name, body):
    open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(body)

write('index.html', head('meta.title','meta.desc','') + nav('home') + '<main id="main">' + hero() + features() + shots() + compare() + band() + '</main>' + footer())

write('faq.html', head('nav.faq','meta.desc','faq.html', 'FAQ — Nightfall Launcher') + nav('faq') +
      f'<main id="main"><div class="w"><div class="page-hero"><span class="mono" data-i18n="faq.kicker">{EN["faq.kicker"]}</span><h1 data-i18n="faq.title">{EN["faq.title"]}</h1><p data-i18n="faq.sub">{EN["faq.sub"]}</p><div class="cta-row"><a class="btn sm" href="crash-help.html" data-i18n="nav.crash">{EN["nav.crash"]}</a><a class="btn sm" href="{INVITE}" rel="noopener">{svg("discord")}Discord</a></div></div><section style="padding-top:40px">' + faq_list() + '</section></div></main>' + footer())

# Static fallback for changelog (replaced live from the GitHub API when reachable)
FALLBACK = [
 ('v0.1.1','2026-10-23',[ 'First release with automatic updates.',
   'Updates download in the background and install when you close the launcher (or click Restart).',
   'New design and the Falling Star icon.']),
]
fb = ''.join(f'<article class="rel"><div class="when"><div class="v">{v}</div><div class="mono d">{d}</div></div><div class="notes"><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul><div class="dl"><a class="btn sm" href="{REPO}/releases/tag/{v}" rel="noopener">{svg("github")}<span data-i18n="log.github">{EN["log.github"]}</span></a></div></div></article>' for v,d,items in FALLBACK)
write('changelog.html', head('nav.changelog','meta.desc','changelog.html','Changelog — Nightfall Launcher') + nav('log') +
      f'<main id="main"><div class="w"><div class="page-hero"><span class="mono" data-i18n="log.kicker">{EN["log.kicker"]}</span><h1 data-i18n="log.title">{EN["log.title"]}</h1><p data-i18n="log.sub">{EN["log.sub"]}</p></div>'
      f'<p class="note" id="log-status" aria-live="polite" data-i18n="log.loading">{EN["log.loading"]}</p><div id="releases" data-repo="CrackedRolly/nightfall-launcher">{fb}</div></div></main>' + footer())

# Legal pages: keep the English text from the current files
def legal(fn, title):
    src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    m = re.search(r'<main[^>]*>(.*?)</main>', src, re.S)
    inner = m.group(1).strip()
    write(fn, head('meta.title','meta.desc',fn, f'{title} — Nightfall Launcher') + nav('') + f'<main id="main" class="w doc">{inner}</main>' + footer())
legal('privacy.html','Privacy Policy'); legal('terms.html','Terms of Use')

# translations
os.makedirs(os.path.join(ROOT,'i18n'), exist_ok=True)
for c,_ in LANGS:
    if c=='en': continue
    shutil.copy(os.path.join(SRC, c+'.json'), os.path.join(ROOT,'i18n',c+'.json'))
print('built')

# ---- crash-help.html: built from data/crash-kb.json (same file the launcher ships) ----
def crash_help():
    kb = json.load(open(os.path.join(ROOT, 'data', 'crash-kb.json'), encoding='utf-8'))
    E = html.escape; cats = kb['categories']; items = []
    for e in kb['entries']:
        codes = ''.join(f'<span class="code">exit {c}</span>' for c in e.get('codes', []))
        items.append(f'<details class="kb" id="{e["id"]}" data-cat="{e["cat"]}"><summary><span class="cat">{E(cats[e["cat"]])}</span><span class="t">{E(e["title"])}</span><a class="anchor" href="#{e["id"]}" aria-label="Link to this error">#</a></summary>'
            f'<div class="body"><p>{E(e["cause"])}</p>{("<p>"+codes+"</p>") if codes else ""}<ol>{"".join(f"<li>{E(x)}</li>" for x in e["fixes"])}</ol>'
            f'<p class="sig">Matches: {" · ".join(f"<code>{E(x)}</code>" for x in e["sig"][:3])}</p></div></details>')
    chips = f'<button class="chip on" data-cat="" data-i18n="help.all">{EN["help.all"]}</button>' + ''.join(f'<button class="chip" data-cat="{k}">{E(v)}</button>' for k, v in cats.items())
    js = open(os.path.join(ROOT, 'tools', 'crash-help.js'), encoding='utf-8').read()
    return (f'<main id="main"><div class="w help"><div class="page-hero"><span class="mono" data-i18n="help.kicker">{EN["help.kicker"]}</span><h1 data-i18n="help.title">{EN["help.title"]}</h1>'
        f'<p><b>{len(kb["entries"])}</b> &middot; <span data-i18n="help.sub">{EN["help.sub"]}</span></p></div>'
        f'<div class="kbtools"><input id="q" type="search" data-i18n-ph="help.search" placeholder="{E(EN["help.search"])}" aria-label="Search"><button class="btn sm" id="chk" type="button" data-i18n="help.check">{EN["help.check"]}</button></div>'
        f'<div class="checker" id="checker" hidden><label for="log" class="note" data-i18n="help.privacy">{EN["help.privacy"]}</label><textarea id="log" rows="7"></textarea><div id="res" aria-live="polite" data-likely="{E(EN["help.likely"])}" data-none="{E(EN["help.nomatch"])}"></div></div>'
        f'<div class="chips" role="group" aria-label="Categories">{chips}</div><p class="note"><span id="count">{len(kb["entries"])}</span> <span data-i18n="help.errors">{EN["help.errors"]}</span> &middot; <span data-i18n="help.en">{EN["help.en"]}</span></p>'
        f'<div class="kblist" id="list">{"".join(items)}</div>'
        f'<p class="note"><a href="{REPO}/issues" data-i18n="help.issue">{EN["help.issue"]}</a> &middot; <a href="data/crash-kb.json">crash-kb.json</a> ({kb["updated"]})</p></div></main><script>{js}</script>')
write('crash-help.html', head('help.title', 'meta.desc', 'crash-help.html', 'Crash help — Nightfall Launcher') + nav('crash') + crash_help() + footer())
