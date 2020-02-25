import glob
import os
import sys
import warnings
import json
import warc
from bs4 import BeautifulSoup
import pickle

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", module='bs4')
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


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
        try:
            images[image["src"]] = image["alt"]
        except:
            try:
                images[image["data-src"]] = image["alt"]
            except:
                pass

    text_information[target_uri] = {"title": title, "body": body_text, "images_with_alt": images}


def write_dict(file_path, text_information):
    print("writing ", file_path)
    with open(file_path, "wb") as writer:
        pickle.dump(text_information, writer)

warc_path_prefix = os.path.abspath(sys.argv[1])
file_path = os.path.abspath(sys.argv[2])

warc_records = {}
counter = 0
part_number = 1
for warc_path in glob.glob(warc_path_prefix + "*"):
    if not warc_path.endswith("warc") and not warc_path.endswith("warc.gz") and not warc_path.endswith("warcs.tgz"):
        print("skipped", warc_path)
        continue
    try:
        f = warc.open(warc_path)
        print("reading", warc_path)

        for record in f:
            try:
                target_uri = record["WARC-Target-URI"]
                html_text = record.payload.read()
                try:
                    html_text = html_text.decode("utf-8", "ignore")
                except:
                    pass
                warc_records[target_uri] = html_text
            except:
                pass
            counter += 1
            if counter % 10000 == 0:
                write_dict(file_path=file_path+"."+str(part_number),text_information=warc_records)
                part_number+=1
                warc_records = {}
    except:
        print("problem with", warc_path)
        pass

if len(warc_records) >0:
    write_dict(file_path=file_path + "." + str(part_number), text_information=warc_records)
