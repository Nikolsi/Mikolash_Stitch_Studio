from PIL import Image
W = 'work/char/sit_rear'; O = 'work/v3'
legs = Image.open(f'{O}/sit_rear_legs.png')
def stack(*ls):
    c = Image.new('RGBA', (320, 440), (0, 0, 0, 0))
    for l in ls: c.alpha_composite(l)
    return c
hd, ht, bd = (Image.open(f'{W}/{n}.png') for n in ('sit_rear_head', 'sit_rear_head_turn_right', 'sit_rear_body'))
for n in ('sit_rear_head', 'sit_rear_head_turn_right', 'sit_rear_body'): Image.open(f'{W}/{n}.png').save(f'{O}/{n}.png')
stack(legs, hd, bd).save(f'{O}/sit_rear_01.png'); stack(legs, ht, bd).save(f'{O}/sit_rear_02_look_right.png')
for n in ('rise_rear_01', 'rise_rear_02'): stack(legs, Image.open(f'{W}/{n}_nolegs.png')).save(f'{O}/{n}.png')
print('composed')
