import os
import sys

pages = 0
with open(os.path.abspath(sys.argv[1]), "r") as reader:
    for line in reader:
        if "<page>" in line:
            pages += 1
            if pages % 10000 == 0:
                print(pages)

print(pages)
