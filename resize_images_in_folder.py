import os
import sys

from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

def svg2png(file_path):
    drawing = svg2rlg(file_path)
    new_file_path = file_path[:-3] + "png"
    renderPM.drawToFile(drawing, new_file_path, fmt="PNG")
    os.system("rm "+ file_path)
    return new_file_path

dir_path = os.path.abspath(sys.argv[1])
new_width, new_height = int(sys.argv[2]), int(sys.argv[3])

orig_sizes, new_sizes = 0, 0
resized, all = 0, 0
for f in os.listdir(dir_path):
    all += 1
    file_path = os.path.join(dir_path, f)

    if f.lower().endswith(".svg"):
        file_path = svg2png(file_path)
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
