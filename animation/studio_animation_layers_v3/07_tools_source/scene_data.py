import json
import numpy as np
from PIL import Image
ROOT = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
cm = json.load(open(f'{ROOT}/04_guides/character_manifest.json'))
slots = json.load(open('work/v3/slots_export.json'))
old = json.load(open(f'{ROOT}/04_guides/layer_map.json'))
amb = {k: v for k, v in old['ambient_overlays'].items() if k != 'neon_glow'}
def bbox(n):
    a = np.asarray(Image.open(f'{ROOT}/01_scene_layers/{n}').convert('RGBA'))[..., 3]; ys, xs = np.nonzero(a)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
LAYERS = [
 ('00_background_clean_plate.png', 'static', 'Мастерская без кресла, тени кресла, головки/игл, неона и мячика. Закрытые участки восстановлены.'),
 ('00b_neon_sign.png', 'flicker', 'Неоновая вывеска (сменяемый «баннер»): трубки + свечение на стене, полупрозрачная. Можно заменить любым RGBA того же холста.'),
 ('content_slots', 'slot', 'Постеры и экраны мониторов: картинки из /content проецируются на четырёхугольники (см. content_slots).'),
 ('01_chair_shadow.png', 'static', 'Тень/отражения кресла на полу.'),
 ('02_machine_needles_static.png', 'static', 'Неподвижные иглы и лапки (11 из 12).'),
 ('02b_machine_needle_active.png', 'needle', 'Одна активная игла: ход 0→4 px вниз, синусоида ~9 Гц во время шитья.'),
 ('03_machine_head.png', 'head', 'Головка: подрагивание ≤0.5 px синхронно с иглой.'),
 ('character', 'character', 'Персонаж (02_character_frames).'),
 ('05_chair_seat_base.png', 'static', 'Сиденье, механизм, крестовина. Кресло спинкой к зрителю — поверх персонажа.'),
 ('06_chair_back.png', 'static', 'Спинка и подлокотники — поверх персонажа.'),
 ('06b_chair_back_mesh_occupied.png', 'occupied', 'Сетка спинки «занята»: сквозь плетение видна толстовка, а не стол. Показывается, пока персонаж сидит/стоит за креслом.'),
 ('07_foreground_rug.png', 'static', 'Ковёр (перекрытие, на маршруте не задействован).'),
 ('dog', 'dog', 'Собака: пиксельные спрайт-кадры 68×104 (09_dog/frames, sw_* — в кофточке), исходник SVG 09_dog/yorkie.svg.'),
 ('ball', 'ball', 'Теннисный мячик: 8 кадров вращения 32×32 (01_scene_layers/ball/), катится от носа собаки.'),
 ('08_dog_bed_front_rim.png', 'static', 'Передний бортик лежанки — поверх собаки и мячика.'),
]
layers = []
for z, (n, motion, role) in enumerate(LAYERS):
    if n.endswith('.png'): layers.append(dict(z=z, file=f'01_scene_layers/{n}', canvas=[1672, 941], position=[0, 0], bbox_xyxy=bbox(n), motion=motion, role=role))
    else: layers.append(dict(z=z, name=n, type=motion, role=role))
P = dict(sit=[476, 722], turn=[525, 724], profile=[560, 726], walk_start=[590, 728], lane_y=755, machine_stop=[1170, 755], lean_base=[1192, 755])
H = lambda frame, x, y, dur, flip=False, label=None: dict(type='hold', frame=frame, at=[x, y], dur=dur, flip=flip, label=label)
route = [
 dict(type='sit', at=P['sit'], dur=[10, 15], label='работает за компьютером'),
 dict(type='rise', at=P['sit'], dur=0.5, label='встаёт'), H('walk_away/walk_away_01', *P['sit'], 0.3),
 H('walk_away/walk_away_02', *P['turn'], 0.22, label='поворачивается'), H('idle/idle_profile', *P['profile'], 0.24),
 dict(type='walk', **{'from': P['walk_start']}, to=P['machine_stop'], dir=1, y_ease_until_x=820, label='идёт к машине'),
 dict(type='lean', at=P['lean_base'], angle_from=18, in_s=0.55, hold_s=5.0, out_s=0.45, taps=[[0.5, 2.1], [2.9, 4.6]], tap_period=0.42, tap_deg=7, label='смотрит на вышивку, притопывает'),
 H('idle/idle_main', 1180, 755, 0.36, label='разворачивается'), H('idle/idle_profile', 1176, 755, 0.22, flip=True),
 dict(type='walk', **{'from': [1150, 755]}, to=P['walk_start'], dir=-1, y_ease_until_x=820, label='возвращается'),
 H('idle/idle_profile', 565, 726, 0.2, flip=True), H('walk_away/walk_away_02', *P['turn'], 0.24, flip=True), H('walk_away/walk_away_01', *P['sit'], 0.3),
 dict(type='sitdown', at=P['sit'], dur=0.55, label='садится'),
]
content_slots = {k: dict(quad=v['quad'], size=v['size'], aspect=v['aspect'], file=v['file'], kind=v['kind'], fit='cover', filter='') for k, v in slots.items()}
dog = dict(box_xyxy=[262, 761, 330, 865], frames_dir='09_dog/frames', source_svg='09_dog/yorkie.svg (+ 06_web_preview/dog.js)', sweater=False,
           poses={'sleep': dict(frames=['sleep_a', 'sleep_b'], period=1.7), 'awake': dict(frames=['awake_a', 'awake_b'], period=0.8), 'twitch': dict(frames=['twitch']),
                  'tilt-l': dict(frames=['tilt_l']), 'tilt-r': dict(frames=['tilt_r']), 'ball': dict(frames=['ball_a', 'ball_b'], period=0.17), 'nudge': dict(frames=['nudge']),
                  'happy': dict(frames=['happy_a', 'happy_b'], period=0.17), 'guy': dict(frames=['guy_a', 'guy_b'], period=0.17)},
           ball=dict(center=[338, 846], radius=15, roll_px=18, frames='01_scene_layers/ball/ball_0..7.png (45° steps)'), sleep_s=[7, 12],
           behaviour='sits in the bed: dozes (eyes closed, head droops) → wakes, twitches ears, tilts head left/right → looks at the ball → nudges it (rolls ~18 px), happy hop + tongue + tail wag → pulls it back → dozes. Blinks; looks at the guy when he stands up. Optional sweater (dog.sweater).')
machine = dict(needle=dict(file='01_scene_layers/02b_machine_needle_active.png', stroke_px=4, hz=9), head=dict(file='01_scene_layers/03_machine_head.png', jitter_px=0.5), run_s=6.5, pause_s=1.2)
data = dict(scene=[1672, 941], layers_back_to_front=layers, content_slots=content_slots, ambient_overlays=amb,
            character=dict(canvas=cm['canvas'], anchor_px=cm['anchor_px'], walk_cycle=cm['walk_cycle'], sit_rear=cm['sit_rear'], lean_rig=cm['lean_rig'],
                           z_rule='character is above machine layers and below both chair layers'),
            dog=dog, route_points=P, route=route, machine=machine)
json.dump(data, open(f'{ROOT}/04_guides/layer_map.json', 'w'), ensure_ascii=False, indent=1)
open(f'{ROOT}/06_web_preview/scene_data.js', 'w').write('// generated from 04_guides/layer_map.json — edit content_slots there or here (keep both in sync)\nwindow.MSS = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')
print('ok', len(route), 'steps')
