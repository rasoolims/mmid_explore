import os
import sys

dump_folder = os.path.abspath(sys.argv[1])
json_info_file = os.path.abspath(sys.argv[2])
fasttext_model = os.path.abspath(sys.argv[3])
config_folder = os.path.abspath(sys.argv[4])
output_folder = os.path.abspath(sys.argv[5])
mode = "txt"
language = sys.argv[6]
min_folder = int(sys.argv[7])
max_folder = int(sys.argv[8])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/collect_wiki_text_info_with_images.py"

for folder in os.listdir(dump_folder):
    if folder != language:
        continue

    for i in range(min_folder, max_folder + 1):
        folder_path = os.path.join(dump_folder, folder)
        txt_json_folder = os.path.join(folder_path, "images.json")
        lang_out_folder = os.path.join(output_folder, os.path.basename(folder))

        content = ["#$ -N c_" + folder]
        content += ["#$ -o " + os.path.join(config_folder, folder + "." + str(i) + ".stdout")]
        content += ["#$ -e " + os.path.join(config_folder, folder + "." + str(i) + ".stderr")]
        content += ["#$ -M rasooli@seas.upenn.edu"]
        content += ["#$ -l h_vmem=20G"]
        content += ["#$ -l mem=20G"]
        content += ["#$ -l h_rt=2048:00:00"]
        content += ["#$ -cwd"]
        content += ["source /home1/r/rasooli/torch_env/bin/activate"]
        command = "python3 -u " + path_dir_name + " " + " ".join(
            [txt_json_folder, json_info_file, fasttext_model, lang_out_folder, mode, str(min_folder), str(max_folder)])
        content += [command]

        content = "\n".join(content)
        config_path = os.path.join(config_folder, folder) + "." + str(i) + ".sh"
        with open(config_path, "w") as writer:
            writer.write(content)
        command = "qsub " + config_path
        print(command)
        os.system(command)

print("Done!")
