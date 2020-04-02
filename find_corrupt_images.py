import os
import sys

from PIL import Image
from PIL import ImageFile
from torchvision import transforms

ImageFile.LOAD_TRUNCATED_IMAGES = True

transform = transforms.Compose([  # [1]
    transforms.Resize(256),  # [2]
    transforms.CenterCrop(224),  # [3]
    transforms.ToTensor(),  # [4]
    transforms.Normalize(  # [5]
        mean=[0.485, 0.456, 0.406],  # [6]
        std=[0.229, 0.224, 0.225]  # [7]
    )])

# Also resize them if possible
Image.MAX_IMAGE_PIXELS = None

input_folder = os.path.abspath(sys.argv[1])
for file in os.listdir(input_folder):
    if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg") or file.lower().endswith(".png"):
        path = os.path.join(input_folder, file)
        try:
            image = Image.open(path).convert("RGB")
            x, y = image.size
            if x * y > 1024 * 1024:
                new_im = image.resize((1024, 1024))
                new_im.save(path)
            image = transform(image)
        except:
            print(path)
