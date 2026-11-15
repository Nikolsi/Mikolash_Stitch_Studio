import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
CW, CH, AX, AY = 320, 440, 160, 430
def load(n): return np.asarray(Image.open(f'work/char/{n}.png').convert('RGBA')).copy()
def save(a, n):
    os.makedirs(os.path.dirname(f'work/char/{n}.png'), exist_ok=True); Image.fromarray(a, 'RGBA').save(f'work/char/{n}.png', optimize=True)
def stack(*ls):
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    for l in ls: c.alpha_composite(l if isinstance(l, Image.Image) else Image.fromarray(l, 'RGBA'))
    return np.asarray(c).copy()
def rot(a, deg, pivot):   # PIL: positive = counter-clockwise
    return Image.fromarray(a, 'RGBA').rotate(deg, resample=Image.BICUBIC, center=tuple(pivot))
lum = lambda a: a[..., :3].astype(int).mean(-1)
# ================= machine lean rig (from lean_inspect_03) =================
L3 = load('lean_inspect/lean_inspect_03'); al = L3[..., 3] > 0
r, g, b = (L3[..., i].astype(int) for i in range(3))
yy, xx = np.mgrid[:CH, :CW]
skin = al & (r > 140) & (r - b > 40) & (g > 80) & (yy > 212) & (yy < 285)
hood_black = al & (lum(L3) < 40) & ((r - b) < 25)
BOX = (xx >= 145) & (xx <= 202) & (yy >= 212) & (yy <= 285)
hand = ndimage.binary_dilation(skin, iterations=2) & al & BOX & ((lum(L3) < 60) | skin)
lab_s, _ = ndimage.label(hood_black & (yy < 250))
top_ids = set(np.unique(lab_s[(yy < 228) & (lab_s > 0)]))
sleeve = np.isin(lab_s, list(top_ids)) & BOX
torso = al & ((yy < 228) | hand | sleeve)
legs = al & ~torso
# front boot = tan/sole pixels of the right-hand boot near the floor
tan = al & (r > 120) & (r - b > 50) & (g > 70) & (r > g) & (yy > 385)
lab, n = ndimage.label(ndimage.binary_dilation(tan, iterations=1))
ys, xs = np.nonzero(tan); split = 150
front = np.zeros_like(al); front[385:, split:] = True
front = (front & legs & (ndimage.binary_dilation(tan & (xx >= split), iterations=3))) | (legs & (yy >= 397) & (xx >= split))
legs_only = legs & ~front
def part(mask):
    p = L3.copy(); p[~mask] = 0; return p
P_torso, P_legs, P_boot = part(torso), part(legs_only), part(front)
# pad pants upward under the hoodie hem so a rotated torso never opens a gap
R = 268
ext = np.zeros_like(P_legs)
row = np.nonzero(legs_only[R])[0]
for x in range(row.min(), row.max() + 1):
    colpx = P_legs[R - 4:R + 6, x]; colpx = colpx[colpx[:, 3] > 200]
    if not len(colpx): continue
    c = np.median(colpx[:, :3], 0).astype(np.uint8)
    ext[214:R, x] = [*c, 255]
base_im = Image.fromarray(ext, 'RGBA'); base_im.alpha_composite(Image.fromarray(P_legs, 'RGBA'))
P_legs = np.asarray(base_im).copy()
HIP = [140, 244]; HEEL = [int(xs[xs >= split].min()) + 4 if (xs >= split).any() else 160, 428]
save(P_torso, 'lean_rig/lean_rig_torso'); save(P_legs, 'lean_rig/lean_rig_legs'); save(P_boot, 'lean_rig/lean_rig_front_boot')
frames = {}
for name, ang in (('lean_rig_00_upright', 18), ('lean_rig_01_half', 9), ('lean_rig_02_inspect', 0)):
    fr = stack(P_legs, P_boot, rot(P_torso, ang, HIP)); save(fr, f'lean_rig/{name}'); frames[name] = ang
tap = stack(P_legs, rot(P_boot, 7, HEEL), P_torso); save(tap, 'lean_rig/lean_rig_02_inspect_tap')
# ================= seated legs (from walk_away_01, back view) =================
W1 = load('walk_away/walk_away_01'); a1 = W1[..., 3] > 0
# planted (right-hand) lower leg: columns right of the stride gap, knee down
leg = W1.copy(); keep = a1 & (yy > 318) & (xx > 140); leg[~keep] = 0
bb = Image.fromarray(leg, 'RGBA').getbbox(); leg_im = Image.fromarray(leg, 'RGBA').crop(bb)
legL = leg_im.transpose(Image.FLIP_LEFT_RIGHT)
meta_sit = json.load(open('work/sit_rear_meta.json'))
FOOT_Y = 420            # canvas row of soles when seated (scene y 712 with anchor at 722)
def legs_layer():
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    for im, cx in ((legL, 146), (leg_im, 200)):
        c.alpha_composite(im, (int(cx - im.width / 2), FOOT_Y - im.height))
    return c
LEGS = legs_layer(); LEGS.save('work/char/sit_rear/sit_rear_legs.png', optimize=True)
head1 = Image.open('work/char/sit_rear/sit_rear_head.png'); head2 = Image.open('work/char/sit_rear/sit_rear_head_turn_right.png'); body = Image.open('work/char/sit_rear/sit_rear_body.png')
save(stack(LEGS, head1, body), 'sit_rear/sit_rear_01'); save(stack(LEGS, head2, body), 'sit_rear/sit_rear_02_look_right')
for n in ('rise_rear_01', 'rise_rear_02'):
    base = Image.open(f'work/char/sit_rear/{n}.png')
    if not os.path.exists(f'work/char/sit_rear/{n}_nolegs.png'): base.save(f'work/char/sit_rear/{n}_nolegs.png')
    base = Image.open(f'work/char/sit_rear/{n}_nolegs.png')
    save(stack(LEGS, base), f'sit_rear/{n}')
json.dump(dict(lean_rig=dict(hip_pivot_canvas=HIP, heel_pivot_canvas=HEEL, torso_angles_deg_ccw=frames, tap_deg_ccw=7,
                             note='legs fixed; torso rotates around the hip; front boot rotates around the heel (toe up) for foot tapping'),
               sit_legs=dict(foot_row_canvas=FOOT_Y, leg_centres_canvas=[146, 200], source='walk_away_01 planted lower leg + mirror')),
          open('work/rigs_v2_meta.json', 'w'), indent=1)
print('HIP', HIP, 'HEEL', HEEL, 'torso px', int(torso.sum()), 'boot px', int(front.sum()))
