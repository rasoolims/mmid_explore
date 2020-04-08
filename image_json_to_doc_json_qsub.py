import os
import sys

root_path = os.path.abspath(sys.argv[1])
input_folder = os.path.abspath(sys.argv[2])
output_txt_folder = os.path.abspath(sys.argv[3])
output_img_folder = os.path.abspath(sys.argv[4])
config_folder = os.path.abspath(sys.argv[5])

if not os.path.exists(output_txt_folder):
    os.makedirs(output_txt_folder)
if not os.path.exists(output_img_folder):
    os.makedirs(output_img_folder)
if not os.path.exists(config_folder):
    os.makedirs(config_folder)

file_num = 0
json_files = []
output_txt_files = []
output_img_files = []

langs = []
for folder in sorted(os.listdir(input_folder)):
    folder_path = os.path.join(input_folder, folder)
    if not os.path.isdir(folder_path):
        continue
    lang = folder
    json_file = os.path.join(folder_path, "image_index." + lang + ".json")
    json_files.append(json_file)
    new_folder = os.path.join(output_txt_folder, lang + ".json")
    output_txt_files.append(new_folder)
    new_folder = os.path.join(output_img_folder, lang + ".txt")
    output_img_files.append(new_folder)
    langs.append(lang)

print("finished listing all!", len(output_txt_files))
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/image_json_to_doc_json.py"

for i in range(len(json_files)):
    content = ["#$ -N " + langs[i]]
    content += ["#$ -o " + os.path.join(config_folder, langs[i] + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, langs[i] + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=1200:00:00"]
    content += ["#$ -cwd"]

    command = "python3 -u " + path_dir_name + " " + root_path + " " + json_files[i] + " " + output_txt_files[i] + " " + \
              output_img_files[
                  i]
    content += [command]
    content = "\n".join(content)
    config_path = os.path.join(config_folder, langs[i]) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)

    print(command)
    command = "qsub " + config_path
    print(command)
    os.system(command)
