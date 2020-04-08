import json
import os
import re
import sys
from typing import Dict

sen_split_reg = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\.|\؟|。|\!|\!|।)\s"


def split_caption(lang, caption):
    spl = re.split(sen_split_reg, caption)
    caption = (lang + " " + " </s> ".join(spl)).strip() + " </s>"
    return caption


class Image:
    def __init__(self, root_path, lang, image_dict):
        self.info_url = image_dict["img_info_url"]
        self.url = image_dict["img_url"]
        self.img_file = image_dict["file"]
        self.img_path = os.path.join(root_path, image_dict["file"])
        self.caption = split_caption("<" + lang + ">", image_dict["caption"])

    def exists(self):
        return os.path.exists(self.img_path)


class DocumentInfo:
    def __init__(self, root_path, path, lang, image_entries: Dict[str, Dict]):
        self.path = os.path.join(root_path, path)
        if not os.path.exists(self.path):
            self.path = self.path + ".gz"

        self.lang = lang
        self.images = []
        for im in image_entries.values():
            image = Image(root_path, lang, im)
            if image.exists():
                self.images.append(image.__dict__)

    def exists(self):
        return os.path.exists(self.path)


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
        doc = DocumentInfo("", k, lang, v)
        if doc.exists():
            docs.append(doc)
        images += doc.images
    print(len(docs))

    with open(output_json_file, 'w', encoding="utf-8") as fp:
        for doc in docs:
            json.dump(doc.__dict__, fp, indent=4)

    with open(image_file, 'w', encoding="utf-8") as fp:
        for image in images:
            fp.write(image["img_path"] + "\t" + image["caption"] + "\n")
