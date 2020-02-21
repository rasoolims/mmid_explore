import os,sys, pickle,json

with open(os.path.abspath(sys.argv[1]), "rb") as fin:
    target_uri_dict = pickle.load(fin)

counter = 0
with open(os.path.abspath(sys.argv[3]), "w", encoding="utf-8") as writer:
    image_text_dict = {}
    for line in open(os.path.abspath(sys.argv[2]), "r"):
        word, correspond_file_path, page_url, image_link = line.split("\t")
        counter+=1
        if counter %100000==0:
            print(counter)
        if page_url in target_uri_dict:
            texts = target_uri_dict[page_url].split("\n")
            contains_text = []
            for text in texts:
                if word.lower() in text.lower():
                    contains_text.append(text)
            if len(contains_text)>0:
                contains_text_dict = {i:text for i, text in enumerate(contains_text)}
                image_text_dict[correspond_file_path] = {"word":word, "text":contains_text_dict, "url": page_url, "image":image_link}
    json.dump(image_text_dict, writer, ensure_ascii=False)

print("done!")