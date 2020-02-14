import os,sys
import glob

input_dir = os.path.abspath(sys.argv[1])
target_path = os.path.abspath(sys.argv[2])

for dir in os.listdir(input_dir):
    dir_path = os.path.join(input_dir, dir)

    if not os.path.isdir(dir_path):
        continue

    target_dir = os.path.join(target_path, dir)
    print(target_dir)

    os.system("cp "+dir_path+"/*.jpg "+target_dir)

print("finished")
