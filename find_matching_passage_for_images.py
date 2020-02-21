import os,sys, pickle

with open(os.path.abspath(sys.argv[1]), "rb") as fin:
    target_uri_dict = pickle.load(fin)

counter = 0
with open(os.path.abspath(sys.argv[3]), "w") as writer:
    for line in open(os.path.abspath(sys.argv[2]), "r"):
        word, correspond_file_path, page_url, image_link = line.split("\t")
        counter+=1
        if counter %1000==0:
            print(counter)
        if page_url in target_uri_dict:
            texts = page_url.split("\n")
            contains_text = []
            for text in texts:
                if word.lower() in text.lower():
                    contains_text.append(text)
            if len(contains_text)>0:
                contains_text = " ".join(contains_text)
                writer.write(line+"\t"+contains_text+"\n")
print("done!")