import sys, json
from PIL import Image, ImageDraw
L = 'work/'
def scene(chars):
    c = Image.open(L + 'clean_full.png').convert('RGBA')
    for n in ('L_chair_shadow',): c.alpha_composite(Image.open(L + n + '.png'))
    for path, ax, ay, flip in chars:
        im = Image.open(path)
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        c.alpha_composite(im, (int(ax - 160), int(ay - 430)))
    for n in ('L_chair_seat_base', 'L_chair_back', 'L_machine_needles', 'L_machine_head'): c.alpha_composite(Image.open(L + n + '.png'))
    rug = Image.open('/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_revised_pack_v2/studio_animation_revised_pack/02_background_and_foreground/foreground_rug_full_canvas_RGBA.png').convert('RGBA')
    c.alpha_composite(rug); return c
if __name__ == '__main__':
    spec = json.loads(sys.argv[1]); out = sys.argv[2]; box = list(map(int, sys.argv[3:7])) if len(sys.argv) > 6 else None
    im = scene([(L + 'char/' + p + '.png', x, y, f) for p, x, y, f in spec])
    (im.crop(box) if box else im).convert('RGB').save(out)
