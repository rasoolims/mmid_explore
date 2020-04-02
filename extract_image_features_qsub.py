import os
import sys

image_folder = os.path.abspath(sys.argv[1])
config_folder = os.path.abspath(sys.argv[2])
output_folder = os.path.abspath(sys.argv[3])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/../code/image_feature_extractor/feature_extractor.py"

for folder in os.listdir(image_folder):
    folder_path = os.path.join(image_folder, folder)
    cur_output_folder = os.path.join(output_folder, folder)

    content = ["#$ -N i_" + folder]
    content += ["#$ -o " + os.path.join(config_folder, folder + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, folder + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=2048:00:00"]
    content += ["#$ -cwd"]
    content += ["source /home1/r/rasooli/torch_env/bin/activate"]
    command = "python3 -u " + path_dir_name + " " + " ".join(
        ["--data", folder_path, "--output", cur_output_folder, "--batch 128"])
    content += [command]
    content = "\n".join(content)
    config_path = os.path.join(config_folder, folder) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    # os.system(command)

print("Done!")
