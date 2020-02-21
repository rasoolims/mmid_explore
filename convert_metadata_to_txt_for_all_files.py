import os,sys
import glob
import json
import ntpath

# root directory for the image data that has subdirectories.
input_folder = os.path.abspath(sys.argv[1])
index_content = []
for subdir in os.listdir(input_folder):
    subdir_path = os.path.join(input_folder, subdir)
    print(subdir_path)
    for json_name in glob.glob(subdir_path + "/*metadata.json"):
        print(json_name)
        file_prefix = json_name[:json_name.rfind("-")+1]
        file_prefix_path = os.path.join(subdir_path, file_prefix)
        file_prefix = ntpath.basename(file_prefix)
        directory_path = ntpath.basename(os.path.split(file_prefix_path)[0])
        with open(json_name, 'r') as json_file:
            json_data = json.load(json_file)
            word = open(json_name[:-13]+"word.txt","r").read().strip()
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
                correspond_file_path = os.path.join(directory_path , file_prefix+ key + ".jpg")
                index_content.append("\t".join([word, correspond_file_path, page_url, image_link]))

with open(os.path.join(input_folder, "all_indices.txt"), "w") as writer:
    writer.write("\n".join(index_content))

print("finished")
