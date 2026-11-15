import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
OUTC = np.array([20, 14, 14])
def pixelize(im, palette_img=None, colors=20, outline=True):
    im = im.convert('RGBA'); W, H = im.size; W2, H2 = (W + 1) // 2, (H + 1) // 2
    a = np.asarray(im).astype(float); al = a[..., 3:4] / 255
    pm = Image.fromarray(np.dstack([a[..., :3] * al, a[..., 3:]]).astype(np.uint8), 'RGBA').resize((W2, H2), Image.BOX)
    s = np.asarray(pm).astype(float); A = s[..., 3]; rgb = s[..., :3] / np.maximum(A[..., None] / 255, 1e-3)
    solid = A >= 110
    rgbim = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), 'RGB')
    q = rgbim.quantize(palette=palette_img, dither=Image.Dither.NONE) if palette_img else rgbim.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    rgb = np.asarray(q.convert('RGB')).astype(float)
    if outline:
        edge = solid & ndimage.binary_dilation(~solid)
        lum = rgb.mean(-1); darken = edge & (lum > 70)
        rgb[darken] = rgb[darken] * 0.25 + OUTC * 0.75
    out = np.dstack([rgb, solid * 255]).astype(np.uint8); out[~solid] = 0
    return Image.fromarray(out, 'RGBA').resize((W2 * 2, H2 * 2), Image.NEAREST)
def palette_from(images, colors):
    strip = np.concatenate([np.asarray(i.convert('RGBA'))[..., :3][np.asarray(i.convert('RGBA'))[..., 3] > 128] for i in images])[None]
    return Image.fromarray(strip.astype(np.uint8), 'RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
# ---------------- dog sprite frames
names = json.load(open('work/dog_states.json')); sheet = Image.open('work/dog_sheet.png').convert('RGBA')
crops = []
for i, n in enumerate(names):
    x, y = (i % 10) * 80 + 10, (i // 10) * 120 + 10
    crops.append(sheet.crop((x - 4, y - 6, x + 64, y + 98)))
pal = palette_from(crops, 22)
for n, c in zip(names, crops): pixelize(c, pal).save(f'work/v4/dog/{n}.png')
# ---------------- seated arms (re-posed: elbow down at the armrest, forearm up to the mouse)
S = 4
def bez(p0, p1, p2, n=30):
    t = np.linspace(0, 1, n)[:, None]; p0, p1, p2 = map(np.array, (p0, p1, p2)); return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
def tube(d, pts, w0, w1, fill, ox, oy):
    pts = np.array(pts); n = len(pts); L, R = [], []
    for i in range(n):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, n - 1)]; t = (b - a) / (np.linalg.norm(b - a) + 1e-6); nr = np.array([-t[1], t[0]]); w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append(pts[i] + nr * w); R.append(pts[i] - nr * w)
    poly = [((x - ox) * S, (y - oy) * S) for x, y in L + R[::-1]]; d.polygon(poly, fill=fill); return poly
HOOD, HI, SK, SKS = (34, 29, 32, 255), (66, 58, 64, 255), (224, 170, 134, 255), (176, 120, 92, 255)
BX0, BY0, BX1, BY1 = 516, 474, 648, 590
im = Image.new('RGBA', ((BX1 - BX0) * S, (BY1 - BY0) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
P = lambda pts: [((x - BX0) * S, (y - BY0) * S) for x, y in pts]
tube(d, bez((534, 488), (566, 520), (574, 566)), 25, 20, HOOD, BX0, BY0)                       # upper arm down to the elbow
tube(d, bez((574, 566), (594, 556), (620, 541)), 19, 14, HOOD, BX0, BY0)                       # forearm up toward the mouse
d.ellipse(P([(564, 554), (586, 578)]), fill=HOOD)                                              # elbow
d.line(P(bez((546, 492), (568, 520), (576, 556))), fill=HI, width=int(2 * S))                  # rim light
d.line(P([(586, 560), (608, 548)]), fill=HI, width=int(1.6 * S))
d.polygon(P([(612, 533), (622, 532), (624, 545), (614, 547)]), fill=(46, 40, 44, 255))           # cuff
d.ellipse(P([(619, 530), (637, 542)]), fill=SK); d.line(P([(624, 534), (634, 533)]), fill=SKS, width=int(1.4 * S))
arm_r = pixelize(im.resize((BX1 - BX0, BY1 - BY0), Image.LANCZOS), colors=8)
arm_r.save('work/v4/sit_rear_arm_right.png')
LX0, LY0, LX1, LY1 = 390, 482, 452, 562
im = Image.new('RGBA', ((LX1 - LX0) * S, (LY1 - LY0) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
tube(d, np.vstack([bez((446, 492), (414, 500), (406, 532)), bez((406, 532), (408, 548), (434, 552))[1:]]), 22, 17, HOOD, LX0, LY0)
d.line([((x - LX0) * S, (y - LY0) * S) for x, y in bez((432, 497), (414, 506), (410, 528))], fill=HI, width=int(1.8 * S))
arm_l = pixelize(im.resize((LX1 - LX0, LY1 - LY0), Image.LANCZOS), colors=6); arm_l.save('work/v4/sit_rear_arm_left.png')
# ---------------- seated legs (pixelized version of the procedural legs)
pixelize(Image.open('work/v3/sit_rear_legs.png'), colors=10).save('work/v4/sit_rear_legs.png')
# ---------------- ball rotation frames
R_, S2 = 16, 8; base = Image.new('RGBA', (2 * R_ * S2, 2 * R_ * S2), (0, 0, 0, 0)); bd = ImageDraw.Draw(base); box = [4, 4, 2 * R_ * S2 - 4, 2 * R_ * S2 - 4]
bd.ellipse(box, fill=(176, 188, 50, 255)); bd.ellipse([30, 20, 2 * R_ * S2 - 70, 2 * R_ * S2 - 80], fill=(208, 216, 86, 255))
bd.arc([-70, 34, 124, 240], -60, 60, fill=(238, 234, 198, 255), width=16); bd.arc([136, 14, 330, 224], 120, 240, fill=(238, 234, 198, 255), width=16)
for k in range(8):
    fr = base.rotate(-45 * k, resample=Image.BICUBIC).resize((2 * R_, 2 * R_), Image.LANCZOS)
    pixelize(fr, colors=6).save(f'work/v4/ball/ball_{k}.png')
json.dump(dict(arm_right=[BX0, BY0], arm_left=[LX0, LY0], dog_frame=[68, 104], dog_crop_offset=[-4, -6], ball=[32, 32]), open('work/v4/meta.json', 'w'))
print('pixel pass ok')
