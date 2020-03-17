import os
import sys

input_folder = os.path.abspath(sys.argv[1])
config_folder =  os.path.abspath(sys.argv[2])
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/download_wiki_img_from_list.py"

if not os.path.exists(config_folder):
    os.makedirs(config_folder)

all_folders = os.listdir(input_folder)
for i in range(0, len(all_folders), 10) :
    folder_path = os.path.join(input_folder, all_folders[i])
    content = ["#$ -N " + all_folders[i]]
    content += ["#$ -o " + os.path.join(config_folder, all_folders[i] + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, all_folders[i] + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=48:00:00"]
    content += ["#$ -cwd"]
    for j in range(i, min(i+10, len(all_folders))):
        content += ["python3 -u " + path_dir_name  +"  "+ all_folders[j] + " 512 512"]

    content = "\n".join(content)
    config_path = os.path.join(config_folder, all_folders[i]) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    #os.system(command)

print("done")