import numpy as np
from PIL import Image
from scipy import ndimage
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
clean = np.asarray(Image.open('work/clean_full_v1.png').convert('RGB')).astype(float).copy()
H, W = orig.shape[:2]
head = np.load('work/head_mask_grown.npy')
needle_rect = np.zeros((H, W), bool); needle_rect[504:520, 1346:1412] = True
# restore original outside the machine work zone
chair_keep = np.asarray(Image.open('work/clean_chair_final.png').convert('RGB')).astype(float)
zone = ndimage.binary_dilation(head | needle_rect, iterations=1)
clean[~zone] = chair_keep[~zone]
Image.fromarray(clean.astype(np.uint8)).save('work/clean_full.png')
# head layer
ring = ndimage.binary_dilation(head) & ~head
diff = np.abs(orig - clean).sum(-1)
alpha = head.astype(float); alpha[ring] = np.clip(diff[ring] / 120.0, 0, 0.6)
a3 = np.maximum(alpha, 1e-3)[..., None]
col = np.clip((orig - (1 - a3) * clean) / a3, 0, 255)
rgba = np.dstack([col, alpha * 255]).astype(np.uint8); rgba[alpha == 0] = 0
Image.fromarray(rgba, 'RGBA').save('work/L_machine_head.png', optimize=True)
# needle layer: difference matte inside needle rect (excluding head)
nz = needle_rect & ~head
na = np.clip((diff - 18) / 70.0, 0, 1) * nz
na = np.maximum(na, ndimage.grey_dilation(na, size=(1, 1)))
a3n = np.maximum(na, 1e-3)[..., None]
ncol = np.clip((orig - (1 - a3n) * clean) / a3n, 0, 255)
nrgba = np.dstack([ncol, na * 255]).astype(np.uint8); nrgba[na == 0] = 0
Image.fromarray(nrgba, 'RGBA').save('work/L_machine_needles.png', optimize=True)
def comp(dy_needle=0, dy_head=0):
    c = Image.fromarray(clean.astype(np.uint8)).convert('RGBA')
    n = Image.fromarray(nrgba, 'RGBA'); h = Image.fromarray(rgba, 'RGBA')
    c.alpha_composite(n, (0, dy_needle)); c.alpha_composite(h, (0, dy_head))
    return c
c0 = np.asarray(comp().convert('RGB')).astype(float)
e = np.abs(c0 - orig).mean(-1); print('machine recomposite err mean', e.mean().round(3), 'max', e.max().round(1), 'px>10', int((e > 10).sum()))
tiles = [comp(0, 0), comp(2, 0), comp(3, 1), comp(1, 0)]
S = Image.new('RGB', (4 * 130 * 4, 110 * 4))
for i, t in enumerate(tiles):
    S.paste(t.crop((1310, 410, 1440, 520)).resize((520, 440), Image.NEAREST).convert('RGB'), (i * 520, 0))
S.save('work/needle_frames.png')
