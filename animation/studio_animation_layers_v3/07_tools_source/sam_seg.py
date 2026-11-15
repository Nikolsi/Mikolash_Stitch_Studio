import sys, json
import numpy as np, torch
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor
cfg = json.loads(sys.argv[1]); out = sys.argv[2]
img = np.asarray(Image.open('work/bg.png').convert('RGB'))
sam = sam_model_registry['vit_b'](checkpoint='models/sam_vit_b_01ec64.pth'); sam.to('cpu')
pred = SamPredictor(sam); pred.set_image(img)
pts = np.array(cfg['pos'] + cfg['neg'], float); lbl = np.array([1] * len(cfg['pos']) + [0] * len(cfg['neg']))
masks, scores, logits = pred.predict(point_coords=pts, point_labels=lbl, box=np.array(cfg['box'], float), multimask_output=True)
for i, (m, s) in enumerate(zip(masks, scores)):
    print(i, float(s), int(m.sum()))
best = int(np.argmax(scores)) if 'pick' not in cfg else cfg['pick']
# refine once with the low-res logits
m2, s2, _ = pred.predict(point_coords=pts, point_labels=lbl, box=np.array(cfg['box'], float), mask_input=logits[best][None], multimask_output=False)
np.save(out, m2[0]); print('refined', float(s2[0]), int(m2[0].sum()))
