#!/usr/bin/env python3
"""Build assets/techniques-sheet.png from frame-50 stills of the 48 technique comps.
Render the stills first (from examples/, into the gitignored examples/out/tech/), then run this from the repo root:
  for id in $(npx remotion compositions src/index.ts --quiet | tr ' ' '\\n' | grep -E '^[TNXCUH][0-9]{2}-'); do
    npx remotion still src/index.ts $id out/tech/$id.png --frame=50 --scale=0.334; done
  python3 scripts/techniques-sheet.py examples/out/tech
"""
import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1] if len(sys.argv) > 1 else 'examples/out/tech'
order = 'TNXCUH'
fs = sorted(glob.glob(f'{src}/*.png'), key=lambda p: (order.index(os.path.basename(p)[0]), os.path.basename(p)))
TW, TH, LB, G = 320, 180, 22, 6
cols, rows = 8, (len(fs) + 7) // 8
im = Image.new('RGB', (G + cols * (TW + G), G + rows * (TH + LB + G)), '#0d0f12')
d = ImageDraw.Draw(im)
def font(sz):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
F = font(13)
for i, p in enumerate(fs):
    x, y = G + (i % cols) * (TW + G), G + (i // cols) * (TH + LB + G)
    t = Image.open(p).convert('RGB').resize((TW, TH), Image.LANCZOS)
    im.paste(t, (x, y))
    tid, name = os.path.basename(p)[:-4].split('-', 1)
    d.rectangle([x, y + TH, x + TW, y + TH + LB], fill='#1b1f26')
    d.text((x + 6, y + TH + 4), tid, fill='#ffc94a', font=F)
    d.text((x + 46, y + TH + 4), name, fill='#e8e8e8', font=F)
os.makedirs('assets', exist_ok=True)
im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save('assets/techniques-sheet.png', optimize=True)
print(im.size, len(fs), os.path.getsize('assets/techniques-sheet.png'))
