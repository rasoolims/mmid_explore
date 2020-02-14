import sys,os
from collections import defaultdict
import glob

index_file = os.path.abspath(sys.argv[1])
input_folder = os.path.abspath(sys.argv[2]) # Can be starting index of folder names (in case of English)
target_dir = os.path.abspath(sys.argv[3])
matching_languages = set(sys.argv[4].split(",")) # Devided by comma
allowed_indices = set()

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

index_dict = defaultdict(dict)
for line in open(index_file, 'r'):
    language_id, orig_index, new_index = line.strip().split("\t")
    index_dict[language_id][orig_index] = new_index
    if language_id in matching_languages:
        allowed_indices.add(new_index)

print("number of allowed indices", len(allowed_indices))

for name in glob.glob(input_folder+"*"):
    if not os.path.isdir(name):
        continue
    language_id = name[name.rfind("/")+1:]
    language_id = language_id[language_id.find("-")+1: language_id.find("-package")]
    print(language_id, name)
    for subdir in os.listdir(name):
        subdir_path = os.path.join(name, subdir)
        if not os.path.isdir(subdir_path):
            continue
        new_id = index_dict[language_id][subdir]
        if new_id not in allowed_indices:
            continue

        new_path = os.path.join(target_dir, new_id)
        if not os.path.exists(new_path):
            print("creating", new_path)
            os.makedirs(new_path)

        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            new_file_path = new_path+"/"+language_id+"-"+subdir +"-"+file
            copy_command = " ".join(["cp", file_path, new_file_path])
            os.system(copy_command)
