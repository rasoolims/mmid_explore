import os
import pickle
import sys
import gzip
from collections import defaultdict
from langdetect import detect

url_info_dict = defaultdict(dict)
num_url_lines = 0
print("reading url info dict")
for line in open(os.path.abspath(sys.argv[1])):
    try:
        word, correspond_file_path, page_url, image_link = line.strip().split()
        url_info_dict[page_url][correspond_file_path] = word
        num_url_lines+=1
    except:
        pass
print("length of url info dict", len(url_info_dict), num_url_lines)

pickle_folder = os.path.abspath(sys.argv[2])
target_lang = sys.argv[5]

write_count = 0
with gzip.open(os.path.abspath(sys.argv[3]), "wt") as writer, gzip.open(os.path.abspath(sys.argv[4]), "wt") as short_writer:
    for f in os.listdir(pickle_folder):
        if not f.endswith(".pickle.gz"):
            continue
        print(f, write_count)
        current_output = []
        current_short_output = []
        with gzip.open(os.path.join(pickle_folder, f), "rb") as fin:
            cur_dict = pickle.load(fin)
            for target_url in cur_dict.keys():
                try:
                    body_list = [sentence for sentence in cur_dict[target_url]["body"].values() if detect(sentence)==target_lang]
                    if len(body_list)==0:
                        continue
                        
                    body_text = "\t".join(body_list)

                    for file_path, word in url_info_dict[target_url].items():
                        if target_url in url_info_dict and word.lower() in body_text.lower():
                            whole_text = word + "\t" + file_path +"\t"+ body_text
                            # Doing this to make sure that the text is ok
                            t = whole_text.encode("utf-8")

                            short_body = [body for body in cur_dict[target_url]["body"].values() if word.lower() in body.lower()]
                            short_text =  "\t".join([word, file_path]+short_body)
                            current_output.append(whole_text)
                            current_short_output.append(short_text)
                            write_count+=1
                except:
                    pass
        writer.write("\n".join(current_output))
        writer.write("\n")
        short_writer.write("\n".join(current_short_output))
        short_writer.write("\n")

print("finished", write_count)
