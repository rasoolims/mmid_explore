import os
import sys
from collections import defaultdict
import re
import json

def fix_caption(caption):
    caption = re.sub("(([0-9]+x)?[0-9]+)px", "", caption)
    caption = re.sub("([\[]).*?([\]])", "", caption)  # Remove anything between brackets
    caption = re.sub("([{+]).*?([}+])", "", caption).replace("}", "").replace("{",
                                                                              "")  # Remove anything between brackets
    caption = caption.replace("[", "").replace("]", "")
    if len(caption) < 3 or "{" in caption:
        return None

    return caption

html_url_file = os.path.abspath(sys.argv[1])
html2image_map = os.path.abspath(sys.argv[2])
image_url_file = os.path.abspath(sys.argv[3])
output_file = os.path.abspath(sys.argv[4])

html_file_to_caption_dict = {}
image_url_to_html_file_dict = defaultdict(set)
caption_maps = defaultdict(dict)

url_set = set()
url_counts = 0
print("reading html url file")
with open(html_url_file, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) < 4: continue
        file_num  = spl[0]
        lang = spl[1]
        url = spl[2]
        caption = " ".join(spl[3:])
        caption = fix_caption(caption)
        if url.lower().endswith(".svg"):
            # Ignoring all svg files
            continue
        if caption is None:
            continue
        html_file_to_caption_dict[file_num] = caption, lang
        if (c+1)%1000000==0:
            print(c+1)

print("reading image url file")
with open(html2image_map, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) != 2: continue
        file_num, url = spl
        if file_num in html_file_to_caption_dict:
            image_url_to_html_file_dict[url].add(file_num)
        if (c+1)%1000000==0:
            print(c+1)

print("Merging captions")
total_images = 0
with open(image_url_file, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) < 2: continue

        file_num, url = spl

        if url in image_url_to_html_file_dict:
            for html_file_num in image_url_to_html_file_dict[url]:
                caption, lang = html_file_to_caption_dict[html_file_num]
                if lang not in caption_maps:
                    caption_maps[url][lang] = defaultdict(set)

                caption_maps[file_num][lang].add(caption)
                total_images += 1
        if (c+1)%1000000==0:
            print(c+1)

with open(output_file, 'w') as fp:
    json.dump(caption_maps, fp)
print("wrote everything", len(caption_maps), total_images)