import json
import os
import sys

"""
Removes those captions that we guess they are irrelevant
"""

caption_file = os.path.abspath(sys.argv[1])
caption_output_file = os.path.abspath(sys.argv[2])
saved, skipped = 0, 0
with open(caption_file, "rb") as r:
    doc_dicts = json.load(r)
    for d_num, doc in enumerate(doc_dicts):
        new_list = []
        for image in doc["images"]:
            caption = image["caption"]
            if "=" in caption or caption == "thumb" or caption == "left" or caption == "right" or caption == "thumbnail":
                skipped += 1
                continue
            else:
                new_list.append(image)
                saved += 1
        doc["images"] = new_list

    with open(caption_output_file, "wb") as w:
        json.dump(doc_dicts, w)

print("Saved", saved, "-- Skipped", skipped)
