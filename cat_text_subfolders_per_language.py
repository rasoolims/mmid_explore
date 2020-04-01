import os
import sys

input_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for lang_folder in os.listdir(input_folder):
    lang_folder_path = os.path.join(input_folder, lang_folder)
    if not os.path.isdir(lang_folder_path):
        continue

    txt_files = []
    for subfolder in os.listdir(lang_folder_path):
        subfolder_path = os.path.join(lang_folder_path, subfolder)

        if not os.path.isdir(subfolder_path):
            continue

        file_path = subfolder_path + "/" + lang_folder + "." + subfolder + ".cat.txt"
        if os.path.exists(file_path):
            txt_files.append(file_path)

    command = " ".join(["cat"] + txt_files + ["> ", os.path.join(output_folder, lang_folder + ".txt")])
    print(command)
    os.system(command)
