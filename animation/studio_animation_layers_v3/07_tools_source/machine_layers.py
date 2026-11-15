import numpy as np, subprocess, sys
from PIL import Image
from scipy import ndimage
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
lum = orig.mean(-1); r, b = orig[..., 0], orig[..., 2]
H, W = lum.shape
head = np.load('work/head_mask.npy')
for _ in range(2):
    ring = ndimage.binary_dilation(head) & ~head
    head |= ring & (lum < 70)
np.save('work/head_mask_grown.npy', head)
needle = np.zeros((H, W), bool); needle[504:520, 1346:1412] = True
inp = ndimage.binary_dilation(head | needle, iterations=3)
np.save('work/machine_inpaint_mask.npy', inp)
