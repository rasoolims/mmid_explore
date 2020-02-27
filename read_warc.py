import os
import sys
import warnings
import json
from bs4 import BeautifulSoup
import  pickle
import validators
import gzip

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", module='bs4')
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def is_good_text(text):
    text = text.lower()
    if len(text) < 2:
        return False
    if len(text.split(" "))<4:
        return False
    if "{" in text or "}" in text or "::" in text:
        return False
    if "lorem ipsum" in text:
        return False
    if "javascript" in text:
        return False
    if "domain name has expired" in text:
        return False
    if "page cannot be displayed" in text:
        return False
    if "page not found" in text:
        return False
    if "<" in text or ">" in text or "*" in text or "//" in text:
        return False

    if "loading" in text:
        return False
    if "~" in text or "_" in text or "+" in text or  "|" in text or  "\\" in text:
        return False
    if "©" in text:
        return False
    if text.startswith("--") or text.startswith("/") or text.startswith(":") or text.startswith("."):
        return False

    if "img" in text:
        return False
    if "\t" in text:
        return False
    if "the document has moved" in text:
        return False
    if "page not found" in text:
        return False
    if text == "image" or text == "picture":
        return False
    return True

def is_relevant_image(url, text):
    if not is_good_text(text):
        return False
    if validators.url(url) is not True:
        return False
    url = url.lower()
    if ".svg" in url:
        return False # Usually these extensions do not have good images
    if text.lower() in url.lower():
        return False
    banned_words = ["logo", "icon", "avatar", "thumbnail"]
    for word in banned_words:
        if word in text or word in url:
            return False
    return True

def process_warc_record(text_information, target_uri):
    try:
        html_text = warc_records[target_uri]

        if "the document has moved" in html_text.lower() or "page not found" in html_text.lower():
            pass
        else:
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
            body_text = {}
            added = set()
            for b in chunks:
                b = b.strip().replace("\r", "").replace("\b", "")
                if "<" in b or len(b.strip()) < 2:
                    continue
                if b.isdigit():
                    continue
                if b in added: # Skip repeats
                    continue
                added.add(b)
                if is_good_text(b):
                    body_text[len(body_text)] = b

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
            if len(body_text)>0:
                text_information[target_uri] = {"body": body_text, "images_with_alt": images}
    except:
        pass



def write_pickle(file_path, text_information):
    print("writing ", file_path)
    with gzip.open(file_path, "wb") as writer:
        pickle.dump(text_information, writer)

input_file_path = os.path.abspath(sys.argv[1])
with gzip.open(input_file_path, "rb") as fin:
    warc_records = pickle.load(fin)

file_path = os.path.abspath(sys.argv[2])

text_information = {}

# instantiating process with arguments
for i, name in enumerate(warc_records.keys()):
    process_warc_record(text_information=text_information, target_uri=name)

write_pickle(file_path, text_information)

with gzip.open(file_path+".image_list.txt.gz", "wt") as writer:
    content_list = []
    for values in text_information.values():
        if "images_with_alt" not in values:
            continue
        images = values["images_with_alt"]
        for url, alt_text in images.items():
            content_list.append("\t".join([url, alt_text]))
    print(file_path, "--> found images", len(content_list))
    writer.write("\n".join(content_list))

print("finished", file_path)
