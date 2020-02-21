import os
import pickle
import sys

pickle_folder = os.path.abspath(sys.argv[1])

passage_dict = dict()
for f in os.listdir(pickle_folder):
    if not f.endswith(".pickle"):
        continue
    print(f)
    with open(os.path.join(pickle_folder, f), "rb") as fin:
        cur_dict = pickle.load(fin)
        for target_url in cur_dict.keys():
            try:
                body_text = list(cur_dict[target_url]["body"].values())
                passage_dict[target_url] = cur_dict[target_url]["title"]+"\n"+ "\n".join(body_text)
            except:
                pass

print("dict length", len(passage_dict))
with open(os.path.abspath(sys.argv[2]), "wb") as fout:
    pickle.dump(passage_dict, fout)
