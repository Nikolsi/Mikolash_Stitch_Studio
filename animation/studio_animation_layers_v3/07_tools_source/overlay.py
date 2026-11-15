import sys
import numpy as np
from PIL import Image
m = np.load(sys.argv[1]); x0, y0, x1, y1 = map(int, sys.argv[3:7]); s = int(sys.argv[7])
img = np.asarray(Image.open('work/bg.png').convert('RGB')).astype(float)
o = img.copy(); o[m] = o[m] * 0.45 + np.array([0, 255, 80]) * 0.55
# draw mask boundary in red
from scipy import ndimage
b = m & ~ndimage.binary_erosion(m)
o[b] = [255, 0, 0]
Image.fromarray(o.astype(np.uint8)[y0:y1, x0:x1]).resize(((x1 - x0) * s, (y1 - y0) * s), Image.NEAREST).save(sys.argv[2])
