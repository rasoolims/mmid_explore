import os
import sys

root_pic_dir = os.path.abspath(sys.argv[1])
print(root_pic_dir)

root_pic_dir_name = os.path.basename(root_pic_dir)

with open(os.path.join(root_pic_dir, "index.filtered.txt"), "w") as writer:
    for image_folder in os.listdir(root_pic_dir):
        image_folder_dir_name = os.path.basename(image_folder)
        index_path = os.path.join(root_pic_dir, image_folder, "index.txt")
        print(image_folder_dir_name, index_path)
        if not os.path.exists(index_path):
            continue
        with open(index_path, "r") as reader:
            index_content = reader.read().strip().split("\n")

        accepted_content = []
        for line in index_content:
            spl = line.strip().split("\t")

            url = spl[1]
            extension = url[url.rfind("."):]
            file_name = spl[0] + extension
            new_file_name = root_pic_dir_name + "/" + image_folder_dir_name + file_name

            sentence = spl[2]

            accepted_content.append("\t".join([new_file_name, url, sentence]))

        if len(accepted_content) > 0:
            writer.write("\n".join(accepted_content))
            writer.write("\n")
print("done!")
