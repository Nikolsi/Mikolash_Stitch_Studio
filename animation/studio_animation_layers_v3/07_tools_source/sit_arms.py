import json, os
import numpy as np
from PIL import Image, ImageDraw
D = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
O = 'work/v3'
S = 4
def bez(p0, p1, p2, n=30):
    t = np.linspace(0, 1, n)[:, None]; p0, p1, p2 = map(np.array, (p0, p1, p2))
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2
def tube(d, pts, w0, w1, fill, outline, ox, oy):
    pts = np.array(pts); n = len(pts); left, right = [], []
    for i in range(n):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, n - 1)]; t = b - a; t = t / (np.linalg.norm(t) + 1e-6); nrm = np.array([-t[1], t[0]])
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append(pts[i] + nrm * w); right.append(pts[i] - nrm * w)
    poly = [((x - ox) * S, (y - oy) * S) for x, y in left + right[::-1]]
    d.polygon(poly, fill=fill); d.line(poly + [poly[0]], fill=outline, width=int(1.5 * S), joint='curve')
    return left, right
HOOD = (30, 26, 29, 255); HOOD_HI = (58, 50, 55, 255); OUT = (12, 10, 12, 255); SKIN = (222, 168, 132, 255); SKIN_SH = (178, 120, 92, 255)
# ---- right arm reaching the mouse (scene coords), drawn in its own box
BX0, BY0, BX1, BY1 = 520, 470, 650, 552
im = Image.new('RGBA', ((BX1 - BX0) * S, (BY1 - BY0) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
up = bez((530, 486), (566, 494), (582, 520)); fore = bez((582, 520), (598, 532), (621, 533))
tube(d, np.vstack([up, fore[1:]]), 24, 15, HOOD, OUT, BX0, BY0)
P = lambda pts: [((x - BX0) * S, (y - BY0) * S) for x, y in pts]
d.line(P(bez((540, 490), (565, 496), (578, 516))), fill=HOOD_HI, width=int(1.6 * S))
for a, b in (((570, 508), (582, 503)), ((586, 523), (592, 517)), ((596, 529), (600, 524))):
    d.line(P([a, b]), fill=OUT, width=int(1.1 * S))
d.rounded_rectangle(P([(611, 526.5), (621, 538.5)]), radius=2 * S, fill=(40, 34, 38, 255), outline=OUT, width=int(1.2 * S))  # cuff
d.ellipse(P([(619, 529), (637, 541)]), fill=SKIN, outline=OUT, width=int(1.3 * S))                                            # hand on the mouse
d.line(P([(626, 531), (632, 530.5)]), fill=SKIN_SH, width=int(1.0 * S)); d.line(P([(624, 535), (634, 534)]), fill=SKIN_SH, width=int(1.0 * S))
arm_r = im.resize((BX1 - BX0, BY1 - BY0), Image.LANCZOS); arm_r.save(f'{O}/sit_rear_arm_right.png')
# ---- left elbow sticking out beside the backrest
LX0, LY0, LX1, LY1 = 392, 480, 452, 560
im = Image.new('RGBA', ((LX1 - LX0) * S, (LY1 - LY0) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
el = np.vstack([bez((444, 490), (412, 500), (404, 532)), bez((404, 532), (406, 548), (432, 550))[1:]])
tube(d, el, 22, 16, HOOD, OUT, LX0, LY0)
P2 = lambda pts: [((x - LX0) * S, (y - LY0) * S) for x, y in pts]
d.line(P2(bez((430, 496), (412, 506), (408, 528))), fill=HOOD_HI, width=int(1.5 * S))
arm_l = im.resize((LX1 - LX0, LY1 - LY0), Image.LANCZOS); arm_l.save(f'{O}/sit_rear_arm_left.png')
meta = json.load(open('work/sit_rear_meta.json'))
meta['arms'] = dict(right=dict(file='02_character_frames/sit_rear/sit_rear_arm_right.png', scene_xy=[BX0, BY0], canvas_xy=[BX0 - 316, BY0 - 292], motion='mouse: tiny 1 px moves'),
                    left=dict(file='02_character_frames/sit_rear/sit_rear_arm_left.png', scene_xy=[LX0, LY0], canvas_xy=[LX0 - 316, LY0 - 292], motion='typing: elbow jitter ≤0.6 px'),
                    note='positions relative to the 320x440 character box when the sit anchor is (476,722); fade out during rise')
json.dump(meta, open('work/sit_rear_meta.json', 'w'), indent=1)
# composite seated frames for docs (legs + arms + head + body) on an extended canvas is not needed: arms are separate parts
print(meta['arms'])
