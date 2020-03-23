import os
import sys
import gzip

input_folder = os.path.abspath(sys.argv[1])

puncs = set()
for folder in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder)
    if not os.path.isdir(folder_path): continue

    for f in os.listdir(folder_path):
        if not f.endswith(".gz"): continue
        with gzip.open(os.path.join(folder_path, f), "rt") as reader:
            content = reader.read().strip().split("\n")
            for line in content:
                words = line.strip().split(' ')
                if len(words)>8:
                    if words[-1][-1] not in puncs:
                        print(line)
                        puncs.add(words[-1][-1])


output_file = os.path.abspath(sys.argv[2])
with open(output_file, "w") as writer:
    writer.write("\n".join(list(puncs)))
    writer.write("\n")
