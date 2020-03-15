# coding: utf8

import os
import sys


def retrieve_url(file_path):
    with open(file_path, "r") as reader:
        content = reader.read()
        q1 = "fullImageLink"
        if q1 not in content:
            return None
        content = content[content.find(q1) + len(q1):]

        q2 = "<a href=\""
        if q2 not in content:
            return None
        content = content[content.find(q2) + len(q2):]

        q3 = "\"><"
        if q3 not in content:
            return None
        content = content[:content.find(q3)]

        if content.startswith("//"):
            content = "https:" + content

        return content


input_folder = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])
r = int(sys.argv[3])

contents = []
with open(output_file, "w") as writer:
    for c, f in enumerate(os.listdir(input_folder)):
        if f.startswith("."):
            continue  # ignore os-specific files
        rm = int(f) % 20
        if r != rm:
            continue
        url = retrieve_url(os.path.join(input_folder, f))
        if url is not None:
            contents.append(f + "\t" + url)
            if len(contents) % 1000 == 0:
                writer.write("\n".join(contents))
                writer.write("\n")
                contents = []
                print(input_folder, c + 1)
    if len(contents) > 0:
        writer.write("\n".join(contents))
        writer.write("\n")
print("done with", input_folder)
