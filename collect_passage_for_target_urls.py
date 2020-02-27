import os
import pickle
import sys
import gzip

url_info_dict = {}
num_url_lines = 0
print("reading url info dict")
for line in open(os.path.abspath(sys.argv[1])):
    try:
        word, correspond_file_path, page_url, image_link = line.strip().split()
        url_info_dict[page_url] = [word, correspond_file_path]
        num_url_lines+=1
    except:
        pass
print("length of url info dict", len(url_info_dict), num_url_lines)

pickle_folder = os.path.abspath(sys.argv[2])

write_count = 0
with gzip.open(os.path.abspath(sys.argv[3]), "wt") as writer:
    for f in os.listdir(pickle_folder):
        if not f.endswith(".pickle.gz"):
            continue
        print(f, write_count)
        current_output = []
        with gzip.open(os.path.join(pickle_folder, f), "rb") as fin:
            cur_dict = pickle.load(fin)
            for target_url in cur_dict.keys():
                try:
                    body_text = "\t".join(list(cur_dict[target_url]["body"].values()))

                    if target_url in url_info_dict and url_info_dict[target_url][0].lower() in body_text.lower():
                        whole_text = url_info_dict[target_url][1] +"\t"+ body_text + "\n"
                        # Doing this to make sure that the text is ok
                        t = whole_text.encode("utf-8")
                        current_output.append(whole_text)
                        write_count+=1
                except:
                    pass
        writer.write("\n".join(current_output))
        writer.write("\n")

print("finished", write_count)
