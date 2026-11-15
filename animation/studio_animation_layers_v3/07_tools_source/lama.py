import sys, json
import numpy as np, torch
from PIL import Image
# usage: lama.py image.png mask.npy|mask.png out.png x0 y0 x1 y1   (crop box, must be multiple of 8 in size)
img = np.asarray(Image.open(sys.argv[1]).convert('RGB'))
mp = sys.argv[2]
mask = np.load(mp) if mp.endswith('.npy') else (np.asarray(Image.open(mp).convert('L')) > 127)
x0, y0, x1, y1 = map(int, sys.argv[4:8])
model = torch.jit.load('models/big-lama.pt', map_location='cpu'); model.eval()
ci = img[y0:y1, x0:x1].astype(np.float32) / 255.; cm = mask[y0:y1, x0:x1].astype(np.float32)
it = torch.from_numpy(ci).permute(2, 0, 1)[None]; mt = torch.from_numpy(cm)[None, None]
with torch.no_grad():
    res = model(it, (mt > 0).float())[0].permute(1, 2, 0).numpy()
res = np.clip(res * 255, 0, 255).astype(np.uint8)
out = img.copy(); reg = out[y0:y1, x0:x1]; reg[cm > 0] = res[cm > 0]
Image.fromarray(out).save(sys.argv[3])
