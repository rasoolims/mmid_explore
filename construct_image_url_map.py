import os
import sys
from collections import defaultdict
import re
import json
import urllib.parse as urlparse

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
image_paths = os.path.abspath(sys.argv[4])
output_file = os.path.abspath(sys.argv[5])

html_file_to_caption_dict = {}
image_url_to_html_file_dict = defaultdict(set)

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
        html_file_to_caption_dict[file_num] = caption, lang, url
        if (c+1)%1000000==0:
            print(c+1)

print("reading image url file")
with open(html2image_map, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) != 2: continue
        file_num, url = spl
        parsed_link = urlparse.urlsplit(url)
        parsed_link = parsed_link._replace(path=urlparse.quote(parsed_link.path))
        fixed_url = parsed_link.geturl()
        if file_num in html_file_to_caption_dict:
            image_url_to_html_file_dict[fixed_url].add(file_num)
        if (c+1)%1000000==0:
            print(c+1)


image_file_paths = {}
print("reading image file paths")
with open(image_paths, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) != 2:
            print("hi!")
            continue
        file_num, path = spl
        image_file_paths[file_num] = path
        if (c+1)%1000000==0:
            print(c+1)

html_to_jpg_maps = {}
to_remove_writer = open(output_file+".remove", "w")
print("Merging captions")
caption_maps = defaultdict(dict)
total_images = 0
file_num_exists = 0
with open(image_url_file, "r") as reader:
    for c, line in enumerate(reader):
        spl = line.strip().split("\t")
        if len(spl) < 2: continue

        file_num, url = spl
        extension = url[url.rfind("."):]
        parsed_link = urlparse.urlsplit(url)
        parsed_link = parsed_link._replace(path=urlparse.quote(parsed_link.path))
        url = parsed_link.geturl()

        if file_num not in image_file_paths:
            continue
        else:
            file_num_exists += 1
        file_path = image_file_paths[file_num]

        if url in image_url_to_html_file_dict:
            for html_file_num in image_url_to_html_file_dict[url]:
                caption, lang, html_url = html_file_to_caption_dict[html_file_num]
                if lang not in caption_maps:
                    caption_maps[file_path][lang] = {}
                cur_len = len(caption_maps[file_path][lang])
                caption_maps[file_path][lang][cur_len] = {"caption": caption, "url": url, "html_url":html_url}
                html_to_jpg_maps[html_url] = {"file_path": file_path, "image_url": url}
                total_images += 1
        else:
            folder_num = str(int(file_num)%1000)
            to_remove_writer.write("rm " + folder_num+"/"+file_num+extension+" \n")
        if (c+1)%1000000==0:
            print(c+1)

with open(output_file, 'w', encoding="utf-8") as fp:
    json.dump(caption_maps, fp, indent=4)
with open(output_file+".html_info.json", 'w', encoding="utf-8") as fp:
    json.dump(html_to_jpg_maps, fp, indent=4)
print("wrote everything", len(caption_maps), total_images, file_num_exists, len(html_to_jpg_maps))
to_remove_writer.close()