import os
import pickle
import sys
import gzip
from collections import defaultdict
import fasttext
from detectormorse import detector
tokenizer = detector.default_model()

def tokenize_sentence(input):
    return tokenizer.segments(input)

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
fasttext_path = os.path.abspath(sys.argv[6])
fasttext_model = fasttext.load_model(fasttext_path)
fasttext_lang = "__label__"+target_lang

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
                    body_list = []
                    for line in cur_dict[target_url]["body"].values():
                        if "::" in line:
                            continue
                        print(line)
                        body_list += tokenize_sentence(tokenizer, line)
                    print(body_list)
                    fasttext_pred = fasttext_model.predict(body_list)
                    print(fasttext_pred)
                    body_list = [sentence for i, sentence in enumerate(body_list) if fasttext_pred[0][i][0]==fasttext_lang and fasttext_pred[1][i][0]>0.95]
                    print(body_list)
                    if True: sys.exit(0)

                    if len(body_list)==0:
                        continue

                    body_text = "\t".join(body_list)

                    for file_path, word in url_info_dict[target_url].items():
                        if target_url in url_info_dict and word.lower() in body_text.lower():
                            whole_text = word + "\t" + file_path +"\t"+ body_text
                            # Doing this to make sure that the text is ok
                            t = whole_text.encode("utf-8")

                            short_body = [body for body in body_list if word.lower() in body.lower()]
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
