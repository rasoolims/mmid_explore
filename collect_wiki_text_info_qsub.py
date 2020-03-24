import os
import sys

dump_folder = os.path.abspath(sys.argv[1])
json_info_file = os.path.abspath(sys.argv[2])
fasttext_model = os.path.abspath(sys.argv[3])
image_folder_prefix = "images/"
config_folder = os.path.abspath(sys.argv[4])
output_folder = os.path.abspath(sys.argv[5])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/collect_wiki_text_info_with_images.py"

for folder in os.listdir(dump_folder):
    folder_path = os.path.join(dump_folder, folder)
    txt_json_folder = os.path.join(folder_path, "images.json")

    content = ["#$ -N c_" + folder]
    content += ["#$ -o " + os.path.join(config_folder, folder + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, folder + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=48:00:00"]
    content += ["#$ -cwd"]
    command = "python3 -u " + path_dir_name + " " + " ".join(
        [txt_json_folder, json_info_file, fasttext_model, image_folder_prefix, output_folder])
    content += [command]

    content = "\n".join(content)
    config_path = os.path.join(config_folder, folder) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    # os.system(command)

print("Done!")
