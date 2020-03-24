import os
import sys

input_file = os.path.abspath(sys.argv[1])
folders = os.path.abspath(sys.argv[2])

output_file = os.path.abspath(sys.argv[3])

already_downloaded = 0
count = 0
svg_ignore = 0
with open(output_file, "w") as writer:
    with open(input_file) as reader:
        for line in reader:
            spl = line.strip().split("\t")
            n, url = spl[0].strip(), spl[1].strip()
            extension = url[url.rfind("."):]
            if extension.lower() == ".svg":
                svg_ignore += 1
                continue  # ignoring svg files
            file_name = n + extension
            specific_folder_path = os.path.join(folders, str(int(n) % 1000))
            img_file_path = os.path.join(specific_folder_path, file_name)
            if not os.path.exists(img_file_path):
                writer.write(line.strip() + "\n")
            count += 1
            if count % 10000 == 0:
                print(count)
print("ignored svg files", svg_ignore)
print("done!")
