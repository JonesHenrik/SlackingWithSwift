"""Split PaulFrontBack.jpeg into two registered, transparent sprite frames.

The source is a JPEG sprite sheet: front-facing Paul on the left, back-turned
Paul on the right, both sitting on a *baked-in* checkerboard (JPEG has no alpha)
with a white sticker outline around each figure.

Two things matter for the game:
  1. Real transparency — flood-fill the checkerboard and the white halo away.
  2. Registration — the two frames must place the figure at identical size and
     position, or swapping them mid-turn makes Paul jump.
"""
from collections import deque
import numpy as np
from PIL import Image

SRC = '/Users/nickmelekian/Desktop/PaulAIWorkshop/PaulGame/PaulFrontBack.jpeg'
OUT = '/Users/nickmelekian/Desktop/PaulAIWorkshop/PaulGame/PaulGame/PaulGame/Assets.xcassets'

img = np.array(Image.open(SRC).convert('RGB')).astype(np.int16)
H, W, _ = img.shape
print('source', W, 'x', H)

# Background = low-saturation and bright. Tolerances are loose because JPEG
# ringing smears the checkerboard edges and the white outline.
mx = img.max(axis=2); mn = img.min(axis=2)
bg_like = ((mx - mn) <= 34) & (mn >= 132)

# Keep only the background *connected to the border*, so light greys inside the
# figure (shirt highlights, glasses lenses) survive.
seen = np.zeros((H, W), bool)
q = deque()
for x in range(W):
    for y in (0, H-1):
        if bg_like[y, x] and not seen[y, x]:
            seen[y, x] = True; q.append((y, x))
for y in range(H):
    for x in (0, W-1):
        if bg_like[y, x] and not seen[y, x]:
            seen[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1,0), (-1,0), (0,1), (0,-1)):
        ny, nx = y+dy, x+dx
        if 0 <= ny < H and 0 <= nx < W and not seen[ny, nx] and bg_like[ny, nx]:
            seen[ny, nx] = True; q.append((ny, nx))

alpha = np.where(seen, 0, 255).astype(np.uint8)

# Erode the JPEG fringe: pale, low-saturation pixels touching transparency.
for _ in range(3):
    pale = ((mx - mn) <= 48) & (mn >= 112) & (alpha > 0)
    nbr_clear = np.zeros((H, W), bool)
    nbr_clear[1:, :] |= alpha[:-1, :] == 0
    nbr_clear[:-1, :] |= alpha[1:, :] == 0
    nbr_clear[:, 1:] |= alpha[:, :-1] == 0
    nbr_clear[:, :-1] |= alpha[:, 1:] == 0
    alpha[pale & nbr_clear] = 0

rgba = np.dstack([img.astype(np.uint8), alpha])

def bbox(a):
    ys, xs = np.nonzero(a)
    return xs.min(), ys.min(), xs.max(), ys.max()

# Split the sheet down the middle.
mid = W // 2
frames = {}
for name, x0, x1 in (('front', 0, mid), ('back', mid, W)):
    sub = rgba[:, x0:x1]
    bx0, by0, bx1, by1 = bbox(sub[:, :, 3])
    frames[name] = (sub[by0:by1+1, bx0:bx1+1], (x0+bx0, by0))
    print(name, 'bbox size', bx1-bx0+1, 'x', by1-by0+1, 'at sheet', (x0+bx0, by0))

# Common square canvas. Figures are centred horizontally and share a baseline,
# so a front/back swap reads as a turn rather than a jump.
hmax = max(f.shape[0] for f, _ in frames.values())
wmax = max(f.shape[1] for f, _ in frames.values())
S = max(hmax, wmax) + 24
baseline = (S + hmax) // 2   # y of the feet, identical in both frames

placements = {}
for name, (f, origin) in frames.items():
    h, w = f.shape[:2]
    canvas = np.zeros((S, S, 4), np.uint8)
    ox = (S - w) // 2
    oy = baseline - h
    canvas[oy:oy+h, ox:ox+w] = f
    Image.fromarray(canvas).save(f'{OUT}/Paul{name.capitalize()}.imageset/Paul{name.capitalize()}.png')
    placements[name] = (ox, oy, origin, (w, h))
    print(name, '-> canvas', S, 'offset', (ox, oy))

# Locate the irises on the FRONT frame so the eye-glow overlay lands correctly.
f, origin = frames['front']
ox, oy, _, (w, h) = placements['front']
r = f[:, :, 0].astype(int); g = f[:, :, 1].astype(int); b = f[:, :, 2].astype(int)
a = f[:, :, 3]
head = int(h * 0.34)
mask = (a > 0) & (b > r + 30) & (b > 95) & (g > r)
mask[head:, :] = False
ys, xs = np.nonzero(mask)
if len(xs):
    cx = np.median(xs)
    for label, sel in (('left', xs < cx), ('right', xs >= cx)):
        ex, ey = xs[sel].mean() + ox, ys[sel].mean() + oy
        print(f'  {label} iris normalised: x={ex/S:.4f} y={ey/S:.4f}  (n={sel.sum()})')
else:
    print('  no irises detected')
print('canvas side', S)
