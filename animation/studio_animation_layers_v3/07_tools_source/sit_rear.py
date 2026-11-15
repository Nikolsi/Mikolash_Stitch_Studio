import json, os
import numpy as np
from PIL import Image
CW, CH, AX, AY = 320, 440, 160, 430
DROP = 58          # seated = standing-behind-chair sprite lowered by DROP px
CUT_SCENE = 640    # nothing below seat level (scene y) when the anchor is at y=722
ANCHOR_Y_SCENE = 722
cut_canvas = CUT_SCENE - (ANCHOR_Y_SCENE - AY) - DROP   # canvas row in the lowered sprite
src1 = np.asarray(Image.open('work/char/walk_away/walk_away_01.png')).copy()
src2 = np.asarray(Image.open('work/char/walk_away/walk_away_02.png')).copy()
NECK1, NECK2 = 113, 123      # head/hood boundary rows in each source frame (canvas coords)
def is_hair_skin(px):
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    lum = (r + g + b) / 3; return (r - b > 18) & (lum > 42)
def head_part(src, neck):
    h = src.copy(); h[neck + 10:] = 0
    return h
def body_part(src, neck):
    b = src.copy(); b[:neck] = 0
    band = b[neck:neck + 10]; hs = is_hair_skin(band) & (band[..., 3] > 0); band[hs] = 0
    return b
def shift(a, dx, dy):
    out = np.zeros_like(a); H, W = a.shape[:2]
    ys, xs = slice(max(0, dy), min(H, H + dy)), slice(max(0, dx), min(W, W + dx))
    ys2, xs2 = slice(max(0, -dy), min(H, H - dy)), slice(max(0, -dx), min(W, W - dx))
    out[ys, xs] = a[ys2, xs2]; return out
head1 = shift(head_part(src1, NECK1), 0, DROP)
body1 = shift(body_part(src1, NECK1), 0, DROP); body1[cut_canvas:] = 0
# head turned right: align neck point of frame 2 to frame 1
def neck_x(src, neck):
    row = src[neck - 4:neck + 2, :, 3] > 128; xs = np.nonzero(row)[1]; return int(round(xs.mean()))
dx = neck_x(src1, NECK1) - neck_x(src2, NECK2); dy = NECK1 - NECK2
head2 = shift(head_part(src2, NECK2), dx, dy + DROP)
os.makedirs('work/char/sit_rear', exist_ok=True)
def save(a, n): Image.fromarray(a, 'RGBA').save(f'work/char/sit_rear/{n}.png', optimize=True)
save(head1, 'sit_rear_head'); save(head2, 'sit_rear_head_turn_right'); save(body1, 'sit_rear_body')
def stack(*layers):
    c = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    for l in layers: c.alpha_composite(Image.fromarray(l, 'RGBA'))
    return np.asarray(c)
save(stack(head1, body1), 'sit_rear_01'); save(stack(head2, body1), 'sit_rear_02_look_right')
# rise frames: full standing sprite lowered, cut at the floor line (AY) and at seat for the lowest one
for i, k in enumerate((2 / 3, 1 / 3), 1):
    d = int(round(DROP * k)); fr = shift(src1, 0, d); fr[CUT_SCENE - (ANCHOR_Y_SCENE - AY) - d:] = 0
    save(fr, f'rise_rear_0{i}')
pivot = [neck_x(src1, NECK1), NECK1 + DROP]
json.dump(dict(DROP=DROP, cut_canvas_row=cut_canvas, head_pivot_canvas=pivot, head_turn_offset=[dx, dy]), open('work/sit_rear_meta.json', 'w'))
print('pivot', pivot, 'turn offset', dx, dy, 'cut row', cut_canvas)
