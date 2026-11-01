#!/usr/bin/env python3
"""Check every relative link and image in the repo's Markdown files, including #anchors
(GitHub slug rules). Use --external to also check http(s) links with a HEAD/GET request.
Usage: python3 scripts/check-links.py [--external]
"""
import os, re, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = '--external' in sys.argv
MD_LINK = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
HTML_LINK = re.compile(r'(?:src|href)="([^"]+)"')
AUTO = re.compile(r'<(https?://[^>]+)>')

def slug(h):
    h = re.sub(r'`|\*\*|\*|_(?=\w)|\[|\]\([^)]*\)', '', h.strip()).lower()
    h = re.sub(r'[^\w\- ]', '', h, flags=re.U)
    return h.replace(' ', '-')

def anchors(path):
    out, seen, fence = set(), {}, False
    for line in open(path, encoding='utf-8'):
        if line.startswith('```'): fence = not fence
        if fence: continue
        m = re.match(r'#{1,6} (.+)', line)
        if m:
            s = slug(m.group(1)); n = seen.get(s, 0); seen[s] = n + 1
            out.add(s if n == 0 else f'{s}-{n}')
    return out

bad, ext, n = [], set(), 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in ('node_modules', '.git', 'out')]
    for f in files:
        if not f.endswith('.md'): continue
        p = os.path.join(d, f)
        text = open(p, encoding='utf-8').read()
        text_nocode = re.sub(r'```.*?```', '', text, flags=re.S)
        for url in MD_LINK.findall(text_nocode) + HTML_LINK.findall(text_nocode) + AUTO.findall(text_nocode):
            n += 1
            if url.startswith(('http://', 'https://')): ext.add(url); continue
            if url.startswith('mailto:'): continue
            target, _, frag = url.partition('#')
            tp = os.path.normpath(os.path.join(d, target)) if target else p
            if not os.path.exists(tp):
                bad.append((os.path.relpath(p, ROOT), url, 'missing file')); continue
            if frag and tp.endswith('.md') and frag not in anchors(tp):
                bad.append((os.path.relpath(p, ROOT), url, 'missing anchor'))
print(f'checked {n} links ({len(ext)} unique external)')
if EXT:
    for u in sorted(ext):
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 motionite-linkcheck'})
            code = urllib.request.urlopen(req, timeout=15).status
        except Exception as e:
            code = getattr(e, 'code', str(e)[:60])
        if code != 200: print(f'  external {code}: {u}')
for b in bad: print('BROKEN', *b, sep='  ')
sys.exit(1 if bad else 0)
