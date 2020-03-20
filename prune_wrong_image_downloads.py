import os
import sys
from collections import defaultdict

image_url_file = os.path.abspath(sys.argv[1])
image_list_file = os.path.abspath(sys.argv[2])
image_folder = os.path.abspath(sys.argv[3])

print("reading image paths")
image_paths = defaultdict(set)
with open(image_list_file, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) != 2: continue
        file_num, path = spl
        image_paths[file_num].add(path)

print("reading output files")
removed = 0
with open(image_url_file, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) != 2: continue

        file_num, url = spl
        extension = url[url.rfind("."):]
        folder = str(int(file_num)%1000)

        for image_file in image_paths[file_num]:
            image_extension = image_file[image_file.rfind("."):]
            if extension != image_extension:
                removed += 1
                if removed % 100 == 0:
                    command = "rm " + os.path.join(image_folder, image_file)
                else:
                    command = "rm " + os.path.join(image_folder, image_file) + " &"
                print(command)
                os.system(command)

        if (c + 1) % 1000000 == 0:
            print(c + 1)

print("removed files", removed)