import gzip
import os
import sys

input_folder = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

if input_folder.endswith("/"):
    input_folder = input_folder[-1]
lang_name = os.path.basename(input_folder)
lang_name = "<" + lang_name + ">"

with open(output_file, "w") as writer:
    for folder in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder)
        if not os.path.isdir(folder_path):
            continue
        print("reading folder", folder_path)
        output = []
        for file in os.listdir(folder_path):
            if not file.endswith(".gz"):
                continue

            file_path = os.path.join(folder_path, file)
            with gzip.open(file_path, "rt") as reader:
                content = reader.read().strip().split("\n")
                content = lang_name + " " + " </s> ".join(content) +" </s>"
                output.append(content.strip())

        writer.write("\n".join(output))
        writer.write("\n")
print("done with", lang_name)
