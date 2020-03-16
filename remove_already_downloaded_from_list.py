import datetime
import errno
import os
import signal
import sys
import time
import urllib.parse as urlparse
import urllib.request
from functools import wraps



input_file = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

file_number = 0
url_count = 0
start_time = time.time()
file_path = os.path.join(output_folder, "index.txt")
already_downloaded = 0
with open(input_file) as reader:
    for line in reader:
        spl = line.strip().split("\t")
        n, url = spl[0].strip(), spl[1].strip()
        extension = url[url.rfind("."):]
        file_name = n + extension

        specific_folder_path = os.path.join(output_folder, str(int(n) % 1000))
        if not os.path.exists(specific_folder_path):
            os.makedirs(specific_folder_path)
        img_file_path = os.path.join(specific_folder_path, file_name)
        if os.path.exists(img_file_path):
            already_downloaded += 1
            continue