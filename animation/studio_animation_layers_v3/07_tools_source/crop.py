import sys
from PIL import Image
src, out, x0, y0, x1, y1, s = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7]), float(sys.argv[7])
im = Image.open(src).convert('RGBA').crop((x0, y0, x1, y1))
bg = Image.new('RGBA', im.size, (255, 0, 255, 255)); bg.alpha_composite(im)
bg = bg.resize((int(im.width*s), int(im.height*s)), Image.NEAREST)
bg.convert('RGB').save(out)
