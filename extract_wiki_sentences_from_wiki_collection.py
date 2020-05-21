"""
Assuming that a data is already preprocessed and each sentence is split by </s>.
We also assume that every line starts with language identifier token.
"""
import os
import random
import sys
from collections import defaultdict

input = os.path.abspath(sys.argv[1])
output = os.path.abspath(sys.argv[2])
min_num = None
if len(sys.argv) > 3:
    min_num = int(sys.argv[3])
sen_set = defaultdict(set)

with open(input, "r") as reader, open(output, "w") as writer:
    for i, line in enumerate(reader):
        sentences = line.strip().split("</s>")
        first_sen = sentences[0].split(" ")
        lang = first_sen[0]
        sentences[0] = " ".join(first_sen[1:])

        for sen in sentences:
            if len(sen.strip()) > 0:
                # To skip repetitive sentences.
                sen_set[lang].add(lang + " " + sen.strip() + " </s>")
        if (i + 1) % 1000000 == 0:
            lens = " ".join([lang + ":" + str(len(sens)) for lang, sens in sen_set.items()])
            print(i + 1, lens, "\r", end="")

    print("\nSampling and writing sentences... ")
    if min_num is None:
        min_num = min([len(sen_set[lang]) for lang in sen_set.keys()])

    data = []
    for lang in sen_set.keys():
        if len(sen_set[lang]) <= min_num:
            data += list(sen_set[lang])
        else:
            sentences = list(sen_set[lang])
            random.shuffle(sentences)
            data += sentences[:min_num]

    random.shuffle(data)
    print("Sample size", len(data))
    writer.write("\n".join(data))
