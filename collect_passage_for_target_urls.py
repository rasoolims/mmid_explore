import os
import pickle
import sys
import gzip

pickle_folder = os.path.abspath(sys.argv[1])

passage_dict = dict()
for f in os.listdir(pickle_folder):
    if not f.endswith(".pickle.gz"):
        continue
    print(f)
    with gzip.open(os.path.join(pickle_folder, f), "rb") as fin:
        cur_dict = pickle.load(fin)
        for target_url in cur_dict.keys():
            try:
                body_text = list(cur_dict[target_url]["body"].values())
                passage_dict[target_url] = cur_dict[target_url]["title"]+"\n"+ "\n".join(body_text)
            except:
                pass

output_text = "\n".join([key+"\t"+value for key,value in passage_dict.items()])
print("dict length", len(passage_dict))
with gzip.open(os.path.abspath(sys.argv[2]), "wt") as writer:
    writer.write("\n".join(output_text))
print("finished")
