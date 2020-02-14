import os,sys
import glob

input_dir = os.path.abspath(sys.argv[1])
target_path = os.path.abspath(sys.argv[2])
min_num_files = int(sys.argv[3])  # Minimum number of files to move into the validation folder
max_ratio = float(sys.argv[4]) # Maximum percent of files in

if not os.path.exists(target_path):
    os.makedirs(target_path)

for dir in os.listdir(input_dir):
    dir_path = os.path.join(input_dir, dir)

    if not os.path.isdir(dir_path):
        continue

    target_dir = os.path.join(target_path, dir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    num_of_jpg_files = len(glob.glob1(dir_path, "*.jpg"))
    num_to_sample = max(min_num_files, int(max_ratio * num_of_jpg_files))
    sampled = 0

    for f in os.listdir(dir_path):
        if f.endswith(".jpg"):
            file_path = os.path.join(dir_path, f)
            new_file_path = os.path.join(target_dir, f)
            move_command = " ".join(["mv", file_path, new_file_path, "&"])
            sampled+=1
            os.system(move_command)
            if sampled>=num_to_sample:
                break
    copy_command = " ".join(["cp", dir_path+"/*.txt", target_dir+"/ "])
    print(copy_command)
    os.system(copy_command)

    copy_command = " ".join(["cp", dir_path + "/*.json", target_dir + "/ "])
    print(copy_command)
    os.system(copy_command)

    copy_command = " ".join(["cp", dir_path + "/*.jsonl", target_dir + "/ "])
    print(copy_command)
    os.system(copy_command)

print("finished")
