import os
import sys
from collections import defaultdict

html_url_file = os.path.abspath(sys.argv[1])
image_url_file = os.path.abspath(sys.argv[2])
image_folder = os.path.abspath(sys.argv[3])

image_url_info_dict = defaultdict()

url_set = set()
url_counts = 0
with open(image_url_file, "r") as reader:
    for line in reader:
        spl = line.strip().split("\t")
        if len(spl) < 2: continue
        url_counts += 1
        url_set.add(spl[1])
print(f, url_counts)