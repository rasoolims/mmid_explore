import gzip
import html
import json
import os
import re
import sys
import urllib.parse as urlparse

import fasttext

sen_split_reg = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\.|\؟|。|\!|\!|।)\s"
eos = [".", "?", ".", "؟", "。", "!", "!"]


def fix_caption(caption):
    caption = html.unescape(caption.strip())
    caption = re.sub("(([0-9]+x)?[0-9]+)px", "", caption)
    caption = re.sub("([\[]).*?([\]])", "", caption)  # Remove anything between brackets
    caption = re.sub("([{+]).*?([}+])", "", caption).replace("}", "").replace("{",
                                                                              "")  # Remove anything between brackets
    caption = re.sub("([<]).*?([>])", "", caption)  # Remove anything between brackets
    caption = caption.replace("[", "").replace("]", "")
    caption = re.sub("\s+", " ", caption)
    if len(caption) < 3 or "{" in caption:
        return None
    return caption


def clean_text(sen):
    sen = html.unescape(sen.strip())
    sen = re.sub("([<]).*?([>])", "", sen)
    if sen.startswith("http:") or sen.startswith("https:") or sen.startswith("!"):
        return None  # most likely a url
    if "_" in sen:
        return None
    if sen.startswith("--"):
        return None
    sen = re.sub("\s+", " ", sen)
    if len(sen.split(" ")) == 1:
        return None  # Skip one-words
    return sen


def get_text_content(gzip_file, lang):
    with gzip.open(gzip_file, "rt") as reader:
        content = reader.read().strip().split("\n")
        title = content[0]
        sentences = []
        label = "__label__" + lang
        has_label = label in fasttext_model.labels

        full_stop = "\n"
        if lang == "hy":
            full_stop = ":"
        elif lang == "am":
            full_stop = "::"

        for sens in content[1:]:
            # Special treatment for Thai.
            if lang == "th":
                if "(" not in sens and re.search('[0-9a-z]', sens.lower()) is None:
                    full_stop = " "
                else:
                    full_stop = "\n"

            for sen in sens.split(full_stop):
                sen = sen.replace("。", "。 ").strip()
                spl = re.split(sen_split_reg, sen)

                if lang != "en" and re.search('[a-z]', sen.lower()) is not None:
                    # First make sure it has some English character before running fasttext.
                    fasttext_pred = fasttext_model.predict(spl)

                    if has_label:
                        spl = [sentence for i, sentence in enumerate(spl) if
                               fasttext_pred[0][i][0] == label]
                    else:
                        spl = [sentence for i, sentence in enumerate(spl) if
                               fasttext_pred[0][i][0] != "__label__en" or fasttext_pred[1][i][0] < 0.8]

                for s in spl:
                    clean_s = clean_text(s)
                    if clean_s is not None:
                        sentences.append(clean_s)
        return title, sentences


txt_json_folder = os.path.abspath(sys.argv[1])
txt_dir_name = os.path.dirname(txt_json_folder)
lang = os.path.basename(txt_dir_name)
if "_" in lang:
    lang_prefix = lang[:lang.find("_")]
else:
    lang_prefix = lang
wiki_prefix = "https://" + lang_prefix + ".wikipedia.org/wiki/"

fasttext_model = fasttext.load_model(os.path.abspath(sys.argv[3]))

output_folder = os.path.abspath(sys.argv[4])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

min_folder, max_folder = -1, 1000000
if len(sys.argv) > 6:
    min_folder = int(sys.argv[5])
    max_folder = int(sys.argv[6])

output_json_file = output_folder + "/image_index." + lang + ".json"
output_cat_file = output_folder + "/txt." + lang

# Either clean text or json files
mode = "json" if sys.argv[5] == "json" else "txt"

with open(os.path.abspath(sys.argv[2]), 'r', encoding="utf-8") as fp:
    html_to_jpg_maps = json.load(fp)

output_dict = {}

if mode == "txt":
    print("revising wiki pages")
    with open(output_cat_file, "w") as cat_writer:
        for subdir in os.listdir(txt_dir_name):
            subdir_int = int(subdir)
            if subdir_int < min_folder or subdir_int > max_folder:
                continue
            subdir_path = os.path.join(txt_dir_name, subdir)
            if not os.path.isdir(subdir_path):
                continue
            for f in os.listdir(subdir_path):
                f_path = os.path.join(subdir_path, f)
                if not f_path.endswith(".gz"):
                    if os.path.exists(f_path + ".gz"):
                        os.system("rm " + f_path)
                        continue
                    else:
                        os.system("gzip -f " + f_path)
                        f_path += ".gz"
                title, sen = get_text_content(f_path, lang)

                output_dir = os.path.join(output_folder, subdir)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                outputfile = os.path.join(output_dir, f)
                with open(outputfile, "w") as fp:
                    fp.write(title + "\n")
                    fp.write("\n".join(sen))
                    fp.write("\n")
                os.system("gzip -f " + outputfile + " &")
                if len(sen) > 0:
                    cat_writer.write("\n".join(sen))
                    cat_writer.write("\n")
else:
    print("revising caption indices")
    with open(os.path.abspath(sys.argv[1]), 'r', encoding="utf-8") as fp:
        lang_json_dict = json.load(fp)
        for file in lang_json_dict.keys():
            images = {}
            for url_hint in lang_json_dict[file].keys():
                url = wiki_prefix + url_hint
                img_file_path = None

                parsed_link = urlparse.urlsplit(url)
                parsed_link = parsed_link._replace(path=urlparse.quote(parsed_link.path))
                fixed_url = parsed_link.geturl()

                if url in html_to_jpg_maps:
                    info = html_to_jpg_maps[url]
                    img_file_path = info["file_path"]
                    img_url = info["image_url"]
                elif fixed_url in html_to_jpg_maps:
                    info = html_to_jpg_maps[fixed_url]
                    img_file_path = info["file_path"]
                    img_url = info["image_url"]

                if img_file_path is None:
                    continue

                caption = lang_json_dict[file][url_hint]
                corrected_caption = fix_caption(caption)
                if corrected_caption is None:
                    continue
                fasttext_pred = fasttext_model.predict(corrected_caption)
                if fasttext_pred[0][0] == "__label__en" and fasttext_pred[1][0] > 0.9:
                    continue  # English caption
                image = {"caption": corrected_caption, "img_info_url": url, "img_url": img_url, "file": img_file_path}
                images[len(images)] = image
            if len(images) > 0:
                output_dict["pages/" + lang + "/" + file] = images

    with open(output_json_file, 'w', encoding="utf-8") as fp:
        json.dump(output_dict, fp, indent=4)
