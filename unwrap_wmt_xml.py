import glob
import os
import sys

input_folder = os.path.abspath(sys.argv[1])

for file in glob.glob(input_folder + "/*.sgm"):
    file_path = os.path.join(input_folder, file)
    output_path = file_path[:-4] + ".txt"

    print(file_path)
    with open(file_path, "r") as r:
        lines = r.read().strip().split("\n")
        sentences = []
        for line in lines:
            if line.startswith("<seg id"):
                sentences.append(line[line.find(">") + 1: line.rfind("</")].strip())
        print(len(sentences))

    with open(output_path, "w") as w:
        w.write("\n".join(sentences))
