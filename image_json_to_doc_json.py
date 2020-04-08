import gzip
import json
import os
import re
import sys
from typing import Dict

sen_split_reg = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\.|\؟|。|\!|\!|।)\s"


def split_txt(lang, txt):
    full_stop = "\n"
    if lang == "hy":
        full_stop = ":"
    elif lang == "am":
        full_stop = "::"

    sentences = []
    for sens in txt.split("\n"):
        # Special treatment for Thai.
        if lang == "th":
            if "(" not in sens and re.search('[0-9a-z]', sens.lower()) is None:
                full_stop = " "
            else:
                full_stop = "\n"

        for sen in sens.split(full_stop):
            sen = sen.replace("。", "。 ").strip()
            spl = re.split(sen_split_reg, sen)
            sentences += spl
    lang_rep = "<" + lang + ">"
    caption = (lang_rep + " " + " </s> ".join(sentences)).strip() + " </s>"
    return caption


class Image:
    def __init__(self, lang, image_dict):
        self.info_url = image_dict["img_info_url"]
        self.url = image_dict["img_url"]
        self.img_path = image_dict["file"]
        self.caption = split_txt(lang, image_dict["caption"])

    def exists(self, root_path):
        return os.path.exists(os.path.join(root_path, self.img_path))


class DocumentInfo:
    def __init__(self, root_path, path, lang, image_entries: Dict[str, Dict]):
        self.content = []
        path = os.path.join(root_path, path)
        if not os.path.exists(path):
            path = path + ".gz"
            if not os.path.exists(path):
                self.content = None

        if os.path.exists(path):
            self.content = split_txt(lang, gzip.open(path, "rt").read().strip())

        self.lang = lang
        self.images = []
        for im in image_entries.values():
            image = Image(lang, im)
            if image.exists(root_path):
                self.images.append(image.__dict__)


root_path = os.path.abspath(sys.argv[1])
input_json_file = os.path.abspath(sys.argv[2])
lang = input_json_file[:-5]
lang = lang[lang.rfind(".") + 1:]
output_json_file = os.path.abspath(sys.argv[3])
image_file = os.path.abspath(sys.argv[4])

with open(input_json_file, 'r', encoding="utf-8") as fp:
    json_dict = json.load(fp)

    docs = []
    images = []
    for k, v in json_dict.items():
        doc = DocumentInfo(root_path, k, lang, v)
        if doc.content is not None:
            docs.append(doc)
        images += doc.images
    print(len(docs), len(images))

    with open(output_json_file, 'w', encoding="utf-8") as fp:
        json.dump([doc.__dict__ for doc in docs], fp, indent=4)

    with open(image_file, 'w', encoding="utf-8") as fp:
        for image in images:
            fp.write(image["img_path"] + "\t" + image["caption"] + "\n")
