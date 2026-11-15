import numpy as np
from PIL import Image
from scipy import ndimage
D = '/Users/nikolaiarsenov/Downloads/handoff-web-project/animation/studio_animation_layers_v3'
back = np.asarray(Image.open(f'{D}/01_scene_layers/06_chair_back.png')).astype(float)
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
H, W = orig.shape[:2]; yy, xx = np.mgrid[:H, :W]
shell = (back[..., 3] > 200) & (yy < 612) & (xx > 404) & (xx < 556)
shell = ndimage.binary_fill_holes(shell)
interior = ndimage.binary_erosion(shell, iterations=9) & (yy > 494)
interior &= ~((xx >= 458) & (xx <= 500) & (yy >= 566))          # lumbar bracket stays as drawn
# mesh weave = fine detail of the painted mesh; base = dark hoodie seen through the mesh
hp = orig - ndimage.gaussian_filter(orig, (1.4, 1.4, 0))
base = np.array([30, 25, 29.0])
vy = np.clip((yy - 494) / 120.0, 0, 1)[..., None]                 # slightly lighter at the top (rim light from monitors)
col = base * (1.12 - 0.18 * vy) + np.clip(hp, -9, 9) * 0.8
a = ndimage.gaussian_filter(interior.astype(float), 0.7) * interior
out = np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8); out[~interior] = 0
Image.fromarray(out, 'RGBA').save(f'{D}/01_scene_layers/06b_chair_back_mesh_occupied.png', optimize=True)
ys, xs = np.nonzero(interior); print('mesh interior bbox', xs.min(), ys.min(), xs.max(), ys.max(), int(interior.sum()))
