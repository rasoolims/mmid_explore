import os
import sys


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
                text_content = "\n".join(current_page_content)
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

all_images = 0
for page in extract_pages(input_file):
    current_file = os.path.join(current_folder, str(written_files) + ".txt")
    with open(current_file, "w") as writer:
        writer.write(page)
    os.system("gzip -f " + current_file + " &")  # Should be faster that python gzip writer.

    written_files += 1
    if written_files % 10000 == 0:
        folder_num += 1
        current_folder = os.path.join(output_folder, str(folder_num))
        if not os.path.exists(current_folder):
            os.makedirs(current_folder)
        print("written", written_files)

print("Done with texts", input_file, written_files)
