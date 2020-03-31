import math
import os
import sys

page_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
config_folder = os.path.abspath(sys.argv[3])
num_processes = int(sys.argv[4])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/cat_wiki_gz_files_with_lang_id.py"

commands = []
for folder in os.listdir(page_folder):
    folder_path = os.path.join(page_folder, folder)
    output_file = os.path.join(output_folder, folder + ".txt")

    for sub_folder in os.listdir(folder_path):
        command = "python3 -u " + path_dir_name + " " + " ".join([folder_path, output_file, sub_folder])
        commands += [command]

print("number of commands", len(commands))

split_size = math.ceil(len(commands) / num_processes)

print("split size", split_size)

for com_num in range(0, len(commands), split_size):
    end = min(len(commands), com_num + split_size)

    content = ["#$ -N c_" + str(com_num)]
    content += ["#$ -o " + os.path.join(config_folder, str(com_num) + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, str(com_num) + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=2048:00:00"]
    content += ["#$ -cwd"]
    content += ["source /home1/r/rasooli/torch_env/bin/activate"]
    content += commands[com_num:end]
    content = "\n".join(content)
    config_path = os.path.join(config_folder, str(com_num)) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    # os.system(command)

print("Done!")
