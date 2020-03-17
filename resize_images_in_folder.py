import os
import sys

from PIL import Image

dir_path = os.path.abspath(sys.argv[1])
new_width, new_height = int(sys.argv[2]), int(sys.argv[3])

orig_sizes, new_sizes = 0, 0
resized, all = 0, 0
for f in os.listdir(dir_path):
    all += 1
    file_path = os.path.join(dir_path, f)
    if f.lower().endswith(".svg"):
        continue
    try:
        im = Image.open(file_path)
        orig_sizes += os.path.getsize(file_path)/(1024*1024)
        x, y = im.size
        if x * y > new_width * new_height:
            new_im = im.resize((new_width, new_height))
            new_im.save(file_path)
            resized+=1
    except:
        print("problem resizing", f)
    new_sizes += os.path.getsize(file_path) / (1024 * 1024)

print("finished resizing", resized, all, orig_sizes, new_sizes)
