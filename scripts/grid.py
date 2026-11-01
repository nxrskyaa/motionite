#!/usr/bin/env python3
"""Composite every examples/stills/NxrStyle-*.png into assets/styles-grid.png (5x3, labelled).
Non-16:9 stills (9:16, 1:1) are letterboxed on the dark cell so every style keeps its true framing."""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
STILLS = sorted((ROOT / 'examples' / 'stills').glob('NxrStyle-*.png'))
names = dict(re.findall(r"n: (\d+), slug: '[^']+', id: '[^']+', name: '([^']+)'", (ROOT / 'examples/src/styles/registry.ts').read_text()))

def font(size, bold=False):
    for p in [ROOT / 'examples/public/fonts' / ('SpaceMono.woff2'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')]:
        try: return ImageFont.truetype(str(p), size)
        except OSError: continue
    return ImageFont.load_default()

COLS, CW, CH, LB, PAD, HEAD = 5, 400, 225, 40, 14, 92
rows = (len(STILLS) + COLS - 1) // COLS
W = COLS * CW + (COLS + 1) * PAD
H = HEAD + rows * (CH + LB) + (rows + 1) * PAD
g = Image.new('RGB', (W, H), '#111216')
d = ImageDraw.Draw(g)
d.text((PAD + 4, 26), 'MOTIONITE  ·  %d NxrStyles' % len(STILLS), font=font(34, True), fill='#ffcd75')
d.text((W - PAD - 4, 34), 'stills rendered from examples/src/styles', font=font(18), fill='#8b8c93', anchor='ra')
for i, p in enumerate(STILLS):
    n = int(re.search(r'NxrStyle-(\d+)', p.name).group(1))
    x = PAD + (i % COLS) * (CW + PAD); y = HEAD + PAD + (i // COLS) * (CH + LB + PAD)
    im = Image.open(p).convert('RGB'); im.thumbnail((CW, CH), Image.LANCZOS)
    d.rectangle([x, y, x + CW - 1, y + CH - 1], fill='#1b1c22')
    g.paste(im, (x + (CW - im.width) // 2, y + (CH - im.height) // 2))
    d.rectangle([x, y + CH, x + CW - 1, y + CH + LB - 1], fill='#1b1c22')
    d.text((x + 12, y + CH + 9), f'NxrStyle {n}', font=font(18, True), fill='#ffcd75')
    d.text((x + 140, y + CH + 9), names.get(str(n), ''), font=font(18), fill='#f3f3f0')
out = ROOT / 'assets' / 'styles-grid.png'
g.quantize(colors=255, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
print('wrote', out, g.size, out.stat().st_size // 1024, 'KB')
