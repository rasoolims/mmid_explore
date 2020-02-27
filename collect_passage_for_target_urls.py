import os
import pickle
import sys
import gzip

pickle_folder = os.path.abspath(sys.argv[1])

passage_dict = dict()
with gzip.open(os.path.abspath(sys.argv[2]), "wt") as writer:
    for f in os.listdir(pickle_folder):
        if not f.endswith(".pickle.gz"):
            continue
        print(f)
        current_output = []
        with gzip.open(os.path.join(pickle_folder, f), "rb") as fin:
            cur_dict = pickle.load(fin)
            for target_url in cur_dict.keys():
                try:
                    body_text = list(cur_dict[target_url]["body"].values())

                    whole_text = target_url + "\t" + "\t".join(body_text) + "\n"
                    # Doing this to make sure that the text is ok
                    t = whole_text.encode("utf-8")

                    passage_dict[target_url] = cur_dict[target_url]["title"]+"\t"+ "\t".join(body_text)

                    current_output.append(whole_text)
                except:
                    pass
        writer.write("\n".join(current_output))
        writer.write("\n")

print("dict length", len(passage_dict))
print("finished")
