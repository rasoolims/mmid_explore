import os
import sys
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])
use_all_langs = True
sub_langs = None

if len(sys.argv) > 3:
    sub_langs = set(sys.argv[3].strip().split(","))
    use_all_langs = False

image_dict = defaultdict(list)
for file in os.listdir(input_folder):
    if not use_all_langs:
        if file[:-4] not in sub_langs:
            continue
    print(file)
    with open(os.path.join(input_folder, file), "r") as fp:
        for line in fp:
            image, caption = line.strip().split("\t")
            image_dict[image].append(caption)

print("writing...")
with open(output_file, "w") as fp:
    for image in image_dict.keys():
        output = "\t".join([image] + image_dict[image])
        fp.write(output)
        fp.write("\n")
print("done!")
