import os, sys
import warc
from bs4 import BeautifulSoup
import glob
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", module='bs4')
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

import json

warc_path_prefix = os.path.abspath(sys.argv[1])

text_information = {}
counter = 0
alt_text_count = 0
for warc_path in glob.glob(warc_path_prefix+"*"):
    if not warc_path.endswith("warc") and not warc_path.endswith("warc.gz") and not warc_path.endswith("warcs.tgz"):
        print("skipped", warc_path)
        continue
    try:
        f = warc.open(warc_path)
        print("reading", warc_path)

        for record in f:
            try:
                target_uri = record["WARC-Target-URI"]
                html_text =  record.payload.read()
                try:
                    html_text = html_text.decode("utf-8", "ignore")
                except: pass


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
                    b = b.strip().replace("\r","").replace("\b","")
                    if "<" in b or len(b.strip())<2:
                        continue
                    if b.isdigit():
                        continue
                    body_text[len(body_text)] = b

                try:
                    title=soup.title.get_text()
                except: pass

                title = title.replace("\t", " ").replace("\n","").replace("\r","").replace("\b","")
                images = {}
                imgThis = soup.find_all("img", alt=True)
                for image in imgThis:
                    try:
                        images[image["src"]] = image["alt"]
                        alt_text_count+=1
                    except:
                        try:
                            images[image["data-src"]] = image["alt"]
                            alt_text_count += 1
                        except:
                            pass

                text_information[target_uri] = {"title":title, "body": body_text, "images_with_alt": images}
                counter +=1
                if counter%1000==0:
                    sys.stdout.write(str(counter)+"("+str(alt_text_count)+")...")
            except:
                sys.stdout.write("skipped this one...")
    except:
        print("exception in reading this warc file; finished unexpectedly!")

    sys.stdout.write(str(counter)+"("+str(alt_text_count)+")\n")

print("writing...")
with open(os.path.abspath(sys.argv[2]), "w", encoding="utf-8") as writer:
    json.dump(text_information, writer, ensure_ascii=False)


print("finished")