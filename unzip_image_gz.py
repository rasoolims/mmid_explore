import os
import sys

dir_path = os.path.abspath(sys.argv[1])

files = os.listdir(dir_path)
for f in files:
    if f.endswith(".gz"):
        cur_file = os.path.join(dir_path, f)
        orig_file = os.path.join(dir_path, f[:-3])
        if os.path.exists(orig_file):
            command = "rm " + cur_file
        else:
            command = "gunzip " + cur_file
        print(command)
        os.system(command)
