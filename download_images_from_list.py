import os
import sys
from collections import defaultdict
import urllib.request

input_file = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

file_indices = defaultdict(list)

image_list = [line.strip().split("\t") for line in open(input_file, 'r').read().strip().split("\n") if
              len(line.strip().split("\t")) == 2]
file_number = defaultdict(int)
default_set = set(["png", "jpg", "jpeg", "gif"])
written_files = 0
url_count = 0
for url, text in image_list:
    url_count += 1
    fixed_url = url
    if "?" in fixed_url:
        fixed_url = fixed_url[:fixed_url.find("?")]
    extension = fixed_url[fixed_url.rfind(".") + 1:].lower()
    if extension not in default_set:
        extension = "others"
        file_extension = ".jpg" # Assuming default is jpg
    else:
        file_extension = "."+extension

    dir_path = os.path.join(output_folder, extension)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, str(file_number[extension]) + file_extension)

    for tries in range(5):
        try:
            urllib.request.urlretrieve(fixed_url, file_path)
            file_indices[extension].append(str(file_number[extension])+"\t"+fixed_url+"\t"+text)
            file_number[extension] += 1
            written_files+=1
            break
        except:
            try:
                urllib.request.urlretrieve(url, file_path)
                file_indices[extension].append(str(file_number[extension]) + "\t" + fixed_url + "\t" + text)
                file_number[extension] += 1
                written_files += 1
                break
            except:
                pass
    if url_count%100==0:
        sys.stdout.write(str(url_count)+"...")

sys.stdout.write(str(url_count)+"\n")

for extension in os.listdir(output_folder):
    file_path = os.path.join(output_folder, extension, "index.txt")
    open(file_path, "w").write("\n".join(file_indices[extension]))

print("Written files", written_files)

