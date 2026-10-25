# python3 tools/add_release.py 037 '<json {lc: [title, item1, ...]}>' : adds a "New in" changelog block (all 10 languages)
import json, sys
tag, T = sys.argv[1], json.loads(open(sys.argv[2]).read())
n = len(T['en']) - 1
for lc, v in T.items():
    p = f'tools/i18n/v3/{lc}.json'; d = json.load(open(p)); d[f'v3.n{tag}'] = v[0]
    for i in range(1, n + 1): d[f'v3.n{tag}.{i}'] = v[i]
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
p = 'tools/build-site.py'; s = open(p).read(); anchor = '<section class="rel hl033"><h2 data-i18n="v3.n0'
i = s.index(anchor)
blk = '<section class="rel hl033"><h2 data-i18n="v3.n%s">{EN["v3.n%s"]}</h2><ul>{"".join(f"<li data-i18n=v3.n%s.{i}>{EN[f\'v3.n%s.{i}\']}</li>" for i in range(1,%d))}</ul></section>' % (tag, tag, tag, tag, n + 1)
if f'v3.n{tag}"' not in s: s = s[:i] + blk + s[i:]
open(p, 'w').write(s)
