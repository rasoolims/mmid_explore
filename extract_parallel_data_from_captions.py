import os
import sys
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_dict = defaultdict(list)
for file in os.listdir(input_folder):
    print(file)
    with open(os.path.join(input_folder, file), "r") as fp:
        for line in fp:
            image, caption = line.strip().split("\t")
            image_dict[image].append(caption)

parallel_data = defaultdict(list)
print("construct parallel data from", len(image_dict), "images!")
file_handers = {}
for image in image_dict.keys():
    for i1 in range(len(image_dict[image])):
        sen1 = image_dict[image][i1]
        l1 = sen1.split(" ")[0].replace("<", "").replace(">", "")
        for i2 in range(i1 + 1, len(image_dict[image])):
            sen2 = image_dict[image][i2]
            l2 = sen2.split(" ")[0].replace("<", "").replace(">", "")

            if l1 != l2 or sen1 != sen2:
                first_lang = l1  if l1 < l2 else l2
                second_lang = l2  if l1 < l2 else l1
                lang_pair = first_lang + "2" + second_lang
                if not lang_pair in file_handers:
                    basepath = os.path.join(output_folder, lang_pair)
                    file_handers[lang_pair+"." + first_lang] = open(basepath + "." + first_lang, "w")
                    file_handers[lang_pair + "." + second_lang] = open(basepath + "." + second_lang, "w")
                first_sen = sen1 if l1 < l2 else sen2
                second_sen = sen2 if l1 < l2 else sen1
                parallel_data[lang_pair].append(first_sen + "\t" + second_sen)

for fh in file_handers.keys():
    file_handers[fh].close()

print("done!")
