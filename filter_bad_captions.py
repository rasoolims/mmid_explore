import json
import os
import sys
from collections import defaultdict

"""
Remove those captions in other languages that are exactly the same as the English caption
"""

deleted_captions = 0
lang_dict = defaultdict(int)
html_to_jpg_maps = {}
with open(os.path.abspath(sys.argv[1]), "r") as reader:
    caption_dict = json.load(reader)
    print("number of images", len(caption_dict))

    for k in caption_dict.keys():
        if "en" in caption_dict[k]:
            en_captions = {entry["caption"] for entry in caption_dict[k]["en"]}

            to_del = []
            for lang in caption_dict[k].keys():
                if lang == "en":
                    continue

                new_caption_list = []
                for entry in caption_dict[k][lang]:
                    caption = entry["caption"]
                    if (len(caption.split(" ")) < 5 and caption in en_captions) or caption not in en_captions:
                        new_caption_list.append(entry)
                    else:
                        print(lang, caption)

                if len(new_caption_list) == 0:
                    to_del.append(lang)
                    deleted_captions += len(caption_dict[k][lang])
                elif len(caption_dict[k][lang]) != len(new_caption_list):
                    caption_dict[k][lang] = new_caption_list
                    deleted_captions += len(caption_dict[k][lang]) - len(new_caption_list)

            for lang in to_del:
                del caption_dict[k][lang]

            for lang in caption_dict[k].keys():
                for v in caption_dict[k][lang]:
                    html_to_jpg_maps[v["html_url"]] = {"file_path": k, "image_url": v["url"]}

print("deleted captions", deleted_captions)
output_file = os.path.abspath(sys.argv[2])
with open(output_file, 'w', encoding="utf-8") as fp:
    json.dump(caption_dict, fp, indent=4)
with open(output_file + "html_info.json", 'w', encoding="utf-8") as fp:
    json.dump(html_to_jpg_maps, fp, indent=4)
