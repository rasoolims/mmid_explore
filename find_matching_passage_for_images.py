import os,sys, pickle

with open(os.path.abspath(sys.argv[1]), "rb") as fin:
    target_uri_dict = pickle.load(fin)

with open(os.path.abspath(sys.argv[3]), "w") as writer:
    for line in open(os.path.abspath(sys.argv[2]), "r"):
        word, correspond_file_path, page_url, image_link = line.split("\t")
        if page_url in target_uri_dict:
            texts = page_url.split("\n")
            contains_text = []
            for text in texts:
                if word.lower() in text.lower():
                    contains_text.append(text)
            contains_text = " ".join(contains_text)
            writer.write(line+"\t"+contains_text+"\n")
