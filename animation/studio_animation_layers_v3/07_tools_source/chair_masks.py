import numpy as np
from PIL import Image
from scipy import ndimage
img = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(int)
lum = img.mean(-1)
m = np.load('work/chair_mask.npy')
# grow into dark outline pixels (up to 3 px), only near the chair
for _ in range(3):
    ring = ndimage.binary_dilation(m) & ~m
    m = m | (ring & (lum < 70))
m = ndimage.binary_closing(m, iterations=1)
np.save('work/chair_mask_grown.npy', m)
# inpaint mask: chair + 4px + floor shadow zone under the base
inp = ndimage.binary_dilation(m, iterations=4)
yy, xx = np.mgrid[:img.shape[0], :img.shape[1]]
shadow = (yy > 700) & (yy < 752) & (xx > 405) & (xx < 575) & (lum < 120)
shadow = ndimage.binary_dilation(shadow, iterations=2) & (yy > 700) & (yy < 754) & (xx > 400) & (xx < 580)
inp |= shadow
np.save('work/chair_inpaint_mask.npy', inp)
print(m.sum(), inp.sum())
