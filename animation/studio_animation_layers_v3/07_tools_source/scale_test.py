import sys
import numpy as np
from PIL import Image, ImageDraw
R = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_revised_pack_v2/studio_animation_revised_pack/01_character_frames_aligned/'
P = '/Users/nikolaiarsenov/Downloads/handoff-web-project/05_previous_chair_materials/'
bg = Image.open('work/bg.png').convert('RGBA')
back = Image.open(P + 'chair_back_rear_draft.png').convert('RGBA'); front = Image.open(P + 'chair_seat_front_draft.png').convert('RGBA')
GROUP_B = 1.22
def load(name, H):
    im = Image.open(R + name).convert('RGBA')
    s = H / 370 * (GROUP_B if name.startswith(('walk', 'lean')) else 1.0)
    im = im.crop(im.getbbox())
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
def place(canvas, im, cx, foot_y, crop_h=None):
    if crop_h: im = im.crop((0, 0, im.width, crop_h))
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(foot_y - im.height) if not crop_h else int(foot_y)))
outs = []
for H in (400, 425):
    c = bg.copy()
    # standing behind chair (back view), feet y 722
    st = load('walk_away/walk_away_01.png', H); place(c, st, 640, 722)
    # seated: head top ~50px above backrest top (472)
    se = load('walk_away/walk_away_01.png', H); c.alpha_composite(se.crop((0, 0, se.width, 140)), (int(488 - se.width / 2), 472 - 52))
    c.alpha_composite(back); c.alpha_composite(front)
    place(c, load('walk_side/walk_01.png', H), 880, 755)
    place(c, load('idle/idle_profile.png', H), 1120, 755)
    place(c, load('lean_inspect/lean_inspect_03.png', H), 1230, 755)
    d = ImageDraw.Draw(c); d.text((20, 20), f'H={H}', fill=(255, 255, 0))
    outs.append(c.crop((300, 250, 1560, 800)))
S = Image.new('RGB', (outs[0].width, outs[0].height * 2))
for i, o in enumerate(outs): S.paste(o.convert('RGB'), (0, i * o.height))
S.save('work/scale_test.png')
