import os
import sys

input_folder = os.path.abspath(sys.argv[1])
config_folder = os.path.abspath(sys.argv[2])
output_folder = os.path.abspath(sys.argv[3])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/extract_wiki_dump_pages.py"

for file in os.listdir(input_folder):
    if not file.endswith(".xml"):
        continue

    lang_name = file[:file.find("wiki")]

    lang_folder = os.path.join(output_folder, lang_name)
    file_path = os.path.join(input_folder, file)

    content = ["#$ -N resize_" + lang_name]
    content += ["#$ -o " + os.path.join(config_folder, lang_name + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, lang_name + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=48:00:00"]
    content += ["#$ -cwd"]
    command = "python3 -u " + path_dir_name + " " + file_path + " " + lang_folder
    content += [command]

    content = "\n".join(content)
    config_path = os.path.join(config_folder, lang_name) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    os.system(command)

print("Done!")
