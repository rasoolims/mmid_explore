import os
import sys
from collections import defaultdict

image_url_file = os.path.abspath(sys.argv[1])
image_folder = os.path.abspath(sys.argv[2])

print("reading image paths")
image_paths = defaultdict(set)
for folder in os.listdir(image_folder):
    print(folder)
    folder_path = os.path.join(image_folder, folder)
    if not os.path.isdir(folder_path): continue

    for file in os.listdir(folder_path):
        file_num = file[:file.rfind(".")]
        file_path = os.path.join(folder_path, file)
        image_paths[file_num].add(file_path)

print("reading output files")
removed = 0

existing_ids = set()
with open(image_url_file, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) != 2: continue

        file_num, url = spl
        extension = url[url.rfind("."):]
        folder = str(int(file_num) % 1000)

        if not url.lower().endswith(".svg"):
            existing_ids.add(file_num)

        for image_file in image_paths[file_num]:
            image_extension = image_file[image_file.rfind("."):]
            if extension != image_extension:
                removed += 1
                if removed % 100 == 0:
                    command = "rm " + image_file
                else:
                    command = "rm " + image_file + " &"
                #print(command)
                #os.system(command)

        if (c + 1) % 1000000 == 0:
            print(c + 1)

print("removing illegal files!")
for folder in os.listdir(image_folder):
    print(folder)
    folder_path = os.path.join(image_folder, folder)
    if not os.path.isdir(folder_path): continue

    for file in os.listdir(folder_path):
        file_num = file[:file.rfind(".")]
        file_path = os.path.join(folder_path, file)
        if file_num not in existing_ids:
            removed += 1
            if removed % 100 == 0:
                command = "rm " + file_path
            else:
                command = "rm " + file_path + " &"
            print(command)
            #os.system(command)

print("removed files", removed)
