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
for i, image in enumerate(image_dict.keys()):
    for i1 in range(len(image_dict[image])):
        sen1 = image_dict[image][i1]
        l1 = sen1.split(" ")[0].replace("<", "").replace(">", "")
        for i2 in range(i1 + 1, len(image_dict[image])):
            sen2 = image_dict[image][i2]
            l2 = sen2.split(" ")[0].replace("<", "").replace(">", "")

            if l1 != l2 or sen1 != sen2:
                first_lang = l1 if l1 < l2 else l2
                second_lang = l2 if l1 < l2 else l1
                lang_pair = first_lang + "2" + second_lang
                basepath = os.path.join(output_folder, lang_pair)
                first_sen = sen1 if l1 < l2 else sen2
                second_sen = sen2 if l1 < l2 else sen1
                with open(basepath + "." + first_lang, "a") as writer:
                    writer.write(first_sen + "\n")
                with open(basepath + "." + second_lang, "a") as writer:
                    writer.write(second_sen + "\n")
    if i%1000==0:
        print(i)

print("done!")
