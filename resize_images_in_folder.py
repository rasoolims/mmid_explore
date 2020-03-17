import os
import sys

from PIL import Image

# Opens a image in RGB mode
dir_path = os.path.abspath(sys.argv[1])
new_width, new_height = int(sys.argv[2]), int(sys.argv[3])

resized, all = 0, 0
for f in os.listdir(dir_path):
    all += 1
    try:
        file_path = os.path.join(dir_path, f)
        im = Image.open(os.path.abspath(file_path))
        x, y = im.size
        if x * y > new_width * new_height:
            new_im = im.resize((new_width, new_height))
            new_im.save(file_path)
            resized+=1
    except:
        print("problem resizing", f)

print("finished resizing", resized, all)
