import os
import sys
import glob

image_url_file = os.path.abspath(sys.argv[1])
image_folder = os.path.abspath(sys.argv[2])
output_file = os.path.abspath(sys.argv[3])

with open(output_file, "w") as writer:
    with open(image_url_file, "r") as reader:
        for c, line in enumerate(reader):
            spl = line.strip().split("\t")

            if len(spl) != 2: continue

            file_num, url = spl

            extension = url[url.rfind("."):]
            file_name = file_num + extension
            folder = str(int(file_name)%1000)

            image_files = glob.glob(os.path.join(image_folder, folder, file_name+"*"))

            for image_file in image_files:
                image_extension = image_file[image_file.rfind("."):]
                if extension != image_extension:
                    writer.write(os.path.join(image_folder, folder, image_file))

            if (c + 1) % 100000 == 0:
                print(c + 1)