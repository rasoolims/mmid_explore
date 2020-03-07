import os,sys
import subprocess

input_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
config_folder = sys.argv[3]
process_name = sys.argv[4]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

num_process = 0
file_num = 0
folders = []
output_folders = []

for file in sorted(os.listdir(input_folder)):
    if file.endswith(".gz.pickle.gz.image_list.txt.gz"):
        file_number = file[:-len(".gz.pickle.gz.image_list.txt.gz")]
    elif file.endswith(".json.image_list.txt.gz"):
        file_number = file[:-len(".json.image_list.txt.gz")]
    else:
        continue
    file_num += 1

    file_number = int(file_number[file_number.rfind(".")+1:])
    new_folder = os.path.join(output_folder, str(file_number))
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    folders.append(os.path.join(input_folder, file))
    output_folders.append(new_folder)


print("finished listing all!", len(output_folders))
path_dir_name = os.path.dirname(os.path.realpath(__file__))+"/download_images_from_list.py"

for i in range(len(folders)):
    content = ["#$ -N "+process_name+str(i)]
    content += ["$ -o "+process_name+str(i)+".out"]
    content += ["$ -e "+process_name+str(i)+".err"]
    content += ["#$ -cwd"]
    command = "python3 -u " + path_dir_name +" "+folders[i]+" "+output_folders[i]
    content += [command]
    content = "\n".join(content)
    config_path =  os.path.join(config_folder, str(i))+ ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    os.system(command)
