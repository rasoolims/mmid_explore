import os
import sys

input_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
config_folder = sys.argv[3]
max_jobs = int(sys.argv[4])

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

file_num = 0
folders = []
output_folders = []

langs = []
for file in sorted(os.listdir(input_folder)):
    new_folder = os.path.join(output_folder, file)
    folders.append(os.path.join(input_folder, file))
    output_folders.append(new_folder)
    langs.append(file)

print("finished listing all!", len(output_folders))
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/download_html_from_wiki_list.py"

already_downloaded = 0
to_run, completed = 0, 0
skipped = 0
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
    if to_run < max_jobs:
        to_run += 1
        print(command)
        os.system(command)
    else:
        skipped += 1
print("already_downloaded", already_downloaded)
print("to_run", to_run, "completed", completed, "skipped", skipped)
