#!/usr/bin/env python3
"""Build assets/banner.png: a pixel-art title screen for Motionite by NxrLabs.
Drawn at 320x160 logical pixels with a 16-colour palette (Sweetie 16), hand-built glyphs, ordered dither,
sprites, then upscaled x4 nearest-neighbour to 1280x640 with a CRT scanline pass. Deterministic (seeded)."""
import random
from pathlib import Path
from PIL import Image

W, H, K = 320, 160, 4
P = dict(k='#1a1c2c', plum='#5d275d', red='#b13e53', orange='#ef7d57', yellow='#ffcd75', lime='#a7f070', green='#38b764',
         teal='#257179', navy='#29366f', blue='#3b5dc9', sky='#41a6f6', cyan='#73eff7', white='#f4f4f4', silver='#94b0c2',
         slate='#566c86', dark='#333c57')
hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
img = Image.new('RGB', (W, H), hexrgb(P['k']))
px = img.load()
def put(x, y, c):
    if 0 <= x < W and 0 <= y < H: px[x, y] = hexrgb(P[c]) if c in P else hexrgb(c)
def rect(x, y, w, h, c):
    for j in range(h):
        for i in range(w): put(x + i, y + j, c)
BAYER = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5]
bay = lambda x, y: (BAYER[(y & 3) * 4 + (x & 3)] + .5) / 16
rnd = random.Random(7)

# --- sky: banded with ordered dither between bands --------------------------------------------
bands = ['k', 'navy', 'plum', 'red', 'orange']
for y in range(H):
    t = min(len(bands) - 1.001, max(0, (y - 6) / 110 * (len(bands) - 1)))
    i, u = int(t), t - int(t)
    for x in range(W): put(x, y, bands[i + 1] if u > bay(x, y) else bands[i])
for _ in range(70):  # stars, a few with a 4-point twinkle
    x, y = rnd.randrange(W), rnd.randrange(70)
    put(x, y, 'white' if rnd.random() > .3 else 'silver')
for (x, y) in [(40, 18), (262, 26), (198, 12), (110, 30)]:
    put(x, y, 'white'); put(x - 1, y, 'silver'); put(x + 1, y, 'silver'); put(x, y - 1, 'silver'); put(x, y + 1, 'silver')
# moon with crater shading
for j in range(-11, 12):
    for i in range(-11, 12):
        d = (i * i + j * j) ** .5
        if d <= 10.5: put(296 + i, 60 + j, 'silver' if (i + j > 6 and d > 6) else 'white')
for (cx, cy, r) in [(292, 57, 2), (300, 65, 1)]:
    for j in range(-r, r + 1):
        for i in range(-r, r + 1):
            if i * i + j * j <= r * r: put(cx + i, cy + j, 'silver')

# --- parallax hills (far -> near) ------------------------------------------
import math
def ridge(base, amp, freq, phase, col, jag=0):
    for x in range(W):
        h = int(base - amp * (.5 + .5 * math.sin(x * freq + phase)) - (rnd.random() * jag))
        for y in range(h, H): put(x, y, col)
ridge(124, 18, .045, 1.0, 'plum', 2)
ridge(134, 12, .07, 2.2, 'dark', 1)
rect(0, 142, W, 18, 'k')
for x in range(W):  # grass lip with dither
    put(x, 141, 'teal' if x % 3 else 'green'); put(x, 142, 'green' if bay(x, 0) > .3 else 'teal')

# --- pixel glyphs ------------------------------------------------------------------------------
BIG = {  # chunky 7x8 glyphs, 2-px strokes
    'M': ['11...11', '111.111', '1111111', '11.1.11', '11...11', '11...11', '11...11', '11...11'],
    'O': ['.11111.', '1111111', '11...11', '11...11', '11...11', '11...11', '1111111', '.11111.'],
    'T': ['1111111', '1111111', '..111..', '..111..', '..111..', '..111..', '..111..', '..111..'],
    'I': ['1111111', '1111111', '..111..', '..111..', '..111..', '..111..', '1111111', '1111111'],
    'N': ['11...11', '111..11', '1111.11', '11.1111', '11..111', '11...11', '11...11', '11...11'],
    'E': ['1111111', '1111111', '11.....', '111111.', '111111.', '11.....', '1111111', '1111111'],
}
SMALL = {  # 3x5
    'A': ['010', '101', '111', '101', '101'], 'B': ['110', '101', '110', '101', '110'], 'C': ['011', '100', '100', '100', '011'],
    'D': ['110', '101', '101', '101', '110'], 'E': ['111', '100', '110', '100', '111'], 'G': ['011', '100', '101', '101', '011'],
    'H': ['101', '101', '111', '101', '101'], 'I': ['111', '010', '010', '010', '111'], 'L': ['100', '100', '100', '100', '111'],
    'M': ['101', '111', '111', '101', '101'], 'N': ['110', '101', '101', '101', '101'], 'O': ['010', '101', '101', '101', '010'],
    'P': ['110', '101', '110', '100', '100'], 'R': ['110', '101', '110', '101', '101'], 'S': ['011', '100', '010', '001', '110'],
    'T': ['111', '010', '010', '010', '010'], 'U': ['101', '101', '101', '101', '111'], 'V': ['101', '101', '101', '101', '010'],
    'X': ['101', '101', '010', '101', '101'], 'Y': ['101', '101', '010', '010', '010'], 'K': ['101', '101', '110', '101', '101'],
    '0': ['111', '101', '101', '101', '111'], '1': ['010', '110', '010', '010', '111'], '2': ['110', '001', '010', '100', '111'],
    '5': ['111', '100', '110', '001', '110'], '6': ['011', '100', '111', '101', '111'], '9': ['111', '101', '111', '001', '110'],
    '.': ['000', '000', '000', '000', '010'], ' ': ['000', '000', '000', '000', '000'], '-': ['000', '000', '111', '000', '000'],
    '>': ['100', '010', '001', '010', '100'], '<': ['001', '010', '100', '010', '001'], ':': ['000', '010', '000', '010', '000'], 'F': ['111', '100', '110', '100', '100'], 'W': ['101', '101', '111', '111', '101'],
}
def small(text, x, y, col, shadow=None):
    for ch in text:
        g = SMALL[ch]
        for j, row in enumerate(g):
            for i, b in enumerate(row):
                if b == '1':
                    if shadow: put(x + i + 1, y + j + 1, shadow)
                    put(x + i, y + j, col)
        x += 4
    return x
def small_w(text): return len(text) * 4 - 1

# --- title: MOTIONITE, chunky glyphs at x3, horizontal bevel + 4-band ramp, outline, long drop shadow ---
S, GW, GH, GAP = 3, 7, 8, 2
title = 'MOTIONITE'
tw_ = len(title) * (GW * S + GAP) - GAP
tx, ty = (W - tw_) // 2, 26
mask = set()
for n, ch in enumerate(title):
    for j, row in enumerate(BIG[ch]):
        for i, b in enumerate(row):
            if b == '1':
                for v in range(S):
                    for u in range(S): mask.add((tx + n * (GW * S + GAP) + i * S + u, ty + j * S + v))
H_T = GH * S
for (x, y) in mask:  # long extruded shadow, 4 px down-right
    for d in range(1, 5): put(x + d, y + d, 'plum' if d < 4 else 'k')
for (x, y) in mask:  # 1-px outline
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        if (x + dx, y + dy) not in mask: put(x + dx, y + dy, 'k')
for (x, y) in mask:
    r = (y - ty) / H_T
    col = 'yellow' if r < .4 else 'orange' if r < .72 else 'red'
    if (x, y - 1) not in mask: col = 'white'          # top bevel
    elif (x, y + 1) not in mask: col = 'plum'         # bottom bevel
    elif (x + 1, y) not in mask and col != 'red': col = {'yellow': 'orange', 'orange': 'red'}[col]  # right shade
    if (y - ty) % S == 1 and r < .4 and (x - 1, y) not in mask: col = 'white'  # glint on left edge
    put(x, y, col)

# --- "by NxrLabs" plate: LCD-green cartridge label ------------------------------------------------
label = 'BY NXRLABS'
lw = small_w(label) + 12
lx, ly = (W - lw) // 2, ty + H_T + 10
rect(lx - 1, ly - 1, lw + 2, 13, 'k')
rect(lx, ly, lw, 11, '#adbc77')
rect(lx, ly, lw, 1, '#bfcc91'); rect(lx, ly + 10, lw, 1, '#697852')
small(label, lx + 6, ly + 3, '#344b23')
for i in (2, lw - 3): put(lx + i, ly + 5, '#344b23')

# --- sprites -----------------------------------------------------------------------------------
def sprite(rows, x, y, pal):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != '.': put(x + i, y + j, pal[ch])
CONSOLE = [  # NxrLabs pocket system, 16x22
    '.kkkkkkkkkkkkkk.', 'kwwwwwwwwwwwwwwk', 'kwssssssssssssswk'[:16], 'kwsllllllllllswk', 'kwslLLllllLLlswk', 'kwsllllllllllswk',
    'kwslllLLLLlllswk', 'kwsllllllllllswk', 'kwssssssssssssswk'[:16], 'kwwwwwwwwwwwwwwk', 'kwwwwwwwwwwwwwwk', 'kwwkwwwwwwwwwwwk',
    'kwkkkwwwwwwrrwwk', 'kwwkwwwwwwwrrwwk', 'kwwwwwwwwrrwwwwk', 'kwwwwwwwwrrwwwwk', 'kwwwwwwwwwwwwwwk', 'kwwwwsswsswwwwwk',
    'kwwwwwwwwwwwkwkk', 'kwwwwwwwwwwkwkwk', '.kwwwwwwwwwwwwk.', '..kkkkkkkkkkkk..']
sprite(CONSOLE, 22, 108, {'k': 'k', 'w': '#e6e4da', 's': '#394333', 'l': '#adbc77', 'L': '#344b23', 'r': '#803c55'})
HERO = ['....kkkk....', '...kyyyyk...', '..kyyyyyyk..', '..kssssssk..', '..ksksskskk.', '..kssssssk..', '...kkkkkk...',
        '..kbbbbbbk..', '.kbbbybbbbk.', '.ksbbbbbbsk.', '..kbbbbbbk..', '..kbk..kbk..', '..kkk..kkk..']
sprite(HERO, 236, 128, {'k': 'k', 'y': 'yellow', 's': '#f8c8a0', 'b': 'blue'})
SLIME = ['...kkkk...', '..kggggk..', '.kgggwggk.', 'kgggggwggk', 'kgkkggkkgk', 'kggggggggk', '.kkkkkkkk.']
sprite(SLIME, 270, 134, {'k': 'k', 'g': 'lime', 'w': 'white'})
COIN = ['.kkk.', 'kyyyk', 'kywok', 'kyyok', '.kkk.']
for i, x in enumerate((56, 66, 76, 206, 216)):
    sprite(COIN, x, 118 - (i % 2) * 3, {'k': 'k', 'y': 'yellow', 'w': 'white', 'o': 'orange'})
# a film strip of frames marching across the ground (motion = frames)
for i in range(9):
    fx = 96 + i * 12
    rect(fx, 146, 10, 8, 'dark'); rect(fx + 1, 147, 8, 6, ['blue', 'red', 'lime', 'yellow', 'sky', 'orange', 'cyan', 'plum', 'green'][i])
    put(fx + 2, 145, 'silver'); put(fx + 7, 145, 'silver'); put(fx + 2, 154, 'silver'); put(fx + 7, 154, 'silver')

# --- HUD chrome --------------------------------------------------------------------------------
small('1UP 015000', 8, 6, 'white', 'k')
hi = 'HI 999990'
small(hi, W - small_w(hi) - 8, 6, 'yellow', 'k')
st = 'STAGE 15 - STYLES'
small(st, (W - small_w(st)) // 2, 6, 'cyan', 'k')
ps = '> PRESS START <'
small(ps, (W - small_w(ps)) // 2, ly + 19, 'white', 'k')
sub = 'MOTION DESIGN SKILL FOR AI AGENTS'
bw = small_w(sub) + 14; bx, by = (W - bw) // 2, ly + 31
rect(bx - 1, by - 1, bw + 2, 13, 'k'); rect(bx, by, bw, 11, 'navy')
for i in range(bw): put(bx + i, by + 1, 'white'); put(bx + i, by + 9, 'white')
for j in range(1, 10): put(bx + 1, by + j, 'white'); put(bx + bw - 2, by + j, 'white')
small(sub, bx + 7, by + 3, 'white')

# --- upscale + CRT pass: scanline every 4th row, soft corner vignette ---------------------------
out = img.resize((W * K, H * K), Image.NEAREST)
op = out.load()
OW, OH = out.size
for y in range(OH):
    for x in range(OW):
        r, g, b = op[x, y]
        f = .78 if y % K == K - 1 else 1.0
        cx, cy = (x - OW / 2) / (OW / 2), (y - OH / 2) / (OH / 2)
        v = max(0.0, (cx * cx * .5 + cy * cy * .6) - .55)
        f *= 1 - min(.35, v * .6)
        op[x, y] = (int(r * f), int(g * f), int(b * f))
dst = Path(__file__).resolve().parent.parent / 'assets' / 'banner.png'
dst.parent.mkdir(exist_ok=True)
out.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)
print('wrote', dst, out.size)
