import os
import sys
import urllib.request
import gzip
import urllib3
import time

input_file = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

file_indices = []

image_list = [line.strip().split("\t") for line in gzip.open(input_file, 'rt').read().strip().split("\n") if
              len(line.strip().split("\t")) == 2]
print("loaded image_list", len(image_list))
file_number = 0
default_set = {"png", "jpg", "jpeg"}
url_count = 0
start_time = time.time()
for url, text in image_list:
    url_count += 1
    fixed_url = url
    if "?" in fixed_url:
        fixed_url = fixed_url[:fixed_url.find("?")]
    extension = fixed_url[fixed_url.rfind(".") + 1:].lower()
    if extension not in default_set:
        continue
    else:
        file_extension = "."+extension

    file_path = os.path.join(output_folder, str(file_number) + file_extension)

    for tries in range(3):
        try:
            urllib.request.urlretrieve(fixed_url, file_path)
            file_indices.append(str(file_number)+"\t"+fixed_url+"\t"+text)
            file_number += 1
            break
        except:
            pass

    print(str(url_count)+"("+str(time.time()-start_time)+")")
    start_time = time.time()

sys.stdout.write(str(url_count)+"\n")

file_path = os.path.join(output_folder, "index.txt")
open(file_path, "w").write("\n".join(file_indices))

print("Written files", file_number)

