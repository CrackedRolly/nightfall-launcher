#!/usr/bin/env python3
"""Nightfall site v3 builder. Builds every page and i18n/*.json from tools/i18n (+ tools/i18n/v3).
English is baked into the HTML; assets/i18n.js swaps in other languages.
Run: python3 tools/build-site.py   (fetches the latest release + Modrinth data for no-JS fallbacks)"""
import json, os, re, html, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'i18n')
INVITE = 'https://discord.gg/PGanscBPUt'
REPO = 'https://github.com/CrackedRolly/nightfall-launcher'
LATEST = REPO + '/releases/latest'
SITE = 'https://crackedrolly.github.io/nightfall-launcher/'
LANGS = [('en','English'),('ro','Română (Romanian)'),('es','Español (Spanish)'),('pt-BR','Português (Portuguese, Brazil)'),
         ('de','Deutsch (German)'),('fr','Français (French)'),('it','Italiano (Italian)'),('pl','Polski (Polish)'),
         ('ru','Русский (Russian)'),('tr','Türkçe (Turkish)')]
def jl(p): return json.load(open(p, encoding='utf-8'))
EN = jl(os.path.join(SRC, 'en.json')); EN.update(jl(os.path.join(SRC, 'v3', 'en.json')))
E = html.escape

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'nightfall-site-build'}), timeout=20) as r: return json.load(r)
    except Exception as e:
        print('fetch failed', url, e); return None
REL = get('https://api.github.com/repos/CrackedRolly/nightfall-launcher/releases/latest') or {}
VER = (REL.get('tag_name') or 'v0.3.1').lstrip('v')
ASSETS = {a['name']: a for a in REL.get('assets', [])}
def asset(rx):
    for n, a in ASSETS.items():
        if re.search(rx, n, re.I): return a
    return None
def mb(n): return f'{n/1048576:.0f} MB' if n else '—'

def T(k, tag='span', attrs=''): return f'<{tag} data-i18n="{k}"{attrs}>{EN[k]}</{tag}>'
def V(k): return EN[k].replace('{v}', f'<span class="ver">{VER}</span>')

I = {
 'dl':'<path d="M12 3v12m0 0l-5-5m5 5l5-5M4 21h16"/>',
 'discord':'<path d="M8 8.5c2.6-.9 5.4-.9 8 0M7.5 16c2.9 1.2 6.1 1.2 9 0M9 4.5c-1.6.3-3 .8-4.3 1.6C2.8 9.3 2.3 12.4 2.6 15.5c1.5 1.2 3.1 2 4.8 2.5l1-1.8M15 4.5c1.6.3 3 .8 4.3 1.6 1.9 3.2 2.4 6.3 2.1 9.4-1.5 1.2-3.1 2-4.8 2.5l-1-1.8"/><circle cx="9" cy="12" r="1.2"/><circle cx="15" cy="12" r="1.2"/>',
 'perf':'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'modrinth':'<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18M3 12h18"/>',
 'toggle':'<rect x="2" y="7" width="20" height="10" rx="5"/><circle cx="16" cy="12" r="3"/>',
 'update':'<path d="M21 12a9 9 0 1 1-3-6.7L21 8M21 3v5h-5"/>',
 'crash':'<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.01"/>',
 'shared':'<path d="M4 6h16M4 12h10M4 18h6"/><circle cx="18" cy="16" r="3"/>',
 'loaders':'<path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5M3 17l9 5 9-5"/>',
 'access':'<circle cx="12" cy="4.5" r="1.8"/><path d="M5 8l7 1.5L19 8M12 9.5V15l-3 6M12 15l3 6"/>',
 'storage':'<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 'share':'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3M21 14v.01M17 21h4v-4M14 21v-3"/>',
 'import':'<path d="M12 3v12m0 0l-4-4m4 4l4-4"/><path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/>',
 'linux':'<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
 'menu':'<path d="M4 7h16M4 12h16M4 17h16"/>',
 'github':'<path d="M9 19c-4 1.5-4-2-6-2.5M15 21v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12 12 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
 'rss':'<path d="M5 11a8 8 0 0 1 8 8M5 5a14 14 0 0 1 14 14"/><circle cx="6" cy="18" r="1.3"/>',
}
def svg(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

def head(title, desc_key, path, title_key=''):
    alts = ''.join(f'<link rel="alternate" hreflang="{c}" href="{SITE}{path}?lang={c}">' for c,_ in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{SITE}{path}">'
    desc = E(EN.get(desc_key, desc_key))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#070708"><meta name="color-scheme" content="dark">
<link rel="icon" href="assets/star.svg" type="image/svg+xml"><link rel="icon" href="favicon.png" sizes="64x64"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="assets/fonts/space-grotesk-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="site.css?v3">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}assets/Nightfall-Launcher-Banner.png"><meta property="og:url" content="{SITE}{path}"><meta name="twitter:card" content="summary_large_image">
{alts}
<script src="assets/i18n.js?v3" defer></script></head>
<body data-title-key="{title_key}">
<a class="skip" href="#main" data-i18n="v3.skip">{EN["v3.skip"]}</a>'''

NAV = [('features.html','nav.features','features'),('download.html','nav.download','download'),('modpacks.html','nav.modpacks','modpacks'),
       ('changelog.html','nav.changelog','log'),('roadmap.html','nav.roadmap','roadmap'),('faq.html','nav.faq','faq'),('crash-help.html','nav.crash','crash')]
def nav(cur):
    opts = ''.join(f'<option value="{c}">{E(n)}</option>' for c,n in LANGS)
    links = ''.join(f'<a href="{h}" data-i18n="{k}"{" aria-current=\"page\"" if c==cur else ""}>{EN[k]}</a>' for h,k,c in NAV)
    return f'''<nav id="nav"><div class="w">
<a class="brand" href="./" aria-label="Nightfall home"><img src="assets/star.svg" alt="" width="22" height="22"><span>NIGHTFALL</span></a>
<div class="links" id="links">{links}</div>
<div class="right">
<label class="lang"><span class="sr" data-i18n="nav.lang">{EN["nav.lang"]}</span><select id="lang" aria-label="Language">{opts}</select></label>
<a class="iconbtn" href="{INVITE}" rel="noopener" aria-label="Discord" title="Discord">{svg("discord")}</a>
<button class="iconbtn menu-btn" id="menu" aria-label="Menu" aria-expanded="false" aria-controls="links">{svg("menu")}</button>
</div></div></nav>'''

def footer():
    def a(h,k,extra=''): return f'<a href="{h}" data-i18n="{k}"{extra}>{EN[k]}</a>'
    return f'''<footer><div class="w">
<div><a class="brand" href="./"><img src="assets/star.svg" alt="" width="22" height="22"><span>NIGHTFALL</span></a>{T("foot.tagline","p")}{T("v3.foot.made","p")}</div>
<div><h4 data-i18n="foot.product">{EN["foot.product"]}</h4>{a("download.html","nav.download")}{a("features.html","nav.features")}{a("modpacks.html","nav.modpacks")}{a("changelog.html","nav.changelog")}{a("roadmap.html","nav.roadmap")}</div>
<div><h4 data-i18n="v3.foot.help">{EN["v3.foot.help"]}</h4>{a("faq.html","nav.faq")}{a("faq.html#troubleshooting","v3.ts.title")}{a("crash-help.html","nav.crash")}</div>
<div><h4 data-i18n="foot.community">{EN["foot.community"]}</h4><a href="{INVITE}" rel="noopener">Discord</a><a href="{REPO}" rel="noopener">GitHub</a></div>
<div><h4 data-i18n="foot.legal">{EN["foot.legal"]}</h4>{a("privacy.html","foot.privacy")}{a("terms.html","foot.terms")}</div>
<div class="fine"><span>{T("foot.disclaimer")} © 2026 Nightfall Launcher</span>{T("foot.translated")}</div>
</div></footer>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="Screenshot"><img alt=""></div>
<script src="assets/site.js?v3" defer></script>
<script src="assets/meteors.js?v3" defer></script>
</body></html>
'''

def sh(no, k): return f'<div class="sh rv"><span class="no">{no}</span><span class="mono" data-i18n="{k}">{EN[k]}</span><i></i></div>'
def headblk(title_k, sub_k=None):
    return f'<div class="head rv"><h2 data-i18n="{title_k}">{EN[title_k]}</h2>{T(sub_k,"p") if sub_k else ""}</div>'

EXE = asset(r'\.exe$'); APP = asset(r'\.AppImage$'); ZIP = asset(r'win.*\.zip$')
def dl_buttons():
    return f'''<div class="cta"><a class="btn primary dl-main" href="{EXE["browser_download_url"] if EXE else LATEST}">{svg("dl")}<span class="os-win" data-i18n="v3.dl.win">{EN["v3.dl.win"]}</span><span class="os-linux" data-i18n="v3.dl.linux" hidden>{EN["v3.dl.linux"]}</span><span class="sub">v<span class="ver">{VER}</span></span></a>
<a class="btn" href="download.html"><span data-i18n="v3.dl.other">{EN["v3.dl.other"]}</span></a></div>
<p class="elsewhere" hidden data-i18n="v3.dl.elsewhere">{EN["v3.dl.elsewhere"]}</p>'''

def spec():
    d = (REL.get('published_at') or '')[:10]
    rows = [('v3.spec.version', f'v<span class="ver">{VER}</span>'), ('v3.spec.released', f'<span class="rel-date">{d}</span>'),
            ('v3.spec.size', f'<span class="rel-size">{mb(EXE["size"]) if EXE else "—"}</span>'), ('v3.spec.os', T('v3.spec.osv')),
            ('v3.spec.loaders', 'Fabric · Quilt · Forge · NeoForge'), ('v3.spec.langs', '23'), ('v3.spec.price', T('v3.spec.pricev'))]
    dl = ''.join(f'<dt data-i18n="{k}">{EN[k]}</dt><span class="dots"></span><dd>{v}</dd>' for k,v in rows)
    return f'<aside class="spec rv" aria-label="{EN["v3.spec.title"]}"><h2><span data-i18n="v3.spec.title">{EN["v3.spec.title"]}</span><span>№ <span class="ver">{VER}</span></span></h2><dl>{dl}</dl><div class="stamp"><span>Nightfall · Java Edition</span><img src="assets/star.svg" alt="" width="34" height="34"></div></aside>'

def hero():
    return f'''<header class="hero"><div class="w"><div class="hero-grid">
<div><div class="kick rv"><b>NEW</b><span data-i18n="v3.hero.kick">{EN["v3.hero.kick"]}</span></div>
<h1 class="rv" data-i18n="v3.hero.title">{EN["v3.hero.title"]}</h1>
<p class="lead rv" data-i18n="v3.hero.lead">{EN["v3.hero.lead"]}</p>
<div class="rv">{dl_buttons()}</div>
<p class="fine rv" data-i18n="hero.signin">{EN["hero.signin"]}</p></div>
{spec()}</div>
<figure class="frame rv"><i></i><i></i><i></i><i></i><img src="assets/shots/home-029.webp" width="1600" height="900" alt="{E(EN["hero.shotAlt"])}" data-i18n-alt="hero.shotAlt" fetchpriority="high"></figure>
<div class="cap"><span>FIG. 01 — <span data-i18n="hero.shotAlt">{EN["hero.shotAlt"]}</span></span><span>v{VER}</span></div>
</div></header>'''

FEATS = [('perf','perf'),('modrinth','modrinth'),('storage','storage'),('share','share'),('import','import'),('loaders','loaders'),('toggle','toggle'),('crash','crash'),('shared','shared'),('update','update'),('linux','linux'),('access','access')]
def flist():
    return '<div class="flist">' + ''.join(f'<div class="fi rv"><div class="hd"><span class="ic">{svg(ic)}</span><span class="n">{i+1:02d}</span></div>{T(f"feat.{k}.t","h3")}{T(f"feat.{k}.d","p")}</div>' for i,(k,ic) in enumerate(FEATS)) + '</div>'

def features_sec():
    return f'''<section id="features"><div class="w">{sh("§01","v3.sec.features")}{headblk("v3.feat.title","v3.feat.sub")}{flist()}
<p class="more rv"><a class="lnk arrow" href="features.html" data-i18n="v3.feat.all">{EN["v3.feat.all"]}</a></p></div></section>'''

def fps_sec(no="§02"):
    pts = ''.join(f'<li><b data-i18n="v3.fps.p{i}.t">{EN[f"v3.fps.p{i}.t"]}</b>{T(f"v3.fps.p{i}.d")}</li>' for i in range(1,6))
    return f'''<section id="fps"><div class="w">{sh(no,"v3.sec.fps")}{headblk("v3.fps.title","v3.fps.lead")}
<div class="fps"><ol class="plist rv">{pts}</ol>
<div class="lab rv"><h3 data-i18n="v3.fps.m.title">{EN["v3.fps.m.title"]}</h3>
<div class="ruler" aria-hidden="true"><div class="track"></div><div class="used"></div><div class="budget"><span>2%</span></div><span class="usedl">0.38%</span><span class="end">10%</span></div>
<div class="row"><span data-i18n="v3.fps.m1">{EN["v3.fps.m1"]}</span><b data-i18n="v3.fps.m1v">{EN["v3.fps.m1v"]}</b></div>
<div class="row"><span data-i18n="v3.fps.m2">{EN["v3.fps.m2"]}</span><b data-i18n="v3.fps.m2v">{EN["v3.fps.m2v"]}</b></div>
<div class="row"><span data-i18n="v3.fps.m3">{EN["v3.fps.m3"]}</span><b>54</b></div>
<p class="note" data-i18n="v3.fps.note">{EN["v3.fps.note"]}</p></div></div></div></section>'''

SHOTDIR = os.path.join(ROOT, 'assets', 'shots')
def fig(k):
    return f'<figure class="rv"><img src="assets/shots/tour/{k}.webp" loading="lazy" width="1440" height="900" alt="{E(EN[f"tour.{k}.t"])}" data-i18n-alt="tour.{k}.t"><figcaption><b data-i18n="tour.{k}.t">{EN[f"tour.{k}.t"]}</b>{T(f"tour.{k}.d")}</figcaption></figure>'
def newfig(k, d='030', wh=(1440, 900)):
    p = f'assets/shots/{d}/{k}.webp'
    if os.path.exists(os.path.join(ROOT, p)):
        media = f'<img src="{p}" loading="lazy" width="{wh[0]}" height="{wh[1]}" alt="{E(EN[f"v3.n.{k}.t"])}" data-i18n-alt="v3.n.{k}.t">'
    else:
        media = f'<div class="phbox" role="img" aria-label="{E(EN["v3.ph"])}"><span data-i18n="v3.ph">{EN["v3.ph"]}</span></div>'
    return f'<figure class="rv">{media}<figcaption><b data-i18n="v3.n.{k}.t">{EN[f"v3.n.{k}.t"]}</b>{T(f"v3.n.{k}.d")}</figcaption></figure>'
TOUR = [('g1',['import','share','builder','optimize','conflicts','modmap']),('g2',['pvphud','hudeditor','emotes']),('g3',['customize','themes','perfcheck','server'])]
ART = ['sword_midnight','sword_frost','sword_ember','sword_void','sword_mint','pickaxe_frost','axe_ember','shield_nightfall','ore_amethyst','ore_diamond']
def tour_full():
    out = f'<h2 class="tour-h rv" data-i18n="v3.fp.new035">{EN["v3.fp.new035"]}</h2>{T("v3.fp.new035sub","p"," class=\"note rv\" style=\"margin:-6px 0 18px\"")}<div class="strip">' + ''.join(newfig(k, '035', (1280, 800)) for k in ['menu035','customize035','recsadd']) + '</div>'
    out += f'<h2 class="tour-h rv" data-i18n="v3.fp.new032">{EN["v3.fp.new032"]}</h2>{T("v3.fp.new032sub","p"," class=\"note rv\" style=\"margin:-6px 0 18px\"")}<div class="strip">' + ''.join(newfig(k, '032', (1280, 800)) for k in ['mods','version','templates']) + '</div>'
    out += f'<h2 class="tour-h rv" data-i18n="v3.fp.new">{EN["v3.fp.new"]}</h2>{T("v3.fp.newsub","p"," class=\"note rv\" style=\"margin:-6px 0 18px\"")}<div class="strip">' + ''.join(newfig(k) for k in ['home','guide','friends','meteors'][:3]) + '</div>'
    for g, ks in TOUR:
        out += f'<h2 class="tour-h rv" data-i18n="tour.{g}">{EN["tour."+g]}</h2><div class="strip{' s4' if len(ks) == 4 else ''}">{"".join(fig(k) for k in ks)}</div>'
    return out

def tour_sec(no):
    return f'''<section id="tour"><div class="w">{sh(no,"v3.sec.tour")}{headblk("v3.tour.title","tour.sub")}
<div class="strip lead">{fig("perfcheck")}{fig("optimize")}{fig("pvphud")}</div>
<p class="more rv"><a class="lnk arrow" href="features.html" data-i18n="v3.tour.more">{EN["v3.tour.more"]}</a></p></div></section>'''

# Modpacks (Modrinth slugs). Fallback numbers baked at build time; site.js refreshes them live.
PACKS = [('perf',[('fabulously-optimized','fo'),('additive','additive')]),('plus',[('vanilla-perfected','vp'),('fresh-smooth','fresh')]),
         ('adv',[('better-mc-fabric-bmc2','bmc'),('prominence-2-fabric','prom')]),('more',[('cobblemon-fabric','cobble'),('create_plus','create')])]
SLUGS = [s for _,ps in PACKS for s,_ in ps]
MR = {p['slug']: p for p in (get('https://api.modrinth.com/v2/projects?ids=' + urllib.request.quote(json.dumps(SLUGS))) or [])}
def human(n):
    return f'{n/1e6:.1f}M' if n >= 1e6 else f'{n/1e3:.0f}K'
def pack(slug, k):
    p = MR.get(slug, {}); title = p.get('title', slug); loaders = ' · '.join(l.capitalize() for l in p.get('loaders', []) if l in ('fabric','quilt','forge','neoforge'))
    gv = p.get('game_versions', ['']); gv = gv[-1] if gv else ''
    return f'''<a class="pack rv" href="https://modrinth.com/modpack/{slug}" rel="noopener" data-slug="{slug}"><div class="top"><img src="assets/packs/{slug}.webp" width="52" height="52" alt="" loading="lazy"><h3>{E(title)}</h3></div>
{T(f"v3.mp.{k}","p")}<div class="meta"><span class="ld">{E(loaders)}</span><span class="gv">{E(gv)}</span><span><span class="dls">{human(p.get("downloads",0))}</span> <span data-i18n="v3.mp.dls">{EN["v3.mp.dls"]}</span></span></div>
<span class="go arrow" data-i18n="v3.mp.open">{EN["v3.mp.open"]}</span></a>'''

def packs_sec(no):
    picks = [('fabulously-optimized','fo'),('vanilla-perfected','vp'),('prominence-2-fabric','prom'),('cobblemon-fabric','cobble')]
    return f'''<section id="modpacks"><div class="w">{sh(no,"v3.sec.modpacks")}{headblk("v3.mp.title","v3.mp.sub")}
<div class="packs">{"".join(pack(s,k) for s,k in picks)}</div>
<p class="more rv"><a class="lnk arrow" href="modpacks.html" data-i18n="v3.mp.more">{EN["v3.mp.more"]}</a></p></div></section>'''

CMP_COLS = ['Nightfall','Official','Prism','Modrinth App','CurseForge','ATLauncher','GDLauncher']
CMP = [('signin','K','YYYYYY'),('instances','Y','PYYYYY'),('fabric','Y','NYYYYY'),('forge','Y','NYYYYY'),('java','Y','YYYYYY'),
       ('modrinth','Y','NYYNPY'),('curseforge','Y','NYNYYY'),('mrpack','Y','NYYNPY'),('perf','Y','NNNNNN'),('toggle','Y','NNNNNN'),('crash','Y','NPPNNP'),
       ('shared','Y','PNNNNN'),('update','Y','YYYYYY'),('ads','Y','YYNNYP'),('bedrock','N','YNNNNN')]
def cell(c, nf=False):
    cls = ' class="nf"' if nf else ''
    if c=='Y': return f'<td{cls}><span class="y" data-i18n="cmp.yes">Yes</span></td>'
    if c=='P': return f'<td{cls}><span class="p" data-i18n="cmp.partial">Partial</span></td>'
    if c=='N': return f'<td{cls}><span class="n">—</span></td>'
    if c=='K': return f'<td{cls}><span class="y" data-i18n="cmp.yes">Yes</span><span class="soon">*</span></td>'
def compare_sec(no):
    th = ''.join(f'<th{" class=nf" if i==0 else ""} scope="col">{c}</th>' for i,c in enumerate(CMP_COLS))
    rows = ''.join(f'<tr><th scope="row" data-i18n="cmp.r.{k}">{EN["cmp.r."+k]}</th>{cell(nf,True)}{"".join(cell(c) for c in rest)}</tr>' for k,nf,rest in CMP)
    return f'''<section id="compare"><div class="w">{sh(no,"v3.sec.compare")}{headblk("cmp.title","cmp.sub")}
<div class="tbl rv" tabindex="0" role="region" aria-label="{E(EN["cmp.title"])}"><table><thead><tr><th scope="col" data-i18n="cmp.feature">{EN["cmp.feature"]}</th>{th}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">* {T("cmp.note")}</p></div></section>'''

def discord_sec(no):
    return f'''<section id="community"><div class="w">{sh(no,"v3.sec.community")}<div class="dc rv">
<div><h2 data-i18n="v3.dc.title">{EN["v3.dc.title"]}</h2>{T("v3.dc.text","p")}</div>
<div class="side"><div class="count" id="dc-count" hidden><div class="on"><b id="dc-on">0</b><span data-i18n="v3.dc.online">{EN["v3.dc.online"]}</span></div><div><b id="dc-all">0</b><span data-i18n="v3.dc.members">{EN["v3.dc.members"]}</span></div></div>
<div><a class="btn primary" href="{INVITE}" rel="noopener">{svg("discord")}<span data-i18n="v3.dc.join">{EN["v3.dc.join"]}</span></a></div></div>
</div></div></section>'''

def band():
    return f'''<section><div class="w"><div class="band rv"><div><h2 data-i18n="band.title">{EN["band.title"]}</h2>{T("band.text","p")}</div>
<div class="cta"><a class="btn primary dl-main" href="{EXE["browser_download_url"] if EXE else LATEST}">{svg("dl")}<span class="os-win" data-i18n="v3.dl.win">{EN["v3.dl.win"]}</span><span class="os-linux" data-i18n="v3.dl.linux" hidden>{EN["v3.dl.linux"]}</span></a></div></div></div></section>'''

def write(name, body):
    open(os.path.join(ROOT, name), 'w', encoding='utf-8').write(body)
def page_hero(kicker_k, title_k, sub_k, extra=''):
    return f'<div class="page-hero"><div class="sh rv"><span class="no">§</span><span class="mono" data-i18n="{kicker_k}">{EN[kicker_k]}</span><i></i></div><h1 class="rv" data-i18n="{title_k}">{EN[title_k]}</h1>{T(sub_k,"p"," class=\"rv\"")}{extra}</div>'

# ---------- index ----------
write('index.html', head(EN['meta.title'],'meta.desc','', 'meta.title') + nav('home') + '<main id="main">' + hero() + features_sec() + fps_sec('§02') + tour_sec('§03') + packs_sec('§04') + compare_sec('§05') + discord_sec('§06') + band() + '</main>' + footer())

# ---------- features ----------
write('features.html', head('Features — Nightfall Launcher','meta.desc','features.html') + nav('features') +
      f'<main id="main"><div class="w">{page_hero("v3.sec.features","v3.fp.title","v3.fp.sub")}<section style="padding-top:40px">{tour_full()}</section>'
      f'<section>{sh("§","feat.kicker")}{headblk("v3.feat.title","v3.feat.sub")}{flist()}</section></div>' + fps_sec('§') + band() + '</main>' + footer())

# ---------- download ----------
def filecard(kind, a, title_k, desc_k, rec=False):
    if a:
        sha = (a.get('digest') or '').replace('sha256:','')
        meta = f'<dl><dt data-i18n="v3.d.file">{EN["v3.d.file"]}</dt><dd class="fn">{E(a["name"])}</dd><dt data-i18n="v3.d.size">{EN["v3.d.size"]}</dt><dd class="sz">{mb(a["size"])}</dd><dt>SHA-256</dt><dd><span class="sha">{sha or "—"}</span><button class="copy" type="button" data-i18n="v3.d.copy" data-done="{E(EN["v3.d.copied"])}">{EN["v3.d.copy"]}</button></dd></dl>'
        act = f'<div class="act"><a class="btn {"primary" if rec else "sm"} dlb" href="{a["browser_download_url"]}">{svg("dl")}<span data-i18n="v3.d.get">{EN["v3.d.get"]}</span><span class="sub">v<span class="ver">{VER}</span></span></a></div>'
    else:
        meta = ''; act = f'<div class="act"><a class="btn sm" href="{LATEST}" rel="noopener">{svg("github")}<span data-i18n="v3.d.all">{EN["v3.d.all"]}</span></a></div>'
    return f'<article class="file rv" data-kind="{kind}"><span class="badge" hidden data-i18n="v3.d.rec">{EN["v3.d.rec"]}</span><h2 data-i18n="{title_k}">{EN[title_k]}</h2>{T(desc_k,"p")}{meta}{act}</article>'
REQ = ['os','cpu','ram','gpu','disk','net']
req_rows = ''.join(f'<tr><th scope="row" data-i18n="v3.req.{k}">{EN["v3.req."+k]}</th><td data-i18n="v3.req.{k}.min">{EN[f"v3.req.{k}.min"]}</td><td data-i18n="v3.req.{k}.rec">{EN[f"v3.req.{k}.rec"]}</td></tr>' for k in REQ)
write('download.html', head('Download — Nightfall Launcher','meta.desc','download.html') + nav('download') +
      f'<main id="main"><div class="w">{page_hero("nav.download","v3.d.title","v3.d.sub")}'
      f'<div class="files" id="files">{filecard("win",EXE,"v3.d.win.t","v3.d.win.d")}{filecard("linux",APP,"v3.d.linux.t","v3.d.linux.d")}{filecard("zip",ZIP,"v3.d.zip.t","v3.d.zip.d")}'
      f'<article class="file off rv" data-kind="mac"><h2 data-i18n="v3.d.mac.t">{EN["v3.d.mac.t"]}</h2>{T("v3.d.mac.d","p")}<div class="act"><a class="btn sm" href="roadmap.html" data-i18n="nav.roadmap">{EN["nav.roadmap"]}</a></div></article></div>'
      f'<p class="dstatus" id="dstatus" aria-live="polite"><a class="lnk" href="changelog.html" data-i18n="v3.d.notes">{EN["v3.d.notes"]}</a> · <a class="lnk" href="{REPO}/releases" rel="noopener" data-i18n="v3.d.all">{EN["v3.d.all"]}</a></p>'
      f'<section id="install">{sh("§01","v3.d.wsteps.t")}<ol class="steps rv"><li data-i18n="v3.d.w1">{EN["v3.d.w1"]}</li><li data-i18n="v3.d.w2">{EN["v3.d.w2"]}</li><li data-i18n="v3.d.w3">{EN["v3.d.w3"]}</li></ol>'
      f'<p class="note" data-i18n="hero.signin">{EN["hero.signin"]}</p></section>'
      f'<section id="linux">{sh("§02","v3.d.lsteps.t")}<ol class="steps rv"><li data-i18n="v3.d.l1">{EN["v3.d.l1"]}</li><li><span data-i18n="v3.d.l2">{EN["v3.d.l2"]}</span><br><code>chmod +x Nightfall-Launcher-*.AppImage</code></li><li data-i18n="v3.d.l3">{EN["v3.d.l3"]}</li></ol></section>'
      f'<section id="verify">{sh("§03","v3.d.sha")}<div class="twocol"><div class="rv"><h2 data-i18n="v3.d.verify.t">{EN["v3.d.verify.t"]}</h2>{T("v3.d.verify.d","p"," style=\"color:var(--dim);margin-top:16px\"")}</div>'
      f'<div class="box rv"><span class="lbl" style="margin-top:0" data-i18n="v3.d.verify.win">{EN["v3.d.verify.win"]}</span><pre>Get-FileHash .\\Nightfall-Launcher-<span class="ver">{VER}</span>-win-x64.exe -Algorithm SHA256</pre>'
      f'<span class="lbl" data-i18n="v3.d.verify.lin">{EN["v3.d.verify.lin"]}</span><pre>sha256sum Nightfall-Launcher-<span class="ver">{VER}</span>-linux-x86_64.AppImage</pre></div></div></section>'
      f'<section id="requirements">{sh("§04","v3.d.pc")}{headblk("v3.req.t","v3.req.sub")}<div class="tbl req rv" tabindex="0" role="region" aria-label="{E(EN["v3.req.t"])}"><table><thead><tr><th scope="col" data-i18n="v3.req.part">{EN["v3.req.part"]}</th><th scope="col" data-i18n="v3.req.min">{EN["v3.req.min"]}</th><th scope="col" data-i18n="v3.req.rec">{EN["v3.req.rec"]}</th></tr></thead><tbody>{req_rows}</tbody></table></div>'
      f'<p class="note" data-i18n="v3.req.acc">{EN["v3.req.acc"]}</p></section></div></main>' + footer())

# ---------- modpacks ----------
groups = ''.join(f'<h2 class="pgroup rv" data-i18n="v3.mp.g.{g}">{EN["v3.mp.g."+g]}</h2><div class="packs two">{"".join(pack(s,k) for s,k in ps)}</div>' for g,ps in PACKS)
write('modpacks.html', head('Modpacks — Nightfall Launcher','meta.desc','modpacks.html') + nav('modpacks') +
      f'<main id="main"><div class="w">{page_hero("v3.mp.kicker","v3.mp.ptitle","v3.mp.sub")}<section style="padding-top:30px">{groups}<p class="note">{EN and T("v3.mp.note")}</p></section>'
      f'<section>{sh("§","v3.mp.how.t")}<ol class="steps rv"><li data-i18n="v3.mp.how.1">{EN["v3.mp.how.1"]}</li><li data-i18n="v3.mp.how.2">{EN["v3.mp.how.2"]}</li><li data-i18n="v3.mp.how.3">{EN["v3.mp.how.3"]}</li></ol></section></div>' + band() + '</main>' + footer())

# ---------- roadmap ----------
def it(k): return f'<div class="it"><b data-i18n="v3.rm.{k}.t">{EN[f"v3.rm.{k}.t"]}</b>{T(f"v3.rm.{k}.d")}</div>'
def done(k): return f'<div class="it"><b data-i18n="{k}">{EN[k]}</b></div>'
cols = (f'<div class="col now"><h2 data-i18n="v3.rm.now">{EN["v3.rm.now"]}</h2>{it("redesign")}<div class="it"><b data-i18n="v3.n.friends.t">{EN["v3.n.friends.t"]}</b>{T("v3.n.friends.d")}</div>{it("fps")}</div>'
        f'<div class="col"><h2 data-i18n="v3.rm.next">{EN["v3.rm.next"]}</h2>{it("signin")}{it("online")}{it("suggest")}</div>'
        f'<div class="col"><h2 data-i18n="v3.rm.later">{EN["v3.rm.later"]}</h2>{it("light")}{it("store")}{it("mac")}</div>'
        f'<div class="col done"><h2 data-i18n="v3.rm.done">{EN["v3.rm.done"]}</h2>{done("tour.pvphud.t")}{done("tour.perfcheck.t")}{done("feat.shared.t")}{done("tour.import.t")}{done("feat.linux.t")}</div>')
write('roadmap.html', head('Roadmap — Nightfall Launcher','meta.desc','roadmap.html') + nav('roadmap') +
      f'<main id="main"><div class="w">{page_hero("v3.rm.kicker","v3.rm.title","v3.rm.sub")}<div class="rm rv">{cols}</div>'
      f'<p class="more"><a class="btn" href="{INVITE}" rel="noopener">{svg("discord")}<span data-i18n="v3.rm.idea">{EN["v3.rm.idea"]}</span></a></p></div></main>' + footer())

# ---------- faq ----------
def faq_list(pre, n):
    return '<div class="faq">' + ''.join(f'<details><summary data-i18n="{pre}q{i}">{EN[f"{pre}q{i}"]}</summary><div class="a" data-i18n="{pre}a{i}">{EN[f"{pre}a{i}"]}</div></details>' for i in range(1,n+1)) + '</div>'
write('faq.html', head('FAQ — Nightfall Launcher','meta.desc','faq.html') + nav('faq') +
      f'<main id="main"><div class="w">{page_hero("faq.kicker","faq.title","faq.sub")}'
      f'<div class="faqgrid" style="margin-top:56px"><nav class="faqside" aria-label="FAQ"><a href="#questions" data-i18n="faq.kicker">{EN["faq.kicker"]}</a><a href="#troubleshooting" data-i18n="v3.ts.title">{EN["v3.ts.title"]}</a><a href="crash-help.html" data-i18n="nav.crash">{EN["nav.crash"]}</a><a href="{INVITE}" rel="noopener">Discord</a></nav>'
      f'<div><div id="questions">{faq_list("faq.",12)}</div>'
      f'<section id="troubleshooting" style="padding-top:90px">{sh("§","v3.ts.title")}<h2 class="rv" data-i18n="v3.ts.title">{EN["v3.ts.title"]}</h2>{T("v3.ts.sub","p"," style=\"color:var(--dim);margin:16px 0 30px\"")}{faq_list("v3.ts.",7)}</section></div></div></div></main>' + footer())

# ---------- changelog ----------
FALLBACK_NOTE = f'<article class="rel"><div class="when"><div class="v">v{VER}</div></div><div class="notes"><p><a class="lnk" href="{REPO}/releases" rel="noopener" data-i18n="log.github">{EN["log.github"]}</a></p></div></article>'
write('changelog.html', head('Changelog — Nightfall Launcher','meta.desc','changelog.html') + nav('log') +
      f'<main id="main"><div class="w">{page_hero("log.kicker","log.title","log.sub", f"<div class=cta-row><a class=\"btn sm\" href=\"{REPO}/releases.atom\" rel=\"noopener\">{svg("rss")}<span data-i18n=\"v3.log.rss\">{EN["v3.log.rss"]}</span></a></div>")}'
      f'<nav class="jump" id="jump" aria-label="{E(EN["v3.log.jump"])}"></nav><p class="note" id="log-status" aria-live="polite" data-i18n="log.loading">{EN["log.loading"]}</p><section class="rel hl033"><h2 data-i18n="v3.nv0.3.9">{EN["v3.nv0.3.9"]}</h2><ul>{"".join(f"<li data-i18n=v3.nv0.3.9.{i}>{EN[f'v3.nv0.3.9.{i}']}</li>" for i in range(1,4))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.nv0.4.0">{EN["v3.nv0.4.0"]}</h2><ul>{"".join(f"<li data-i18n=v3.nv0.4.0.{i}>{EN[f'v3.nv0.4.0.{i}']}</li>" for i in range(1,5))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.n038">{EN["v3.n038"]}</h2><ul>{"".join(f"<li data-i18n=v3.n038.{i}>{EN[f'v3.n038.{i}']}</li>" for i in range(1,4))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.n037">{EN["v3.n037"]}</h2><ul>{"".join(f"<li data-i18n=v3.n037.{i}>{EN[f'v3.n037.{i}']}</li>" for i in range(1,4))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.n036">{EN["v3.n036"]}</h2><ul>{"".join(f"<li data-i18n=v3.n036.{i}>{EN[f'v3.n036.{i}']}</li>" for i in range(1,7))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.n035">{EN["v3.n035"]}</h2><ul>{"".join(f"<li data-i18n=v3.n035.{i}>{EN[f'v3.n035.{i}']}</li>" for i in range(1,6))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.n034">{EN["v3.n034"]}</h2><ul>{"".join(f"<li data-i18n=v3.n034.{i}>{EN[f'v3.n034.{i}']}</li>" for i in range(1,6))}</ul></section><section class="rel hl033"><h2 data-i18n="v3.n033">{EN["v3.n033"]}</h2><ul>{"".join(f"<li data-i18n=v3.n033.{i}>{EN[f'v3.n033.{i}']}</li>" for i in range(1,6))}</ul></section><div id="releases">{FALLBACK_NOTE}</div></div></main>' + footer())

# ---------- legal ----------
def legal(fn, title):
    src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    inner = re.search(r'<main[^>]*>(.*?)</main>', src, re.S).group(1).strip()
    scripts = re.findall(r'<script>.*?</script>', src, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', src).group(1)
    h = head(f'{title} — Nightfall Launcher', 'meta.desc', fn).replace(E(EN['meta.desc']), desc, 2)
    write(fn, h + nav('') + f'<main id="main" class="w doc">{inner}</main>' + footer().replace('</body></html>', ''.join(scripts) + '</body></html>'))
legal('privacy.html','Privacy Policy'); legal('terms.html','Terms of Use')

# ---------- translations ----------
os.makedirs(os.path.join(ROOT,'i18n'), exist_ok=True)
for c,_ in LANGS:
    if c=='en': continue
    d = jl(os.path.join(SRC, c+'.json'))
    v3p = os.path.join(SRC, 'v3', c+'.json')
    if os.path.exists(v3p): d.update(jl(v3p))
    json.dump(d, open(os.path.join(ROOT,'i18n',c+'.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
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
write('crash-help.html', head('Crash help — Nightfall Launcher', 'meta.desc', 'crash-help.html') + nav('crash') + crash_help() + footer())
print('built v'+VER)
