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
file_cache = defaultdict(list)
for i, image in enumerate(image_dict.keys()):
    for i1 in range(len(image_dict[image])):
        sen1 = image_dict[image][i1]
        l1 = sen1.split(" ")[0].replace("<", "").replace(">", "")
        for i2 in range(i1 + 1, len(image_dict[image])):
            sen2 = image_dict[image][i2]
            l2 = sen2.split(" ")[0].replace("<", "").replace(">", "")

            if l1 != l2 and sen1 != sen2:
                first_lang = l1 if l1 < l2 else l2
                second_lang = l2 if l1 < l2 else l1
                lang_pair = first_lang + "2" + second_lang
                first_sen = sen1 if l1 < l2 else sen2
                second_sen = sen2 if l1 < l2 else sen1
                if "=" in first_sen or first_sen == "thumb" or first_sen == "left" or first_sen == "right" or first_sen == "thumbnail":
                    continue
                if "=" in second_sen or second_sen == "thumb" or second_sen == "left" or second_sen == "right" or second_sen == "thumbnail":
                    continue

                first_sen = first_sen.replace(" </s> ", " ")
                second_sen = second_sen.replace(" </s> ", " ")
                file_cache[output_folder + "/" + first_lang + "2" + second_lang].append(first_sen)
                file_cache[output_folder + "/" + second_lang + "2" + first_lang].append(second_sen)

    if (i + 1) % 100000 == 0:
        print(i+1, len(image_dict))
        for file in file_cache.keys():
            with open(file, "a") as writer:
                writer.write("\n".join(file_cache[file]))
                writer.write("\n")
        file_cache = defaultdict(list)
        print(i + 1)

for file in file_cache.keys():
    with open(file, "a") as writer:
        writer.write("\n".join(file_cache[file]))
        writer.write("\n")

print("done!")
