import os
import sys


def process_info_line(lang, line):
    wiki_prefix = "https://" + lang + ".wikipedia.org/wiki/"
    line = line.strip()
    if not line.startswith("[[") or not line.endswith("]]"):
        return None
    if "|" not in line or ":" not in line:
        return None
    line = line.replace("[[", "").replace("]]", "")
    spl = line.strip().split("|")
    accepted_spls = []
    for s in spl:
        if "=" not in s and not s.endswith("px"):
            accepted_spls.append(s)

    if len(accepted_spls) <= 2:
        return None
    if ":" not in spl[0]:
        return None
    wikipedia_path = wiki_prefix + spl[0]
    caption = spl[-1].strip()
    if len(caption) < 3:
        return None

    return lang + "\t" + wikipedia_path.replace(" ", "_") + "\t" + caption


wikimedia_url_prefix = "https://commons.wikimedia.org/wiki/File:"
wikipedia_url_prefix = "https://[lang].wikipedia.org/wiki/"
wiki_folder = os.path.abspath(sys.argv[1])
out_folder = os.path.abspath(sys.argv[2])

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

url_id = 0
for wiki_lang_folder in os.listdir(wiki_folder):
    lang = os.path.basename(wiki_lang_folder)
    print(lang)
    with open(os.path.join(out_folder, lang), "w") as writer:
        cur_output = []
        for f in os.listdir(os.path.join(wiki_folder, wiki_lang_folder)):
            with open(os.path.join(wiki_folder, wiki_lang_folder, f)) as reader:
                for line in reader:
                    output = process_info_line(lang, line)
                    if output is None:
                        continue
                    cur_output.append(str(url_id) + "\t" + output.strip())
                    url_id += 1
                    if len(cur_output) >= 1000:
                        writer.write("\n".join(cur_output))
                        writer.write("\n")
                        cur_output = []
        if len(cur_output) > 0:
            writer.write("\n".join(cur_output))
            writer.write("\n")

print("finished")
