import os
import sys

input_dir = os.path.abspath(sys.argv[1])
target_path = os.path.abspath(sys.argv[2])

for i, dir in enumerate(os.listdir(input_dir)):
    dir_path = os.path.join(input_dir, dir)

    if not os.path.isdir(dir_path):
        continue

    target_dir = os.path.join(target_path, dir)
    print(target_dir)
    command = "cp " + dir_path + "/*.jpg " + target_dir
    if i % 20 != 0:
        command += " &"
    os.system(command)

print("finished")
