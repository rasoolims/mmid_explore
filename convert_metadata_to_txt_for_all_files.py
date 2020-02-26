import glob
import json
import ntpath
import os
import sys

# root directory for the image data that has subdirectories.
input_folder = os.path.abspath(sys.argv[1])
index_content = []
num_processed = 0

print("input folder", input_folder)
for folder_matches in glob.glob(input_folder+"*"):
    print("reading ", folder_matches)
    if not os.path.isdir(folder_matches):
        continue
    for subdir in os.listdir(folder_matches):
        subdir_path = os.path.join(folder_matches, subdir)

        for json_name in glob.glob(subdir_path + "/*metadata.json"):
            num_processed += 1
            if num_processed % 1000 == 0:
                print(num_processed)
            file_prefix = json_name[:json_name.rfind("-") + 1]
            file_prefix_path = os.path.join(subdir_path, file_prefix)
            file_prefix = ntpath.basename(file_prefix)
            directory_path = subdir_path
            if directory_path.endswith("/"):
                directory_path = directory_path[:-1]
            if "/" in directory_path:
                directory_path = directory_path[directory_path.rfind("/") + 1:]

            with open(json_name, 'r') as json_file:
                json_data = json.load(json_file)
                word = open(json_name[:-13] + "word.txt", "r").read().strip()
                for key in json_data:
                    try:
                        image_link = json_data[key]["image_link"]
                    except:
                        image_link = "-"
                    try:
                        page_url = json_data[key]["google"]["ru"]
                    except:
                        page_url = "-"
                    try:
                        original_filename = json_data[key]["original_filename"]
                    except:
                        original_filename = "-"
                    correspond_file_path = subdir_path + "/" + key + ".jpg"
                    index_content.append("\t".join([word, correspond_file_path, page_url, image_link]))

with open(os.path.abspath(sys.argv[2]), "w") as writer:
    writer.write("\n".join(index_content))

print("finished")
