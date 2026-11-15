import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
cur = np.asarray(Image.open('work/clean_chair_v2.png').convert('RGB')).astype(float)
m = np.load('work/chair_inpaint_mask2.npy')
H, W = m.shape
X0, X1, Y0, Y1 = 398, 552, 498, 526
band = np.zeros((Y1 - Y0, X1 - X0, 3))
for i, y in enumerate(range(Y0, Y1)):
    L = np.median(orig[y, 399:409], 0); R = np.median(orig[y, 584:600], 0)
    t = np.linspace(0, 1, X1 - X0)[:, None]
    band[i] = L * (1 - t) + R * t
# soft vertical darkening right under the monitors (contact shadow)
sh = np.clip(1 - (np.arange(Y1 - Y0) / 6.0), 0, 1)[:, None, None] * 0.35
band *= (1 - sh)
# light texture from lit wall patch (high-pass, clipped)
patch = orig[498:530, 600:690]
hp = patch - ndimage.gaussian_filter(patch, (3, 3, 0))
hp = ndimage.gaussian_filter(np.clip(hp, -5, 5), (0.7, 0.7, 0))
tile = np.concatenate([hp, hp[:, ::-1]], 1)
while tile.shape[1] < band.shape[1]: tile = np.concatenate([tile, tile], 1)
band += tile[:band.shape[0], :band.shape[1]] * 0.4
canvas = cur.copy()
region = np.zeros((H, W), bool); region[Y0:Y1, X0:X1] = True
# left part down to slab/desk (x 398..459, y 523..529) also wall
band2 = np.repeat(band[-1:], 3, 0)[:, :61]
paint = canvas.copy()
paint[Y0:Y1, X0:X1] = band
paint[526:529, 398:459] = band2
region[526:529, 398:459] = True
# slab (tablet) extension: copy slab rows 528..542 from x 380..412, continue to x 432, add mirrored cap
slab = orig[528:542, 384:404]
for xs in range(404, 459, 20):
    w = min(20, 459 - xs); paint[528:542, xs:xs + w] = slab[:, :w]
region[528:542, 404:459] = True
img = Image.fromarray(np.clip(paint, 0, 255).astype(np.uint8))
# cables (dark outline style), supersampled
S = 4
lay = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
def cable(pts, w=2.2, col=(28, 18, 18, 255)):
    d.line([(x * S, y * S) for x, y in pts], fill=col, width=int(w * S), joint='curve')
import math
def bez(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]
cable(bez((520, 498), (532, 512), (512, 523)))
cable(bez((447, 498), (436, 511), (446, 528)))
cable(bez((492, 498), (499, 507), (486, 523)), w=1.6)
lay = lay.resize((W, H), Image.LANCZOS)
img = img.convert('RGBA'); img.alpha_composite(lay); paint = np.asarray(img.convert('RGB')).astype(float)
# only apply where chair inpaint mask, feather 2px
kbtop = np.zeros_like(m); kbtop[523:526, 440:552] = True
apply = (region & (m | kbtop)).astype(float)
apply = ndimage.gaussian_filter(apply, 0.8) * (m | kbtop)
out = cur * (1 - apply[..., None]) + paint * apply[..., None]
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save('work/clean_chair_v3.png')
