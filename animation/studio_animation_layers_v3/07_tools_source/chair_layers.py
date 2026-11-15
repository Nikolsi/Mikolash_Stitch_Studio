import numpy as np
from PIL import Image
from scipy import ndimage
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
clean = np.asarray(Image.open('work/clean_chair_final.png').convert('RGB')).astype(float)
m = np.load('work/chair_mask_grown.npy'); H, W = m.shape
# alpha: 1 inside, soft outer 1px ring
ring = ndimage.binary_dilation(m) & ~m
alpha = m.astype(float); 
diff = np.abs(orig - clean).sum(-1)
alpha[ring] = np.clip(diff[ring] / 120.0, 0, 0.6)
col = orig.copy()
a3 = np.maximum(alpha, 1e-3)[..., None]
col = np.clip((orig - (1 - a3) * clean) / a3, 0, 255)
def save(mask_sel, path):
    a = alpha * mask_sel
    rgba = np.dstack([col, a * 255]).astype(np.uint8); rgba[a == 0] = 0
    Image.fromarray(rgba, 'RGBA').save(path, optimize=True)
yy, xx = np.mgrid[:H, :W]
spine = (xx >= 460) & (xx <= 498) & (yy < 670)
posts = ((xx < 426) | (xx > 556)) & (yy < 656)
back_sel = ((yy < 620) | spine | posts).astype(float)
full = (m | ring).astype(float)
save(full * back_sel, 'work/L_chair_back.png')
save(full * (1 - back_sel), 'work/L_chair_seat_base.png')
save(full, 'work/L_chair_full.png')
# shadow layer: solve alpha for dark color D over floor zone, outside chair
D = np.array([28., 14., 10.])
zone = ndimage.binary_dilation(np.load('work/shadow_zone.npy'), iterations=3) & ~(m | ring)
num = ((clean - orig) * (clean - D)).sum(-1); den = ((clean - D) ** 2).sum(-1) + 1e-6
sa = np.clip(num / den, 0, 0.85) * zone
sa = ndimage.gaussian_filter(sa, 0.6) * zone
sa[sa < 0.03] = 0
sa = np.where(sa > 0, np.maximum(sa, 0.12), 0)
sa8 = np.round(sa * 255) / 255.0
C = np.clip((orig - clean * (1 - sa8[..., None])) / np.maximum(sa8, 1e-3)[..., None], 0, 255)
sh = np.zeros((H, W, 4), np.uint8); sh[..., :3] = np.round(C).astype(np.uint8); sh[..., 3] = np.round(sa8 * 255).astype(np.uint8); sh[sa == 0] = 0
sa = sa8; D = C
Image.fromarray(sh, 'RGBA').save('work/L_chair_shadow.png', optimize=True)
# verify recomposite
comp = clean * (1 - sa[..., None]) + D * sa[..., None]
fa = alpha * full; comp = comp * (1 - fa[..., None]) + col * fa[..., None]
err = np.abs(comp - orig).mean(-1)
print('recomposite mean err', err.mean().round(3), 'p99', np.percentile(err, 99).round(2), 'max', err.max().round(1))
Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8)).save('work/chair_recomposite.png')
