import json, sys
from PIL import Image, ImageDraw
sys.path.insert(0, '.')
from comp_test import scene, L
poses = [
 ('1 sit', [('sit_rear/sit_rear_01', 476, 722, False)]),
 ('2 rise', [('sit_rear/rise_rear_02', 476, 722, False)]),
 ('3 stand', [('walk_away/walk_away_01', 476, 722, False)]),
 ('4 turn', [('walk_away/walk_away_02', 525, 724, False)]),
 ('5 walk', [('walk_side/walk_06', 700, 742, False)]),
 ('6 walk', [('walk_side/walk_01', 980, 755, False)]),
 ('7 lean', [('lean_inspect/lean_inspect_03', 1190, 755, False)]),
 ('8 turn', [('idle/idle_main', 1180, 755, False)]),
 ('9 back', [('walk_side/walk_05', 850, 755, True)]),
]
tiles = []
for label, spec in poses:
    im = scene([(L + 'char/' + p + '.png', x, y, f) for p, x, y, f in spec]).convert('RGB')
    d = ImageDraw.Draw(im); d.rectangle([8, 8, 150, 44], fill=(0, 0, 0)); d.text((16, 16), label, fill=(255, 255, 255))
    tiles.append(im.resize((557, 314), Image.LANCZOS))
S = Image.new('RGB', (557 * 3 + 8, 314 * 3 + 8), (255, 255, 255))
for i, t in enumerate(tiles): S.paste(t, ((i % 3) * 561, (i // 3) * 318))
S.save('work/keyposes.png')
