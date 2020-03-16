import os
import sys

input_folder = os.path.abspath(sys.argv[1])
for c, f in os.listdir(input_folder):
    if f.endswith("gz"):
        continue
    command = "gzip " + os.path.join(input_folder, f)

    if c % 100 != 0:
        command += " &"

    if c % 10000==0:
        print(c, f)

print("done")