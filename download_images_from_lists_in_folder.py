import os,sys

input_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
path_dir_name = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

num_process = 0
for file in os.listdir(input_folder):
    if file.endswith(".json.image_list.txt"):
        file_number = file[:-len(".json.image_list.txt")]
        file_number = int(file_number[file_number.rfind(".")+1:])
        new_folder = os.path.join(output_folder, str(file_number))
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        num_process+=1
        command = "python3 -u "+path_dir_name+"/download_images_from_list.py "+ os.path.join(input_folder, file)+" "+new_folder
        if num_process%20 != 0:
            command+= " &"
        print(command)
        os.system(command)

print("finished downloading all!")