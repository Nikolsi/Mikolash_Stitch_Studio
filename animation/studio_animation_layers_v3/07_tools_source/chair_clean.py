import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
orig = np.asarray(Image.open('work/bg.png').convert('RGB')).copy()
H, W = orig.shape[:2]
chair = np.load('work/chair_mask_grown.npy')
base = orig.copy()
# 1) keyboard extension: tile a 40px chunk of keys leftwards, add mirrored end-cap
ky0, ky1 = 523, 543
chunk = orig[ky0:ky1, 556:596]
cap = orig[ky0:ky1, 597:614][:, ::-1]
x = 556
while x - 40 >= 476:
    base[ky0:ky1, x - 40:x] = chunk; x -= 40
base[ky0:ky1, 476:x] = chunk[:, 40 - (x - 476):] if x > 476 else base[ky0:ky1, 476:x]
base[ky0:ky1, 476 - cap.shape[1]:476] = cap
kb = np.zeros((H, W), bool); kb[ky0:ky1, 476 - cap.shape[1]:556] = True
# 2) inpaint mask: chair (+4px) minus pinned keyboard, plus floor shadow/reflection zone
m = ndimage.binary_dilation(chair, iterations=4)
im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
d.polygon([(392, 733), (420, 726), (560, 726), (598, 733), (602, 752), (590, 768), (400, 768), (386, 752)], fill=255)
shadow_zone = np.asarray(im) > 0
m = (m | shadow_zone) & ~kb
np.save('work/chair_inpaint_mask2.npy', m); np.save('work/shadow_zone.npy', shadow_zone)
Image.fromarray(base).save('work/bg_kb.png')
print(m.sum())
