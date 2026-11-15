import json, os, shutil, glob
import numpy as np, cv2
from PIL import Image, ImageFilter
ROOT = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
RUG = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_revised_pack_v2/studio_animation_revised_pack/02_background_and_foreground/foreground_rug_full_canvas_RGBA.png'
for d in ('01_scene_layers', '02_character_frames', '03_ambient_overlays', '04_guides', '05_project', '06_web_preview'):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
L = os.path.join(ROOT, '01_scene_layers')
def bbox(p):
    a = np.asarray(Image.open(p).convert('RGBA'))[..., 3]; ys, xs = np.nonzero(a)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
Image.open('work/clean_full.png').convert('RGBA').save(f'{L}/00_background_clean_plate.png', optimize=True)
scene_layers = [
 ('00_background_clean_plate.png', 'work/clean_full.png', 'static', 'Мастерская без кресла, без тени кресла и без подвижных головки/игл машины. Закрытые участки восстановлены.'),
 ('01_chair_shadow.png', 'work/L_chair_shadow.png', 'static', 'Тень и отражения кресла на полу (полупрозрачный слой). Нужна, если кресло на месте.'),
 ('02_machine_needles.png', 'work/L_machine_needles.png', 'needles', 'Ряд игл и лапок. Цикл: смещение по Y 0→3→0 px во время шитья.'),
 ('03_machine_head.png', 'work/L_machine_head.png', 'head', 'Иглодержатель (головка). Микровибрация 0–1 px во время шитья.'),
 ('04_character_slot', None, 'character', 'Сюда вставляется персонаж (кадры из 02_character_frames).'),
 ('05_chair_seat_base.png', 'work/L_chair_seat_base.png', 'static', 'Сиденье, механизм, газлифт, крестовина и колёса.'),
 ('06_chair_back.png', 'work/L_chair_back.png', 'static', 'Спинка, поясничный кронштейн, подлокотники. Кресло стоит спинкой к зрителю, поэтому обе части кресла лежат ПОВЕРХ персонажа.'),
 ('07_foreground_rug.png', RUG, 'static', 'Передний слой ковра (из пакета v2, без изменений). На текущем маршруте не перекрывает ноги — оставлен на случай другого маршрута.'),
]
layers_json = []
for z, (name, src, motion, role) in enumerate(scene_layers):
    if src is None:
        layers_json.append(dict(z=z, name=name, type='slot', role=role)); continue
    dst = f'{L}/{name}'
    if not name.startswith('00'): shutil.copy(src, dst)
    layers_json.append(dict(z=z, file=f'01_scene_layers/{name}', canvas=[1672, 941], position=[0, 0], bbox_xyxy=bbox(dst), motion=motion, role=role))
# ---------- character frames
meta = json.load(open('work/char_meta.json')); sit = json.load(open('work/sit_rear_meta.json'))
C = os.path.join(ROOT, '02_character_frames')
frames = {}
for key, m in meta['frames'].items():
    os.makedirs(f'{C}/{m["group"]}', exist_ok=True)
    shutil.copy(f'work/char/{key}.png', f'{C}/{key}.png')
    frames[key] = dict(file=f'02_character_frames/{key}.png', source=f'studio_animation_revised_pack_v2/.../01_character_frames_aligned/{key}.png', scale_from_source=m['scale'],
                       anchor_rule='torso centre (treadmill walk)' if m['group'] == 'walk_side' else 'centre of grounded boots', facing='right' if m['group'] not in ('idle',) or m['name'] != 'idle_main' else 'front')
os.makedirs(f'{C}/sit_rear', exist_ok=True)
for f in glob.glob('work/char/sit_rear/*.png'):
    n = os.path.basename(f)[:-4]
    if n.endswith('_nolegs'): continue
    shutil.copy(f, f'{C}/sit_rear/{n}.png')
    frames[f'sit_rear/{n}'] = dict(file=f'02_character_frames/sit_rear/{n}.png', source='derived from walk_away_01 / walk_away_02 (back view)', anchor_rule='same anchor as standing behind the chair; body lowered by DROP',
                                   facing='back')
os.makedirs(f'{C}/lean_rig', exist_ok=True)
for f in sorted(glob.glob('work/char/lean_rig/*.png')):
    n = os.path.basename(f)[:-4]; shutil.copy(f, f'{C}/lean_rig/{n}.png')
    frames[f'lean_rig/{n}'] = dict(file=f'02_character_frames/lean_rig/{n}.png', source='derived from lean_inspect_03 (legs fixed, torso rotated around hip)', anchor_rule='centre of grounded boots (same as lean_inspect_03)', facing='right')
rig = json.load(open('work/rigs_v2_meta.json'))
char_manifest = dict(
    canvas=[320, 440], anchor_px=[160, 430], anchor_meaning='ground contact point (soles line). Place frame so that anchor == scene point (x, y).',
    scene_scale=dict(standing_height_px=390, group_A_scale=round(meta['S_A'], 4), group_B_scale=round(meta['S_B'], 4),
                     note='Source sheet drew walk/walk_away/lean ~1.22x smaller than idle/sit/stand_up; both groups now match the scene scale.'),
    mirror='Frames face right. For walking left use CSS transform: scaleX(-1) on the 320x440 box (anchor stays at x=160).',
    walk_cycle=dict(order=['walk_side/walk_01', 'walk_side/walk_06', 'walk_side/walk_05', 'walk_side/walk_04'], advance_px_per_frame=[26, 42, 40, 34], fps=8,
                    note='Order chosen by planted-foot analysis; advances keep the planted boot within ~±6 px. walk_02/walk_03 are spare frames (inconsistent foot phase).'),
    sit_rear=dict(DROP_px=sit['DROP'], head_pivot_canvas=sit['head_pivot_canvas'], parts=['sit_rear/sit_rear_head', 'sit_rear/sit_rear_head_turn_right', 'sit_rear/sit_rear_body'],
                  layer_order='head under body (hood covers the neck seam)', idle_motion='head rotate ±1.2° around pivot, ~0.9 s; occasional head_turn_right 2–4 s; body breathing scaleY 1.000–1.006 from bottom',
                  rise_sequence=['sit_rear/sit_rear_01', 'sit_rear/rise_rear_01', 'sit_rear/rise_rear_02', 'walk_away/walk_away_01']),
    lean_rig=dict(rig['lean_rig'], parts=['lean_rig/lean_rig_legs', 'lean_rig/lean_rig_front_boot', 'lean_rig/lean_rig_torso'], layer_order='legs, front boot, torso',
                  frames=['lean_rig/lean_rig_00_upright', 'lean_rig/lean_rig_01_half', 'lean_rig/lean_rig_02_inspect', 'lean_rig/lean_rig_02_inspect_tap'],
                  waiting='alternate lean_rig_02_inspect (0.30 s) / lean_rig_02_inspect_tap (0.16 s) = foot tapping while the machine stitches'),
    sit_legs=dict(rig['sit_legs'], file='02_character_frames/sit_rear/sit_rear_legs.png', note='static under the seat; sit_rear_01/02 and rise_rear_* already include it'),
    unused_in_this_composition=['lean_inspect/lean_inspect_01', 'lean_inspect/lean_inspect_02', 'lean_inspect/lean_inspect_03 (replaced by lean_rig, same legs throughout)', 'computer_and_stand/sit_at_computer_01', 'computer_and_stand/sit_at_computer_02', 'computer_and_stand/stand_up_01', 'computer_and_stand/stand_up_02'],
    unused_reason='Chair in the scene faces away from the viewer, profile seated poses do not fit it. Kept (rescaled) for other compositions.',
    frames=frames)
json.dump(char_manifest, open(f'{ROOT}/04_guides/character_manifest.json', 'w'), ensure_ascii=False, indent=1)
# ---------- ambient overlays
A = os.path.join(ROOT, '03_ambient_overlays'); bg = Image.open('work/bg.png').convert('RGBA')
def glow(box, name, blur, gain):
    x0, y0, x1, y1 = box; pad = blur * 3
    crop = bg.crop((x0 - pad, y0 - pad, x1 + pad, y1 + pad)); a = np.asarray(crop).astype(float)
    lum = a[..., :3].max(-1); mask = np.clip((lum - 150) / 80, 0, 1)
    g = np.dstack([a[..., :3], mask * 255]).astype(np.uint8)
    gi = Image.fromarray(g, 'RGBA').filter(ImageFilter.GaussianBlur(blur))
    arr = np.asarray(gi).astype(float); arr[..., 3] = np.clip(arr[..., 3] * gain, 0, 255)
    Image.fromarray(arr.astype(np.uint8), 'RGBA').save(f'{A}/{name}.png', optimize=True)
    return [x0 - pad, y0 - pad, x1 + pad, y1 + pad]
amb = {}
amb['neon_glow'] = dict(file='03_ambient_overlays/neon_glow.png', box_xyxy=glow((401, 139, 631, 294), 'neon_glow', 6, 1.6), blend='screen', motion='breathing opacity 0.35–0.7, rare flicker')
amb['pc_rgb_glow'] = dict(file='03_ambient_overlays/pc_rgb_glow.png', box_xyxy=glow((262, 590, 354, 700), 'pc_rgb_glow', 4, 2.0), blend='screen', motion='pulse 4 s')
# clock colon "off" patch
cx0, cy0, cx1, cy1 = 1576, 142, 1592, 172
patch = np.asarray(bg.convert('RGB'))[cy0:cy1, cx0:cx1].copy()
blue = (patch[..., 2].astype(int) > 120) & (patch[..., 0].astype(int) < 140)
blue = cv2.dilate(blue.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
patch = cv2.inpaint(patch, blue.astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA)
Image.fromarray(patch).save(f'{A}/clock_colon_off.png')
amb['clock_colon_off'] = dict(file='03_ambient_overlays/clock_colon_off.png', box_xyxy=[cx0, cy0, cx1, cy1], blend='normal', motion='show 0.5 s every 1 s (colon blink)')
amb['monitor_glow'] = dict(type='css', boxes_xyxy=[[322, 372, 486, 491], [487, 376, 701, 493]], blend='screen', motion='soft flicker while typing')
json.dump(dict(layers_back_to_front=layers_json, ambient_overlays=amb), open(f'{ROOT}/04_guides/layer_map_partial.json', 'w'), ensure_ascii=False, indent=1)
print('ok', len(frames), 'frames')
