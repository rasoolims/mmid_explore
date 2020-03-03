import os, sys
"""
Input: text file, tab-separated, first: label, second: image path, others: sentences corresponding to image
Output: A folder with 3 subfolders: label, image, text where the last contains text files containing sentences each in
one line
"""

target_path = os.path.abspath(sys.argv[2])
image_folder = os.path.join(target_path, "img")
label_path = os.path.join(target_path, "label")
text_path = os.path.join(target_path, "txt")

paths = [target_path, image_folder, label_path, text_path]
for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)

image_counter = 0
for line in open(os.path.abspath(sys.argv[1]), "r"):
    spl = line.strip().split("\t")
    label = spl[0]
    image_path = spl[1]
    image_extension = image_path[image_path.rfind(".")+1:]
    content = "\n".join(spl[2:])

    img_file_name = str(image_counter) + "."+image_extension
    txt_file_name = str(image_counter) + ".txt"
    if not os.path.exists(image_path):
        print(image_path, "does not exist")
    else:
        copy_command = " ".join(["cp", image_path, os.path.join(image_folder, img_file_name), "&"])
        os.system(copy_command)

        with open(os.path.join(label_path, txt_file_name), "w") as writer:
            writer.write(label)

        with open(os.path.join(text_path, txt_file_name), "w") as writer:
            writer.write(content)

        image_counter+=1

        if image_counter%1000==0:
            print(image_counter)

print(image_counter)
print("finished")
