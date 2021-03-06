import gzip
import math
import os
import subprocess
import sys

path_dir_name = os.path.dirname(os.path.realpath(__file__))

"""
First, split a file to 40 files, then run the tokenizer on each in parallel.
Finally, merge them.
"""

all_lines = []
for line in gzip.open(os.path.abspath(sys.argv[1]), "rt"):
    all_lines.append(line.strip())

split_len = math.ceil(len(all_lines) / 40)

target_lang = sys.argv[2]
output_path = os.path.abspath(sys.argv[3])

popopens = []
for i in range(40):
    start, end = i * split_len, min(len(all_lines), (i + 1) * split_len)
    content = "\n".join(all_lines[start:end])
    with open(output_path + "." + str(i + 1) + ".input.txt", "wt") as writer:
        writer.write(content)

    command = ["python3", path_dir_name + "/tokenize_and_filter_text.py", output_path + "." + str(i + 1) + ".input.txt",
               target_lang, output_path + "." + str(i + 1) + ".output.txt"]
    popopen = subprocess.Popen(command)
    popopens.append(popopen)
    print("ran", output_path + "." + str(i + 1) + ".input.txt")

for popopen in popopens:
    popopen.wait()

print("Concatenating")
os.system("cat " + output_path + ".*.output.txt > " + output_path)
os.system("rm " + output_path + ".*.output.txt")
os.system("rm " + output_path + ".*.input.txt")
print("finished")
