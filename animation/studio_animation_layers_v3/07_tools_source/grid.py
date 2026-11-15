import sys
from PIL import Image, ImageDraw
src, out, x0, y0, x1, y1, s, step = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7]), int(sys.argv[7]), int(sys.argv[8])
im = Image.open(src).convert('RGB').crop((x0, y0, x1, y1)).resize(((x1 - x0) * s, (y1 - y0) * s), Image.NEAREST)
d = ImageDraw.Draw(im)
for x in range((x0 // step + 1) * step, x1, step):
    d.line([((x - x0) * s, 0), ((x - x0) * s, im.height)], fill=(0, 255, 255)); d.text(((x - x0) * s + 2, 2), str(x), fill=(255, 255, 0))
for y in range((y0 // step + 1) * step, y1, step):
    d.line([(0, (y - y0) * s), (im.width, (y - y0) * s)], fill=(0, 255, 255)); d.text((2, (y - y0) * s + 2), str(y), fill=(255, 255, 0))
im.save(out)
