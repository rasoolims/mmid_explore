import os
import sys

"""
Removes those captions that we guess they are irrelevant
"""

caption_file = os.path.abspath(sys.argv[1])
caption_output_file = os.path.abspath(sys.argv[2])
saved, skipped = 0, 0
with open(caption_file, "r") as r, open(caption_output_file, "w") as w:
    for line in r:
        path, lang, caption = line.strip().split("\t")
        if "=" in caption or caption == "thumb" or caption == "left" or caption == "right" or caption == "thumbnail":
            skipped += 1
            continue
        w.write(line.strip() + "\n")
        saved += 1

print("Saved", saved, "-- Skipped", skipped)
