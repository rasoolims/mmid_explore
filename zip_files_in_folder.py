import os
import sys

input_folder = os.path.abspath(sys.argv[1])
for folder in os.listdir(input_folder):
    print(folder)
    folder_path = os.path.join(input_folder, folder)
    for c, f in enumerate(os.listdir(folder_path)):
        if f.endswith("gz"):
            continue
        command = "gzip " + os.path.join(folder_path, f)

        if c % 100 != 0:
            command += " &"

        os.system(command)

        if c % 10000 == 0:
            print(c, f)

print("done")
