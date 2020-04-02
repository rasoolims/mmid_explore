import os
import sys

image_folder = os.path.abspath(sys.argv[1])
config_folder = os.path.abspath(sys.argv[2])
output_folder = os.path.abspath(sys.argv[3])
num_processes = int(sys.argv[4])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/../code/image_feature_extractor/feature_extractor.py"

commands = []
for folder in os.listdir(image_folder):
    folder_path = os.path.join(image_folder, folder)
    cur_output_folder = os.path.join(output_folder, folder)
    command = "python3 -u " + path_dir_name + " " + " ".join(
        ["--data", folder_path, "--output", cur_output_folder, "--batch 128"])
    commands.append(command)

print("number of commands", len(commands))

split_size = int(len(commands) / num_processes)

print("split size", split_size)

step = 0
for step in range(num_processes + 1):
    start = step * split_size
    end = min(len(commands), start + split_size)

    content = ["#$ -N i_" + str(step)]
    content += ["#$ -o " + os.path.join(config_folder, str(step) + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, str(step) + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=2048:00:00"]
    content += ["#$ -cwd"]
    content += ["source /home1/r/rasooli/torch_env/bin/activate"]
    content += commands[start:end]
    content = "\n".join(content)

    content = "\n".join(content)
    config_path = os.path.join(config_folder, str(step)) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    # os.system(command)

print("Done!")
