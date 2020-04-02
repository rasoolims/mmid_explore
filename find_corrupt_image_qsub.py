import os
import sys

image_folder = os.path.abspath(sys.argv[1])
config_folder = os.path.abspath(sys.argv[2])
num_processes = int(sys.argv[3])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
path_dir_name = os.path.dirname(os.path.realpath(__file__)) + "/find_corrupt_images.py"

commands = []
for folder in os.listdir(image_folder):
    folder_path = os.path.join(image_folder, folder)
    command = "python3 -u " + path_dir_name + " " + folder_path
    commands.append(command)

print("number of commands", len(commands))

split_size = int(len(commands) / num_processes)

print("split size", split_size)

step = 0
while True:
    start = step * split_size
    end = min(len(commands), start + split_size)
    if start >= end:
        break
    print(start, end)

    content = ["#$ -N c_" + str(step)]
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

    config_path = os.path.join(config_folder, str(step)) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    step += 1
    os.system(command)

print("Done!")
