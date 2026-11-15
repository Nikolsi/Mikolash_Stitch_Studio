import json, os, zipfile, io, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
ORIG = 'work/bg.png'
LM = json.load(open(f'{ROOT}/04_guides/layer_map.json')); CM = json.load(open(f'{ROOT}/04_guides/character_manifest.json'))
try: FONT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 18); FS = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Unicode.ttf', 13)
except Exception: FONT = FS = ImageFont.load_default()
G = f'{ROOT}/04_guides'
def L(n): return Image.open(f'{ROOT}/{n}').convert('RGBA')
def scene(chars, with_amb=False):
    c = L('01_scene_layers/00_background_clean_plate.png')
    for n in ('00b_neon_sign', '01_chair_shadow', '02_machine_needles_static', '02b_machine_needle_active', '03_machine_head'): c.alpha_composite(L(f'01_scene_layers/{n}.png'))
    for f, x, y, flip in chars:
        im = L(f'02_character_frames/{f}.png')
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        c.alpha_composite(im, (x - 160, y - 430))
    for n in ('05_chair_seat_base', '06_chair_back', '07_foreground_rug'): c.alpha_composite(L(f'01_scene_layers/{n}.png'))
    c.alpha_composite(L('09_dog/frames/awake_a.png'), (262, 761)); c.alpha_composite(L('01_scene_layers/ball/ball_0.png'), (322, 830)); c.alpha_composite(L('01_scene_layers/08_dog_bed_front_rim.png'))
    return c
# 1) layer map preview
c = Image.open(ORIG).convert('RGB'); d = ImageDraw.Draw(c, 'RGBA')
cols = {'01_chair_shadow': (255, 200, 0), '02b_machine_needle_active': (255, 230, 0), '00b_neon_sign': (255, 120, 220), '08_dog_bed_front_rim': (200, 160, 255), '03_machine_head': (255, 60, 60), '05_chair_seat_base': (0, 200, 255), '06_chair_back': (90, 120, 255), '07_foreground_rug': (80, 220, 120)}
for l in LM['layers_back_to_front']:
    if 'file' not in l: continue
    k = os.path.basename(l['file'])[:-4]
    if k not in cols: continue
    x0, y0, x1, y1 = l['bbox_xyxy']; col = cols[k]
    d.rectangle([x0, y0, x1, y1], outline=col + (255,), width=2)
    d.text((x0 + 2, y0 - 18 if y0 > 20 else y1 + 2), f"z{l['z']} {k} [{x0},{y0}–{x1},{y1}]", fill=col + (255,), font=FS, stroke_width=2, stroke_fill=(0, 0, 0))
for name, (x, y) in [('sit', LM['route_points']['sit']), ('turn', LM['route_points']['turn']), ('walk start', LM['route_points']['walk_start']), ('machine stop', LM['route_points']['machine_stop']), ('lean', LM['route_points']['lean_base'])]:
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 0, 200, 255)); d.text((x + 7, y + 2), name, fill=(255, 0, 200, 255), font=FS, stroke_width=2, stroke_fill=(0, 0, 0))
pts = [LM['route_points']['sit'], LM['route_points']['turn'], LM['route_points']['profile'], LM['route_points']['walk_start'], [820, 755], LM['route_points']['lean_base']]
d.line([tuple(p) for p in pts], fill=(255, 0, 200, 200), width=2)
for k, a in LM['ambient_overlays'].items():
    for b in (a.get('boxes_xyxy') or [a['box_xyxy']]):
        d.rectangle(b, outline=(255, 255, 255, 160), width=1)
    b0 = (a.get('boxes_xyxy') or [a['box_xyxy']])[0]; d.text((b0[0], b0[3] + 1), 'ambient: ' + k, fill=(255, 255, 255, 220), font=FS, stroke_width=2, stroke_fill=(0, 0, 0))
for k, v in LM['content_slots'].items():
    d.polygon([tuple(p) for p in v['quad']], outline=(255, 255, 0, 255)); d.text((v['quad'][0][0] + 2, v['quad'][0][1] + 2), 'slot: ' + k, fill=(255, 255, 0, 255), font=FS, stroke_width=2, stroke_fill=(0, 0, 0))
db = LM['dog']['box_xyxy']; d.rectangle(db, outline=(255, 200, 80, 255), width=2); d.text((db[0], db[1] - 16), 'dog (SVG) + ball', fill=(255, 200, 80, 255), font=FS, stroke_width=2, stroke_fill=(0, 0, 0))
d.rectangle([10, 900, 820, 935], fill=(0, 0, 0, 170)); d.text((18, 907), 'Карта слоёв (координаты в пикселях холста 1672×941). Розовый — маршрут персонажа (точки привязки = опора ног).', fill=(255, 255, 255), font=FS)
c.save(f'{G}/layer_map_preview.png', optimize=True)
# 2) composite preview sheet (key poses)
poses = [('1 сидит за ПК (спиной)', [('sit_rear/sit_rear_01', 476, 722, False)]), ('2 смотрит на правый монитор', [('sit_rear/sit_rear_02_look_right', 476, 722, False)]),
         ('3 встаёт', [('sit_rear/rise_rear_02', 476, 722, False)]), ('4 стоит за креслом', [('walk_away/walk_away_01', 476, 722, False)]),
         ('5 поворот', [('walk_away/walk_away_02', 525, 724, False)]), ('6 идёт к машине', [('walk_side/walk_06', 760, 750, False)]),
         ('7 подошёл (ноги на месте)', [('lean_rig/lean_rig_00_upright', 1192, 755, False)]), ('8 наклон + притоп', [('lean_rig/lean_rig_02_inspect_tap', 1192, 755, False)]),
         ('9 разворот', [('idle/idle_main', 1180, 755, False)]), ('10 идёт обратно', [('walk_side/walk_01', 900, 755, True)]),
         ('11 заходит за кресло', [('walk_away/walk_away_02', 525, 724, True)]), ('12 садится', [('sit_rear/rise_rear_01', 476, 722, False)])]
tw, th = 557, 314; S = Image.new('RGB', (tw * 4 + 12, th * 3 + 8), (255, 255, 255))
for i, (lab, spec) in enumerate(poses):
    im = scene(spec).convert('RGB').resize((tw, th), Image.LANCZOS); dd = ImageDraw.Draw(im)
    dd.rectangle([4, 4, 12 + 9 * len(lab), 26], fill=(0, 0, 0)); dd.text((8, 6), lab, fill=(255, 255, 255), font=FS)
    S.paste(im, ((i % 4) * (tw + 4), (i // 4) * (th + 4)))
S.save(f'{G}/composite_preview_sheet.png', optimize=True)
# 3) character frames sheet with anchors
keys = sorted(CM['frames'].keys()); cw, ch = 320, 440; cols_n = 7
F = Image.new('RGB', (cw * cols_n, (ch + 24) * ((len(keys) + cols_n - 1) // cols_n)), (40, 40, 44))
for i, k in enumerate(keys):
    t = Image.new('RGBA', (cw, ch), (205, 200, 190, 255)); t.alpha_composite(L(CM['frames'][k]['file']))
    dd = ImageDraw.Draw(t); dd.line([(0, 430), (cw, 430)], fill=(0, 90, 255)); dd.line([(160, 0), (160, ch)], fill=(255, 0, 120)); dd.rectangle([0, 0, cw - 1, ch - 1], outline=(120, 120, 120))
    x, y = (i % cols_n) * cw, (i // cols_n) * (ch + 24); F.paste(t.convert('RGB'), (x, y))
    ImageDraw.Draw(F).text((x + 4, y + ch + 4), k, fill=(255, 255, 255), font=FS)
F.save(f'{G}/character_frames_sheet.png', optimize=True)
# 4) layer order (exploded) preview
order = [('00 чистый фон + неон', ['00_background_clean_plate', '00b_neon_sign']), ('01 тень кресла', ['01_chair_shadow']), ('02–03 иглы (1 активная) + головка', ['02_machine_needles_static', '02b_machine_needle_active', '03_machine_head']),
         ('04 персонаж', None), ('05 сиденье/крестовина', ['05_chair_seat_base']), ('06 спинка/подлокотники', ['06_chair_back']), ('07–08 ковёр + бортик лежанки', ['07_foreground_rug', '08_dog_bed_front_rim'])]
ow, oh = 418, 235; O = Image.new('RGB', (ow * 4 + 12, oh * 2 + 30), (30, 30, 34))
for i, (lab, ns) in enumerate(order):
    t = Image.new('RGBA', (1672, 941), (255, 0, 255, 255) if i else (0, 0, 0, 255))
    if ns is None: t.alpha_composite(L('02_character_frames/sit_rear/sit_rear_01.png'), (476 - 160, 722 - 430)); t.alpha_composite(L('02_character_frames/lean_rig/lean_rig_02_inspect.png'), (1192 - 160, 755 - 430))
    else:
        for n in ns: t.alpha_composite(L(f'01_scene_layers/{n}.png'))
    t = t.convert('RGB').resize((ow, oh), Image.LANCZOS); x, y = (i % 4) * (ow + 4), (i // 4) * (oh + 15)
    O.paste(t, (x, y)); ImageDraw.Draw(O).text((x + 4, y + oh), lab, fill=(255, 255, 255), font=FS)
full = scene([('sit_rear/sit_rear_01', 476, 722, False)]).convert('RGB').resize((ow, oh), Image.LANCZOS); O.paste(full, (3 * (ow + 4), oh + 15)); ImageDraw.Draw(O).text((3 * (ow + 4) + 4, 2 * oh + 15), '= итоговый композит', fill=(255, 255, 255), font=FS)
O.save(f'{G}/layer_order_preview.png', optimize=True)
# 5) project files: ORA (Krita/GIMP/MyPaint) + PSD
P = f'{ROOT}/05_project'
stack = [  # bottom -> top: (name, image, x, y, visible)
    ('REF original banner (do not export)', Image.open(ORIG).convert('RGBA'), 0, 0, False),
    ('00 background clean plate', L('01_scene_layers/00_background_clean_plate.png'), 0, 0, True),
    ('00b neon sign (swappable)', L('01_scene_layers/00b_neon_sign.png'), 0, 0, True),
    ('01 chair shadow', L('01_scene_layers/01_chair_shadow.png'), 0, 0, True),
    ('02 machine needles static', L('01_scene_layers/02_machine_needles_static.png'), 0, 0, True),
    ('02b machine needle ACTIVE', L('01_scene_layers/02b_machine_needle_active.png'), 0, 0, True),
    ('03 machine head', L('01_scene_layers/03_machine_head.png'), 0, 0, True),
]
chars = [('04 CHAR sit_rear_01 @476,722', 'sit_rear/sit_rear_01', 476, 722, True), ('04 CHAR walk_01 @900,755', 'walk_side/walk_01', 900, 755, False), ('04 CHAR lean_rig_02_inspect @1192,755', 'lean_rig/lean_rig_02_inspect', 1192, 755, False)]
for n, f, x, y, v in chars:
    im = L(f'02_character_frames/{f}.png'); bb = im.getbbox(); stack.append((n, im.crop(bb), x - 160 + bb[0], y - 430 + bb[1], v))
stack += [('05 chair seat + base', L('01_scene_layers/05_chair_seat_base.png'), 0, 0, True), ('06 chair back + armrests', L('01_scene_layers/06_chair_back.png'), 0, 0, True),
          ('07 foreground rug', L('01_scene_layers/07_foreground_rug.png'), 0, 0, True),
          ('09 DOG (pixel sprite awake_a)', L('09_dog/frames/awake_a.png'), 262, 761, True), ('09b ball', L('01_scene_layers/ball/ball_0.png'), 322, 830, True),
          ('08 dog bed front rim', L('01_scene_layers/08_dog_bed_front_rim.png'), 0, 0, True)]
for k, v in LM['content_slots'].items():
    q = np.array(v['quad']); stack.append((f'SLOT {k} (default art)', L(v['file']).resize((int(q[:, 0].max() - q[:, 0].min()), int(q[:, 1].max() - q[:, 1].min()))), int(q[:, 0].min()), int(q[:, 1].min()), False))
for k, a in LM['ambient_overlays'].items():
    if 'file' in a: b = a['box_xyxy']; stack.append((f'AMB {k}', L(a['file']), b[0], b[1], False))
def trim(im, x, y):
    bb = im.getbbox()
    return (im.crop(bb), x + bb[0], y + bb[1]) if bb else (im, x, y)
merged = scene([('sit_rear/sit_rear_01', 476, 722, False)])
with zipfile.ZipFile(f'{P}/studio_scene_layers.ora', 'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'), 'image/openraster', compress_type=zipfile.ZIP_STORED)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<image version="0.0.3" w="1672" h="941" xres="72" yres="72">', '<stack>']
    for i, (n, im, x, y, v) in enumerate(reversed(stack)):
        if not n.startswith(('00', 'REF')): im, x, y = trim(im, x, y)
        buf = io.BytesIO(); im.save(buf, 'PNG'); fn = f'data/layer{i:02d}.png'; z.writestr(fn, buf.getvalue(), compress_type=zipfile.ZIP_DEFLATED)
        xml.append(f'<layer name="{n}" src="{fn}" x="{x}" y="{y}" opacity="1.0" visibility="{"visible" if v else "hidden"}" composite-op="{"svg:screen" if n.startswith("AMB") and "colon" not in n else "svg:src-over"}"/>')
    xml += ['</stack>', '</image>']; z.writestr('stack.xml', '\n'.join(xml), compress_type=zipfile.ZIP_DEFLATED)
    buf = io.BytesIO(); merged.save(buf, 'PNG'); z.writestr('mergedimage.png', buf.getvalue())
    th_ = merged.copy(); th_.thumbnail((256, 256)); buf = io.BytesIO(); th_.save(buf, 'PNG'); z.writestr('Thumbnails/thumbnail.png', buf.getvalue())
try:
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    psd = PSDImage.new(mode='RGBA', size=(1672, 941))
    for n, im, x, y, v in stack:
        if not n.startswith(('00', 'REF')): im, x, y = trim(im, x, y)
        lay = PixelLayer.frompil(im, psd, n, y, x); lay.visible = v; psd.append(lay)
    psd.save(f'{P}/studio_scene_layers.psd')
    chk = PSDImage.open(f'{P}/studio_scene_layers.psd'); print('PSD layers:', len(list(chk)))
except Exception as e:
    print('PSD export failed:', repr(e))
print('guides + project done')
