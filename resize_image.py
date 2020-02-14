from PIL import Image
import os,sys

# Opens a image in RGB mode
image_path = os.path.abspath(sys.argv[1])
im = Image.open(os.path.abspath(image_path))
new_width, new_height = int(sys.argv[2]), int(sys.argv[3])
output_path = os.path.abspath(sys.argv[4])

new_im = im.resize((new_width, new_height))
new_im.save(image_path)