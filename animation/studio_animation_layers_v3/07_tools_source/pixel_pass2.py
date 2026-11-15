import json
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
from scipy import ndimage
OUTC = np.array([20, 14, 14])
def crisp(im, colors=24, palette=None, sat=1.0, gain=1.0):
    im = im.convert('RGBA'); a = np.asarray(im).astype(float); solid = a[..., 3] >= 120
    rgb = Image.fromarray(np.clip(a[..., :3] * gain, 0, 255).astype(np.uint8), 'RGB')
    if sat != 1.0: rgb = ImageEnhance.Color(rgb).enhance(sat)
    q = rgb.quantize(palette=palette, dither=Image.Dither.NONE) if palette else rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    r = np.asarray(q.convert('RGB')).astype(float)
    edge = solid & ndimage.binary_dilation(~solid); dk = edge & (r.mean(-1) > 60); r[dk] = r[dk] * 0.3 + OUTC * 0.7
    o = np.dstack([r, solid * 255]).astype(np.uint8); o[~solid] = 0; return Image.fromarray(o, 'RGBA')
def palette_from(images, colors):
    px = np.concatenate([np.asarray(i)[..., :3][np.asarray(i)[..., 3] > 128] for i in images])[None]
    return Image.fromarray(px.astype(np.uint8), 'RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
# dog: crisp at native resolution, shared palette, a bit warmer/saturated
names = json.load(open('work/dog_states.json')); sheet = Image.open('work/dog_sheet.png').convert('RGBA')
crops = [sheet.crop(((i % 10) * 80 + 6, (i // 10) * 120 + 4, (i % 10) * 80 + 74, (i // 10) * 120 + 108)) for i in range(len(names))]
crops = [Image.fromarray(np.dstack([np.asarray(ImageEnhance.Color(c.convert('RGB')).enhance(1.25)), np.asarray(c)[..., 3]]), 'RGBA') for c in crops]
pal = palette_from(crops, 28)
for n, c in zip(names, crops): crisp(c, palette=pal, gain=0.94).save(f'work/v4/dog/{n}.png')
# ball: crisp native frames
R_, S2 = 15, 8; base = Image.new('RGBA', (2 * R_ * S2 + 16, 2 * R_ * S2 + 16), (0, 0, 0, 0)); bd = ImageDraw.Draw(base); B = [8, 8, 8 + 2 * R_ * S2, 8 + 2 * R_ * S2]
bd.ellipse(B, fill=(174, 186, 48, 255)); bd.ellipse([40, 30, 2 * R_ * S2 - 60, 2 * R_ * S2 - 70], fill=(206, 214, 84, 255))
bd.arc([-60, 40, 130, 236], -58, 58, fill=(238, 234, 198, 255), width=15); bd.arc([126, 24, 316, 220], 122, 238, fill=(238, 234, 198, 255), width=15)
bd.ellipse(B, outline=(28, 24, 16, 255), width=14)
for k in range(8): crisp(base.rotate(-45 * k, resample=Image.BICUBIC).resize((32, 32), Image.LANCZOS), colors=6).save(f'work/v4/ball/ball_{k}.png')
# legs: crisp version of the procedural legs
crisp(Image.open('work/v3/sit_rear_legs.png'), colors=10).save('work/v4/sit_rear_legs.png')
# arms: drawn aliased at native resolution (hand on the right part of the keyboard; left elbow at the backrest edge)
OUT, BASE, SH, HI, SK, SKS = (16, 12, 14), (38, 33, 36), (26, 22, 25), (64, 57, 62), (222, 168, 132), (176, 120, 92)
def tube(pts, w0, w1):
    pts = np.array(pts, float); n = len(pts); L, R = [], []
    for i in range(n):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, n - 1)]; t = (b - a) / (np.linalg.norm(b - a) + 1e-6); nr = np.array([-t[1], t[0]]); w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append(pts[i] + nr * w); R.append(pts[i] - nr * w)
    return [tuple(p) for p in L + R[::-1]]
def bez(p0, p1, p2, n=16):
    t = np.linspace(0, 1, n)[:, None]; p0, p1, p2 = map(np.array, (p0, p1, p2)); return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
def draw_part(box, parts, details):
    x0, y0, x1, y1 = box; im = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = lambda poly: [(x - x0, y - y0) for x, y in poly]
    for poly, fill in parts: d.polygon(sh(poly), fill=fill + (255,), outline=OUT + (255,), width=2)
    for kind, pts, col, w in details:
        if kind == 'line': d.line(sh(pts), fill=col + (255,), width=w)
        else: d.ellipse(sh(pts), fill=col + (255,), outline=OUT + (255,), width=2)
    return im
RB = (510, 476, 604, 562)
upper = tube(bez((535, 489), (556, 512), (563, 548)), 23, 18); fore = tube(bez((563, 548), (572, 541), (582, 534)), 17, 14)
cuff = [(577, 528), (587, 527), (589, 538), (579, 540)]
arm_r = draw_part(RB, [(upper, BASE), (fore, BASE), (cuff, (46, 40, 44))],
                  [('line', [tuple(p) for p in bez((545, 494), (558, 512), (563, 540))], HI, 2), ('line', [(551, 524), (557, 522)], SH, 2), ('line', [(556, 536), (562, 533)], SH, 2),
                   ('ell', [(584, 526), (597, 535)], SK, 0), ('line', [(588, 529), (594, 529)], SKS, 1)])
arm_r.save('work/v4/sit_rear_arm_right.png')
LB = (392, 484, 452, 562)
left = tube(np.vstack([bez((446, 493), (414, 500), (406, 532)), bez((406, 532), (408, 548), (432, 552))[1:]]), 21, 16)
arm_l = draw_part(LB, [(left, BASE)], [('line', [tuple(p) for p in bez((432, 498), (414, 506), (410, 528))], HI, 2)])
arm_l.save('work/v4/sit_rear_arm_left.png')
json.dump(dict(arm_right=list(RB[:2]), arm_left=list(LB[:2]), dog_frame=[68, 104], dog_crop_offset=[-4, -6], ball=[32, 32]), open('work/v4/meta.json', 'w'))
print('ok')
