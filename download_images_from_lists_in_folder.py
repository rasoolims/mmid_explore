import os,sys
import subprocess

input_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
path_dir_name = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

num_process = 0
for file in os.listdir(input_folder):
    if file.endswith(".image_list.txt.gz"):
        file_number = file[:-len(".gz.pickle.gz.image_list.txt.gz")]
    elif file.endswith("image_list.txt.gz"):
        file_number = file[:-len(".json.image_list.txt.gz")]
    else:
        continue
    file_number = int(file_number[file_number.rfind(".")+1:])
    new_folder = os.path.join(output_folder, str(file_number))
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    num_process+=1


    command = ["python3", path_dir_name + "/download_images_from_list.py", os.path.join(input_folder, file), new_folder]
    popopen = subprocess.Popen(command)
    print(os.path.join(input_folder, file))
    if num_process % 40 == 0:
        print("waiting")
        popopen.wait()

print("finished downloading all!")