import os
import sys

input_folder = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

file_set = set()
with open(output_file, "w") as writer:
    for folder in os.listdir(input_folder):
        # print(folder)
        folder_path = os.path.join(input_folder, folder)
        for file in os.listdir(folder_path):
            fl = file.lower()
            if fl.endswith("jpg") or fl.endswith("png"):
                file_num = fl[:-4]
            elif fl.endswith("jpeg"):
                file_num = fl[:-5]
            else:
                continue
            if file_num not in file_set:
                file_set.add(file_num)
            else:
                print("repeated", file_num)
            writer.write(file_num + "\t" + folder + "/" + file + "\n")
print("done!")
