import os
import sys

input_file = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
config_folder = sys.argv[3]
num_

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

file_num = 0
folders = []
output_folders = []

langs = []
for file in sorted(os.listdir(input_folder)):
    folders.append(os.path.join(input_folder, file))
    outfile_name = file
    if "." in file:
        outfile_name = file[:file.find(".")]
    new_folder = os.path.join(output_folder, outfile_name)
    output_folders.append(new_folder)
    langs.append(file)

print("finished listing all!", len(output_folders))
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "../ImageTranslate/wiki/extract_wikipedia_language_links.py"

for i in range(len(folders)):
    content = ["#$ -N " + langs[i]]
    content += ["#$ -o " + os.path.join(config_folder, langs[i] + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, langs[i] + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=1200:00:00"]
    content += ["#$ -cwd"]

    command = "python3 -u " + path_dir_name + " " + folders[i] + " " + output_folders[i]
    content += [command]
    content = "\n".join(content)
    config_path = os.path.join(config_folder, langs[i]) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)

    command = "qsub " + config_path
    print(command)
    os.system(command)
