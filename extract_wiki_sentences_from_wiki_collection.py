"""
Assuming that a data is already preprocessed and each sentence is split by </s>.
We also assume that every line starts with language identifier token.
"""
import os
import sys

input = os.path.abspath(sys.argv[1])
output = os.path.abspath(sys.argv[2])
sen_set = set()

with open(input, "r") as reader, open(output, "w") as writer:
    for i, line in enumerate(reader):
        sentences = line.strip().split("</s>")
        first_sen = sentences[0].split(" ")
        lang = first_sen[0]
        sentences[0] = " ".join(first_sen[1:])

        for sen in sentences:
            if len(sen.strip()) > 0:
                # To skip repetitive sentences.
                sen_set.add(lang + " " + sen.strip() + " </s>")
        if (i + 1) % 1000000 == 0:
            print(i + 1)

    print("Writing sentences", len(sen_set))
    writer.write("\n".join(sen_set))
