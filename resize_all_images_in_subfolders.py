import os
import sys

from PIL import Image

# Opens a image in RGB mode
input_folder = os.path.abspath(sys.argv[1])
new_width, new_height = int(sys.argv[2]), int(sys.argv[3])

for dir in os.listdir(input_folder):
    dir_path = os.path.join(input_folder, dir)
    print("resizing", dir_path)
    if not os.path.isdir(dir_path):
        continue

    for f in os.listdir(dir_path):
        try:
            if f.endswith(".jpg"):
                file_path = os.path.join(dir_path, f)
                im = Image.open(os.path.abspath(file_path))
                x, y = im.size
                if x * y > new_width * new_height:
                    new_im = im.resize((new_width, new_height))
                    new_im.save(file_path)
        except:
            print("problem resizing", file_path)

print("finished")
