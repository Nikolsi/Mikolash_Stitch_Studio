import json, os, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
D = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
O = 'work/v3'
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
H, W = orig.shape[:2]
yy, xx = np.mgrid[:H, :W]
def save_rgba(a, p): Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(p, optimize=True)
def diff_matte(o, c, region, lo=14, span=70):
    d = np.abs(o - c).sum(-1); a = np.clip((d - lo) / span, 0, 1) * region
    a3 = np.maximum(a, 1e-3)[..., None]; col = np.clip((o - (1 - a3) * c) / a3, 0, 255)
    out = np.dstack([col, a * 255]); out[a == 0] = 0; return out
# ---------------- 1) seated legs seen from behind (procedural, supersampled) ----------------
S = 4; CW, CH = 320, 440
im = Image.new('RGBA', (CW * S, CH * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
P = lambda pts: [(x * S, y * S) for x, y in pts]
OUT = (22, 20, 24, 255); BASE = (54, 54, 62); DARK = (36, 36, 42); LIGHT = (74, 74, 84)
TAN = (178, 124, 66, 255); TAN_HI = (208, 154, 92, 255); SOLE = (52, 36, 28, 255)
for cx, side in ((142, -1), (204, 1)):
    top, hem = 344, 414
    # floor contact shadow
    d.ellipse(P([(cx - 17, 416), (cx + 17, 424)]), fill=(10, 6, 6, 90))
    # heel block (only the back of the boot shows under the hem)
    d.rounded_rectangle(P([(cx - 11, 409), (cx + 11, 420)]), radius=3 * S, fill=TAN, outline=OUT, width=int(1.4 * S))
    d.rectangle(P([(cx - 10, 410.5), (cx + 10, 413)]), fill=TAN_HI)
    d.rectangle(P([(cx - 10.5, 417.5), (cx + 10.5, 420)]), fill=SOLE)
    # trouser leg: slightly flared, hem breaking over the heel
    leg = [(cx - 14, top), (cx + 14, top), (cx + 15.5, hem - 14), (cx + 16, hem - 3), (cx + 11, hem + 1.5), (cx + 3, hem - 0.5), (cx - 6, hem + 1.5), (cx - 16, hem - 3), (cx - 15.5, hem - 14)]
    d.polygon(P(leg), fill=BASE + (255,))
    inner = [(cx - side * 16, top), (cx - side * 6, top), (cx - side * 7, hem), (cx - side * 17, hem - 2)]
    d.polygon(P(inner), fill=DARK + (255,))
    d.polygon(P([(cx - 3, top), (cx + 4, top), (cx + 3, hem - 4), (cx - 2, hem - 4)]), fill=LIGHT + (255,))
    for (x0, y0, x1, y1) in ((cx - 12, hem - 9, cx + 2, hem - 5), (cx + 1, hem - 7, cx + 13, hem - 10), (cx - 9, hem - 16, cx + 6, hem - 13)):
        d.line(P([(x0, y0), (x1, y1)]), fill=(28, 28, 33, 255), width=int(1.2 * S))
    # side stripes (outer edge)
    ox = cx + side * 13.5
    for k in (0, 2.4):
        d.line(P([(ox - side * k, top), (ox - side * k + side * 0.8, hem - 2)]), fill=(222, 222, 226, 255), width=int(1.1 * S))
    d.line(P(leg + [leg[0]]), fill=OUT, width=int(1.5 * S), joint='curve')
legs = im.resize((CW, CH), Image.LANCZOS)
la = np.asarray(legs).astype(float); la[..., :3] *= 0.62          # under-desk shade
legs = Image.fromarray(la.astype(np.uint8), 'RGBA'); legs.save(f'{O}/sit_rear_legs.png', optimize=True)
SR = f'{D}/02_character_frames/sit_rear'
def stack(*ls):
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    for l in ls: c.alpha_composite(l)
    return c
hd, ht, bd = (Image.open(f'{SR}/{n}.png') for n in ('sit_rear_head', 'sit_rear_head_turn_right', 'sit_rear_body'))
stack(legs, hd, bd).save(f'{O}/sit_rear_01.png', optimize=True); stack(legs, ht, bd).save(f'{O}/sit_rear_02_look_right.png', optimize=True)
for n in ('rise_rear_01', 'rise_rear_02'):
    stack(legs, Image.open(f'work/char/sit_rear/{n}_nolegs.png')).save(f'{O}/{n}.png', optimize=True)
# ---------------- 2) single active needle ----------------
nd = np.asarray(Image.open(f'{D}/01_scene_layers/02_machine_needles.png')).copy()
act = np.zeros_like(nd); act[:, 1378:1383] = nd[:, 1378:1383]; st = nd.copy(); st[:, 1378:1383] = 0
save_rgba(st, f'{O}/02_machine_needles_static.png'); save_rgba(act, f'{O}/02b_machine_needle_active.png')
# ---------------- 3) neon sign as its own layer + clean wall ----------------
clean = np.asarray(Image.open(f'{D}/01_scene_layers/00_background_clean_plate.png').convert('RGB')).astype(float)
r, g, b = orig[..., 0], orig[..., 1], orig[..., 2]
zone = (xx > 380) & (xx < 655) & (yy > 118) & (yy < 318)
pink = zone & (((b - g) > 30) | ((r > 180) & (b > 140)))
nm = ndimage.binary_dilation(pink, iterations=5) & zone
np.save(f'{O}/neon_mask.npy', nm)
Image.fromarray(clean.astype(np.uint8)).save(f'{O}/tmp_clean.png')
subprocess.run(['.venv/bin/python', '-I', 'lama.py', f'{O}/tmp_clean.png', f'{O}/neon_mask.npy', f'{O}/clean_v3.png', '264', '0', '776', '512'], check=True, capture_output=True)
clean3 = np.asarray(Image.open(f'{O}/clean_v3.png').convert('RGB')).astype(float)
neon = diff_matte(orig, clean3, nm, lo=10, span=60)
save_rgba(neon, f'{O}/00b_neon_sign.png')
# ---------------- 4) ball: remove from bed (LaMa) + procedural full ball ----------------
ballm = (((xx - 311) ** 2 / 21 ** 2 + (yy - 845) ** 2 / 15 ** 2) <= 1) & (yy < 859)
np.save(f'{O}/ball_mask.npy', ballm)
subprocess.run(['.venv/bin/python', '-I', 'lama.py', f'{O}/clean_v3.png', f'{O}/ball_mask.npy', f'{O}/clean_v3.png', '56', '429', '568', '941'], check=True, capture_output=True)
clean3 = np.asarray(Image.open(f'{O}/clean_v3.png').convert('RGB')).astype(float)
R_ = 15; S2 = 8; bi = Image.new('RGBA', (2 * R_ * S2 + 8, 2 * R_ * S2 + 8), (0, 0, 0, 0)); bd_ = ImageDraw.Draw(bi)
c0 = 4; box = [c0, c0, c0 + 2 * R_ * S2, c0 + 2 * R_ * S2]
bd_.ellipse(box, fill=(170, 182, 48, 255))
bd_.ellipse([c0 + 22, c0 + 14, c0 + 2 * R_ * S2 - 50, c0 + 2 * R_ * S2 - 60], fill=(205, 214, 84, 255))
bd_.arc([c0 - 70, c0 + 30, c0 + 120, c0 + 230], -60, 60, fill=(236, 232, 196, 255), width=14)
bd_.arc([c0 + 130, c0 + 10, c0 + 330, c0 + 220], 120, 240, fill=(236, 232, 196, 255), width=14)
bd_.ellipse(box, outline=(30, 26, 18, 255), width=12)
ball = bi.resize((2 * R_ + 1, 2 * R_ + 1), Image.LANCZOS); ball.save(f'{O}/ball.png')
# ---------------- 5) bed front rim (dog lies inside the bed) ----------------
cl = clean3; lum = cl.mean(-1); sat = cl.max(-1) - cl.min(-1)
bedpx = (xx > 190) & (xx < 440) & (yy > 790) & (yy < 905) & (sat < 75) & ~((cl[..., 0] - cl[..., 2]) > 75)
edge = np.full(W, 830)
for x in range(232, 402):
    col = lum[838:868, x]; edge[x] = 838 + int(np.argmin(col)) - 1
edge[232:402] = ndimage.median_filter(edge[232:402], 9)
outline = (lum < 70) & (xx > 188) & (xx < 442) & (yy > 788) & (yy < 906)
sil = ndimage.binary_fill_holes(ndimage.binary_closing(bedpx | outline, iterations=4))
sil = ndimage.binary_opening(sil, iterations=2)
rim = sil & (yy >= edge[None, :])
rim_rgba = np.dstack([cl, rim * 255.0]); rim_rgba[~rim] = 0
save_rgba(rim_rgba, f'{O}/08_dog_bed_front_rim.png')
json.dump(dict(edge={int(x): int(edge[x]) for x in range(232, 402, 10)}), open(f'{O}/bed_edge.json', 'w'))
# ---------------- 6) content slots: default images from the original art ----------------
slots = {
 'monitor_left':  dict(quad=[[329, 379], [479, 379], [479, 488], [329, 488]], kind='screen'),
 'monitor_right': dict(quad=[[490, 382], [697, 382], [697, 488], [490, 488]], kind='screen'),
 'poster_fuji':   dict(quad=[[738, 229], [844, 229], [844, 335], [738, 335]], kind='poster'),
 'poster_torii':  dict(quad=[[882, 229], [982, 229], [982, 335], [882, 335]], kind='poster'),
 'poster_wave':   dict(quad=[[1018, 228], [1120, 228], [1120, 342], [1018, 342]], kind='poster'),
 'poster_tiger':  dict(quad=[[1390, 154], [1495, 154], [1495, 298], [1390, 298]], kind='poster'),
 'poster_cloud':  dict(quad=[[1526, 218], [1601, 210], [1602, 321], [1527, 327]], kind='poster'),
}
os.makedirs(f'{O}/content', exist_ok=True)
src = cv2.cvtColor(np.asarray(Image.open('work/bg.png').convert('RGB')), cv2.COLOR_RGB2BGR)
for k, v in slots.items():
    q = np.array(v['quad'], np.float32)
    w = int(round(max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3])))); h = int(round(max(np.linalg.norm(q[3] - q[0]), np.linalg.norm(q[2] - q[1]))))
    M = cv2.getPerspectiveTransform(q, np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32))
    out = cv2.warpPerspective(src, M, (w, h), flags=cv2.INTER_CUBIC)
    cv2.imwrite(f'{O}/content/{k}.png', out); v.update(size=[w, h], aspect=round(w / h, 4), file=f'content/{k}.png')
json.dump(slots, open(f'{O}/slots.json', 'w'), indent=1)
print('done')
