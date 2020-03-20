import html
import json
import os
import re
import sys

TAG_RE = re.compile(r'<[^>]+>')


def is_image_link(line):
    line = line.strip()
    if line.startswith("[[") and line.endswith("]]") and "|" in line and ":" in line:
        return True
    return False


def extract_image_info(line):
    if not ".png" in line.lower() and not ".jpg" in line.lower() and not ".jpeg" in line.lower():
        return None
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
    wikipedia_path = spl[0].replace(" ", "_")
    caption = spl[-1].strip()
    caption = re.sub("([\[]).*?([\]])", "", caption)  # Remove anything between brackets
    caption = re.sub("([{+]).*?([}+])", "", caption).replace("}", "").replace("{",
                                                                              "")  # Remove anything between brackets
    caption = caption.replace("[", "").replace("]", "")

    if len(caption) < 3:
        return None

    return wikipedia_path, caption


def remove_html_tags(text):
    # from https://tutorialedge.net/python/removing-html-from-string/
    return TAG_RE.sub('', text).strip()


def clean_line(line):
    content = html.unescape(line.strip())
    content = remove_html_tags(text=content)
    content = re.sub("([{+]).*?([}+])", "", content).replace("}", "").replace("{",
                                                                              "")  # Remove anything between brackets
    content = content.replace("\\", "")
    content = content.replace("\'", "'")
    line_contents = []
    for line_content in content.split("]"):
        line_content = line_content.strip()
        if "|" in line_content:
            line_content = line_content[line_content.rfind("|") + 1:]
        line_contents.append(line_content)

    line_contents = " ".join(line_contents)
    spl = line_contents.split(" ")
    output = []
    for w in spl:
        if "[" in w and ":" in w:
            continue
        if "<" in w or ">" in w:
            continue

        for special_char in {"[", "]", "=", "*"}:
            w = w.replace(special_char, "")
        if len(w) > 0:
            output.append(w)
    output = " ".join(output).strip()
    return output


def is_eligible_line(line):
    line = line.strip()
    if len(line) == 0:
        return False
    if line.startswith("* [") and line.endswith("]"):
        return False  # Remove a text that all of it is a hyperlink.
    if line.startswith("[") and line.endswith("]") and not is_image_link(line):
        return False  # Remove a text that all of it is a hyperlink.

    for bad_start in {"{", "_", "|"}:
        if line.startswith(bad_start):
            return False
    if line.startswith("[[") and line.endswith("]]") and ":" in line and "|" not in line:
        # Usually for category information
        return False
    for bad_content in {"#"}:
        if bad_content in line:
            return False
    return True


def extract_tile_and_text(xml_content):
    in_text = False
    text_content = []
    title = ""
    image_links = {}

    # first find the last title that is usually for references
    last_title_line = 0
    for c, line in enumerate(xml_content):
        if "==" in line:
            last_title_line = c

    for c, line in enumerate(xml_content):
        line = line.strip()
        if line.startswith("<title>") and line.endswith("</title>"):
            title = clean_line(line[7:-8].strip())
            if ":" in title:
                return None  # Usually (not always, these pages belong to redirect or category pages)
        else:
            if "</text>" in line:
                line = line[:line.find("</")].strip()
                if is_image_link(line):
                    image_info = extract_image_info(line)
                    if image_info is not None:
                        image_links[image_info[0]] = image_info[1]
                elif c != last_title_line and is_eligible_line(line):
                    line = clean_line(line)
                    if len(line) > 0:
                        text_content.append(line)
                if len(text_content) > 0:
                    return "\n".join([title] + text_content), image_links
                else:
                    return None
            if "<text" in line:
                line = line[line.find(">") + 1:].strip()
                in_text = True
                if is_image_link(line):
                    image_info = extract_image_info(line)
                    if image_info is not None:
                        image_links[image_info[0]] = image_info[1]
                elif c != last_title_line and is_eligible_line(line):
                    line = clean_line(line)
                    if len(line) > 0:
                        text_content.append(line)
            elif in_text:
                if is_image_link(line):
                    image_info = extract_image_info(line)
                    if image_info is not None:
                        image_links[image_info[0]] = image_info[1]
                elif c != last_title_line and is_eligible_line(line):
                    line = clean_line(line)
                    if len(line) > 0:
                        text_content.append(line)


def extract_pages(xmlfile):
    current_page_content = []
    in_page = False
    page_number = 0
    with open(xmlfile, "r") as reader:
        for line in reader:
            line = line.strip()
            if in_page and "</page>" in line:
                line = line[:line.find("</page>")].strip()
                current_page_content.append(line)
                if page_number == 58:
                    pass
                    #
                text_content = extract_tile_and_text(current_page_content)
                current_page_content = []
                in_page = False
                if text_content is not None:
                    page_number += 1
                    yield text_content
            if "<page>" in line:
                line = line[line.find("<page>") + 6:].strip()
                in_page = True
                current_page_content.append(line)
            elif in_page and len(line) > 0:
                current_page_content.append(line)


input_file = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

folder_num = 0
written_files = 0
current_folder = os.path.join(output_folder, str(folder_num))
if not os.path.exists(current_folder):
    os.makedirs(current_folder)

image_link_dict = {}
all_images = 0
for page in extract_pages(input_file):
    current_file = os.path.join(current_folder, str(written_files) + ".txt")
    with open(current_file, "w") as writer:
        writer.write(page[0])
        if len(page[1]) > 0:
            image_link_dict[str(folder_num) + "/" + str(written_files) + ".txt.gz"] = page[1]
            all_images += len(page[1])
    os.system("gzip " + current_file + " &")  # Should be faster that python gzip writer.

    written_files += 1
    if written_files % 10000 == 0:
        folder_num += 1
        current_folder = os.path.join(output_folder, str(folder_num))
        if not os.path.exists(current_folder):
            os.makedirs(current_folder)
        print("written", written_files)

print("Done with texts", input_file, written_files)

with open(os.path.join(output_folder, 'images.json'), 'w') as fp:
    json.dump(image_link_dict, fp)

print("Done with images", len(image_link_dict), all_images)
