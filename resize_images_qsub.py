import os
import sys

input_folder = os.path.abspath(sys.argv[1])
config_folder =  os.path.abspath(sys.argv[2])
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/download_wiki_img_from_list.py"

if not os.path.exists(config_folder):
    os.makedirs(config_folder)

for folder in os.listdir(input_folder):
    print(folder)
    folder_path = os.path.join(input_folder, folder)
    content = ["#$ -N " + folder]
    content += ["#$ -o " + os.path.join(config_folder, folder + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, folder + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=48:00:00"]
    content += ["#$ -cwd"]
    command = "python3 -u " + path_dir_name  + folder_path + " 512 512"
    content += [command]
    content = "\n".join(content)
    config_path = os.path.join(config_folder, folder) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    #os.system(command)

print("done")