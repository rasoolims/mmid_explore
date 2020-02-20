import os
import sys
import warnings
import json
from bs4 import BeautifulSoup
import  pickle
import validators

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", module='bs4')
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def is_relevant_image(url, text):
    text = text.lower()
    if len(text)<2:
        return False
    if validators.url(url) is not True:
        return False
    url = url.lower()
    if ".svg" in url:
        return False # Usually these extensions do not have good images

    banned_words = ["logo", "icon", "avatar", "thumbnail"]
    for word in banned_words:
        if word in text or word in url:
            return False

    if "loading" in text:
        return False
    if "_" in text:
        return False
    if text == "image" or text == "picture":
        return False
    if text in url:
        return False
    return True

def process_warc_record(text_information, target_uri):
    html_text = warc_records[target_uri]
    soup = BeautifulSoup(html_text, features="html.parser", from_encoding="utf-8")

    for script in soup(["script", "style", "a", "menu", "href"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    body = soup.find_all("body")
    body_text_list = "\n".join(b.get_text() for b in body).split("\n")
    body_text = {}
    for b in body_text_list:
        b = b.strip().replace("\r", "").replace("\b", "")
        if "<" in b or len(b.strip()) < 2:
            continue
        if b.isdigit():
            continue
        body_text[len(body_text)] = b

    try:
        title = soup.title.get_text()
    except:
        title = ""
        pass

    title = title.replace("\t", " ").replace("\n", "").replace("\r", "").replace("\b", "")
    images = {}
    imgThis = soup.find_all("img", alt=True)
    for image in imgThis:
        alt_text, src = "", ""
        try:
            alt_text = image["alt"].strip()
            src = image["src"].strip().replace(" ", "%20")
        except:
            try:
                alt_text = image["alt"].strip()
                src = image["data-src"].strip().replace(" ", "%20")
            except:
                pass
        if src.startswith("//"):
            src = src[2:]
        if is_relevant_image(src, alt_text):
            images[src] = alt_text

    text_information[target_uri] = {"title": title, "body": body_text, "images_with_alt": images}


def write_json(file_path, text_information):
    print("writing ", file_path)
    with open(file_path, "w", encoding="utf-8") as writer:
        json.dump(text_information, writer, ensure_ascii=False)

input_file_path = os.path.abspath(sys.argv[1])
with open(input_file_path, "rb") as fin:
    warc_records = pickle.load(fin)

print("loaded warc records with size", len(warc_records))

file_path = os.path.abspath(sys.argv[2])

text_information = {}

# instantiating process with arguments
for i, name in enumerate(warc_records.keys()):
    process_warc_record(text_information=text_information, target_uri=name)
    if(i+1)%1000==0:
        print(input_file_path, i+1)

write_json(file_path, text_information)

with open(file_path+".image_list", "w") as writer:
    content_list = []
    for values in text_information.values():
        images = values["images_with_alt"]
        for url, alt_text in images.items():
            content_list.append("\t".join([url, alt_text]))
    print(file_path, "--> found images", len(content_list))
    writer.write("\n".join(content_list))

print("finished")
