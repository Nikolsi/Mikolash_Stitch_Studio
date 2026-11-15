import glob, os, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
SRC = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_revised_pack_v2/studio_animation_revised_pack/01_character_frames_aligned'
OUT = 'work/char'
os.makedirs(OUT, exist_ok=True)
H_STAND = 390.0
S_A = H_STAND / 370.0          # idle / sit / stand_up group
S_B = S_A * 1.22               # walk / walk_away / lean group (drawn ~1.22x smaller in source sheet)
CW, CH, AX, AY = 320, 440, 160, 430
def defringe(a):
    a = a.astype(float); al = a[..., 3]
    for _ in range(2):
        solid = al > 0
        bnd = solid & ndimage.binary_dilation(~solid)
        rgb = a[..., :3]; mx = rgb.max(-1); mn = rgb.min(-1); lum = rgb.mean(-1)
        sat = (mx - mn) / np.maximum(mx, 1)
        bad = bnd & (lum > 95) & (sat < 0.22)
        al[bad] = 0
    # decontaminate remaining semi-transparent boundary: pull colour toward darkest opaque neighbour
    solid = al > 0; bnd = solid & ndimage.binary_dilation(~solid)
    rgb = a[..., :3]
    dark = np.stack([ndimage.grey_erosion(np.where(al[..., None] >= 250, rgb, 255)[..., c], size=3) for c in range(3)], -1)
    semi = bnd & (al < 250)
    rgb[semi] = np.minimum(rgb[semi], dark[semi])
    a[..., 3] = al
    return a.astype(np.uint8)
def scale(im, s):
    a = np.asarray(im).astype(float); al = a[..., 3:4] / 255.0
    pm = np.dstack([a[..., :3] * al, al * 255]).astype(np.float32)
    w, h = round(im.width * s), round(im.height * s)
    ch = [Image.fromarray(pm[..., i]).resize((w, h), Image.LANCZOS) for i in range(4)]
    r = np.stack([np.asarray(c) for c in ch], -1)
    A = np.clip(r[..., 3], 0, 255); rgb = r[..., :3] / np.maximum(A[..., None] / 255.0, 1e-4)
    out = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), A]).astype(np.uint8), 'RGBA')
    rgbim = out.convert('RGB').filter(ImageFilter.UnsharpMask(radius=0.8, percent=45, threshold=1))
    o = np.dstack([np.asarray(rgbim), np.asarray(out)[..., 3]])
    o[o[..., 3] < 8] = 0
    return Image.fromarray(o, 'RGBA')
def boots(a):
    al = a[..., 3].astype(int); rgb = a[..., :3].astype(int); r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    ys = np.nonzero(al > 128)[0]; y0, y1 = ys.min(), ys.max()
    return (al > 128) & (r > 120) & (r - b > 50) & (g > 70) & (r > g) & (np.arange(a.shape[0])[:, None] > y0 + 0.7 * (y1 - y0))
meta = {}
for f in sorted(glob.glob(os.path.join(SRC, '*', '*.png'))):
    group, name = f.split('/')[-2], os.path.basename(f)[:-4]
    s = S_B if group in ('walk_side', 'walk_away', 'lean_inspect') else S_A
    im = Image.fromarray(defringe(np.asarray(Image.open(f).convert('RGBA'))), 'RGBA')
    im = im.crop(im.getbbox()); im = scale(im, s)
    a = np.asarray(im); al = a[..., 3]
    bt = boots(a); sole = int(np.nonzero(al > 128)[0].max())
    # grounded boot pixels: boot px within 10px of sole
    yy = np.arange(a.shape[0])[:, None] * np.ones((1, a.shape[1]))
    gnd = bt & (yy > sole - 16)
    t0, t1 = int(0.25 * a.shape[0]), int(0.45 * a.shape[0])
    torso_x = float(np.nonzero(al[t0:t1] > 128)[1].mean())
    gx = np.nonzero(gnd)[1]
    base_x = float((gx.min() + gx.max()) / 2) if gnd.any() else torso_x
    ref_x = torso_x if group == 'walk_side' else base_x
    meta[f'{group}/{name}'] = dict(group=group, name=name, scale=round(s, 4), size=im.size, sole_y=sole, torso_x=torso_x, base_x=base_x, ref_x=ref_x)
    canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    ox, oy = int(round(AX - ref_x)), AY - sole
    canvas.alpha_composite(im, (ox, oy))
    os.makedirs(os.path.join(OUT, group), exist_ok=True)
    canvas.save(os.path.join(OUT, group, name + '.png'), optimize=True)
    meta[f'{group}/{name}'].update(offset=[ox, oy], clipped=bool(ox < 0 or oy < 0 or ox + im.width > CW))
json.dump(dict(canvas=[CW, CH], anchor=[AX, AY], S_A=S_A, S_B=S_B, frames=meta), open('work/char_meta.json', 'w'), indent=1)
for k, v in meta.items(): print(k, v['size'], 'sole', v['sole_y'], 'torso', round(v['torso_x']), 'base', round(v['base_x']), 'clip' if v['clipped'] else '')
