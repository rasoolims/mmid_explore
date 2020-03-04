import os, sys
"""
Input: text file, tab-separated, first: label, second: image path, others: sentences corresponding to image
Output: A folder with 2 subfolders and one text file: image and text folders where the last contains text files 
containing sentences each in one line. Label file: each line contains the label for each image.
"""

target_path = os.path.abspath(sys.argv[2])
image_folder = os.path.join(target_path, "img")
text_path = os.path.join(target_path, "index.txt")

paths = [target_path, image_folder]
for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)
labels = []
image_counter = 0
lines = []
copy_commands = []
for line in open(os.path.abspath(sys.argv[1]), "r"):
    spl = line.strip().split("\t")
    label = spl[0]
    image_path = spl[1]
    image_extension = image_path[image_path.rfind(".")+1:]
    content = "\t".join(spl[2:])

    img_file_name = str(image_counter) + "."+image_extension

    if not os.path.exists(image_path):
        print(image_path, "does not exist")
    else:
        if len(copy_commands)==100:
            copy_command = " ".join(["cp", image_path, os.path.join(image_folder, img_file_name)])
            copy_commands.append(copy_command)
            for command in copy_commands:
                os.system(command)
            copy_commands = []
        else:
            copy_command = " ".join(["cp", image_path, os.path.join(image_folder, img_file_name), "&"])
            copy_commands.append(copy_command)

        output = label +"\t"+ os.path.join(image_folder, img_file_name)+"\t"+content
        lines.append(output)
        image_counter+=1

        if image_counter%1000==0:
            print(image_counter)

for command in copy_commands:
    os.system(command)

with open(text_path, "w") as writer:
    writer.write("\n".join(lines))
            
print(image_counter)
print("finished")
