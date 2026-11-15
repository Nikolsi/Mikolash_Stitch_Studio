import json, os, shutil, re
from PIL import Image
import numpy as np
ROOT = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
V = 'work/v3'; L = f'{ROOT}/01_scene_layers'
for n in ('00b_neon_sign', '02_machine_needles_static', '02b_machine_needle_active', '08_dog_bed_front_rim'): shutil.copy(f'{V}/{n}.png', f'{L}/{n}.png')
Image.open(f'{V}/clean_v3.png').convert('RGBA').save(f'{L}/00_background_clean_plate.png', optimize=True)
shutil.copy(f'{V}/ball.png', f'{L}/ball.png')
for old in (f'{L}/02_machine_needles.png', f'{ROOT}/03_ambient_overlays/neon_glow.png'):
    if os.path.exists(old): os.remove(old)
for n in ('sit_rear_legs', 'sit_rear_01', 'sit_rear_02_look_right', 'rise_rear_01', 'rise_rear_02', 'sit_rear_head', 'sit_rear_head_turn_right', 'sit_rear_body'): shutil.copy(f'{V}/{n}.png', f'{ROOT}/02_character_frames/sit_rear/{n}.png')
os.makedirs(f'{ROOT}/content', exist_ok=True)
slots = json.load(open(f'{V}/slots.json'))
for k, v in slots.items(): shutil.copy(f'{V}/content/{k}.png', f'{ROOT}/content/{k}.png')
# standalone dog svg for designers
js = open(f'{ROOT}/06_web_preview/dog.js').read(); svg = js[js.index('`') + 1: js.rindex('`')]
os.makedirs(f'{ROOT}/09_dog', exist_ok=True); open(f'{ROOT}/09_dog/yorkie.svg', 'w').write(svg.strip() + '\n')
# manifest tweaks
cm = json.load(open(f'{ROOT}/04_guides/character_manifest.json'))
cm['walk_cycle']['fps'] = 10; cm['walk_cycle']['crossfade'] = 0.6
sm = json.load(open('work/sit_rear_meta.json')); cm['sit_rear'].update(DROP_px=sm['DROP'], head_pivot_canvas=sm['head_pivot_canvas']); cm['sit_rear'].pop('arms', None)
cm['walk_cycle']['note'] = 'Order chosen by planted-foot analysis; advances keep the planted boot within ~±6 px. 10 fps (was 8) — smoother and ~25% faster.'
cm['sit_legs'] = dict(file='02_character_frames/sit_rear/sit_rear_legs.png', note='trouser legs seen from behind + heels only (no toes); drawn procedurally to match the pants; static under the seat')
cm['sit_rear']['rise'] = 'continuous: translate sit rig (head+body) by -DROP over 0.5 s (ease-in-out), legs stay; then switch to walk_away/walk_away_01'
for k in ('rise_rear_01', 'rise_rear_02'): cm['frames'].setdefault(f'sit_rear/{k}', {})['note'] = 'kept for frame-based players; the preview uses the continuous rise'
cm['frames']['sit_rear/sit_rear_legs'] = dict(file='02_character_frames/sit_rear/sit_rear_legs.png', source='procedural (scripts/rigs_v3.py)', facing='back')
json.dump(cm, open(f'{ROOT}/04_guides/character_manifest.json', 'w'), ensure_ascii=False, indent=1)
json.dump(slots, open(f'{V}/slots_export.json', 'w'))
print('exported')

# ---- v4: pixel-style parts
import glob
os.makedirs(f'{ROOT}/09_dog/frames', exist_ok=True); os.makedirs(f'{L}/ball', exist_ok=True)
for f in glob.glob('work/v4/dog/*.png'): shutil.copy(f, f'{ROOT}/09_dog/frames/' + os.path.basename(f))
for f in glob.glob('work/v4/ball/*.png'): shutil.copy(f, f'{L}/ball/' + os.path.basename(f))
if os.path.exists(f'{L}/ball.png'): os.remove(f'{L}/ball.png')
for n in ('sit_rear_legs',): shutil.copy(f'work/v4/{n}.png', f'{ROOT}/02_character_frames/sit_rear/{n}.png')
legs = Image.open('work/v4/sit_rear_legs.png'); W_ = 'work/char/sit_rear'
def stk(*ls):
    c = Image.new('RGBA', (320, 440), (0, 0, 0, 0))
    for l in ls: c.alpha_composite(l)
    return c
hd, ht, bd = (Image.open(f'{W_}/{n}.png') for n in ('sit_rear_head', 'sit_rear_head_turn_right', 'sit_rear_body'))
stk(legs, hd, bd).save(f'{ROOT}/02_character_frames/sit_rear/sit_rear_01.png'); stk(legs, ht, bd).save(f'{ROOT}/02_character_frames/sit_rear/sit_rear_02_look_right.png')
for n in ('rise_rear_01', 'rise_rear_02'): stk(legs, Image.open(f'{W_}/{n}_nolegs.png')).save(f'{ROOT}/02_character_frames/sit_rear/{n}.png')
m4 = json.load(open('work/v4/meta.json')); cm = json.load(open(f'{ROOT}/04_guides/character_manifest.json'))
cm['walk_cycle']['crossfade'] = 0.35
cm['sit_rear'].pop('arms', None); cm['sit_rear']['occupied_mesh'] = '01_scene_layers/06b_chair_back_mesh_occupied.png — show while someone is behind the chair'
json.dump(cm, open(f'{ROOT}/04_guides/character_manifest.json', 'w'), ensure_ascii=False, indent=1)
print('v4 exported')
