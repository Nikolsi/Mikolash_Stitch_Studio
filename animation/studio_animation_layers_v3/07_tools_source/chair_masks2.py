import numpy as np
from PIL import Image
from scipy import ndimage
img = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(int)
lum = img.mean(-1); r, g, b = img[..., 0], img[..., 1], img[..., 2]
m0 = np.load('work/chair_mask.npy'); H, W = m0.shape
yy = np.mgrid[:H, :W][0]
m = m0.copy()
strict = (lum < 45) & (b - r < 8)
for it in range(3):
    ring = ndimage.binary_dilation(m) & ~m
    ok = ring & strict & ((yy >= 484) | (it == 0))
    m |= ok
m = ndimage.binary_closing(m, iterations=1) | m0
# drop thin protrusions on top edge: opening on the top band only
top = yy < 484
mo = ndimage.binary_opening(m, structure=np.ones((3, 3)))
m = np.where(top, mo | m0, m)
np.save('work/chair_mask_grown.npy', m); print(int(m0.sum()), int(m.sum()))
