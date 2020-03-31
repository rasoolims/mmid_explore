import os
import sys

input_folder = os.path.abspath(sys.argv[1])

all_types = set()
all_toks = 0


def get_stat(file):
    global all_toks
    doc_count, sen_count, tok_count = 0, 0, 0
    types = set()
    with open(file, "r") as reader:
        for line in reader:
            line = line.strip()
            if len(line) == 0: continue

            doc_count += 1
            sens = line.split("</s>")
            sen_count += len(sens)

            for sen in sens:
                toks = sen.strip().split(" ")
                tok_count += len(toks)
                for tok in toks:
                    types.add(tok)
                    all_types.add(tok)
    all_toks += tok_count
    return doc_count, sen_count, tok_count, len(types)


for file in os.listdir(input_folder):
    if not file.endswith(".txt"):
        continue
    file_path = os.path.join(input_folder, file)
    print(file, get_stat(file_path))

print("number of types/tokens in all langs", len(all_types), all_toks)
