import gzip
import os
import sys

input_folder = os.path.abspath(sys.argv[1])
folder = sys.argv[2]
folder_path = os.path.join(input_folder, folder)

if input_folder.endswith("/"):
    input_folder = input_folder[-1]
lang_name = os.path.basename(input_folder)

output_file = os.path.join(folder_path, lang_name + folder + ".cat.txt")

lang_name = "<" + lang_name + ">"

with open(output_file, "w") as writer:
    for folder in os.listdir(input_folder):
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
                content = lang_name + " " + " </s> ".join(content) + " </s>"
                output.append(content.strip())

            if len(output) >= 1000:
                writer.write("\n".join(output))
                writer.write("\n")
                output = []
        if len(output) > 0:
            writer.write("\n".join(output))
            writer.write("\n")
print("done with", lang_name)
