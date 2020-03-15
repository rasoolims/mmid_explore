import os
import pickle
import sys

with open(os.path.abspath(sys.argv[1]), "rb") as fin:
    target_uri_dict = pickle.load(fin)

counter = 0
with open(os.path.abspath(sys.argv[3]), "w", encoding="utf-8") as writer:
    for line in open(os.path.abspath(sys.argv[2]), "r", encoding="utf-8"):
        word, correspond_file_path, page_url, image_link = line.split("\t")
        counter += 1
        if counter % 100000 == 0:
            print(counter)
        if page_url in target_uri_dict:
            texts = target_uri_dict[page_url].split("\n")
            contains_text = []
            for text in texts:
                if word.lower() in text.lower():
                    contains_text.append(text)
            if len(contains_text) > 0:
                try:
                    final_text = "\t".join(contains_text)
                    output = line.strip() + "\t" + final_text
                    writer.write(output + "\n")
                except:
                    pass
print("done!")
