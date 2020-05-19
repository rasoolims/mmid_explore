"""
Assuming that a data is already preprocessed and each sentence is split by </s>.
We also assume that every line starts with language identifier token.
"""
import os
import sys

input = os.path.abspath(sys.argv[1])
output = os.path.abspath(sys.argv[2])

with open(input, "r") as reader, open(output, "w") as writer:
    for i, line in enumerate(reader):
        sentences = line.strip().split("</s>")
        first_sen = sentences[0].split(" ")
        lang = first_sen[0]
        sentences[0] = " ".join(first_sen[1:])

        sentences = [lang + " " + sen.strip() + " </s>" for sen in sentences if len(sen.strip()) > 0]
        writer.write("\n".join(sentences))
        writer.write("\n")

        if (i + 1) % 100000 == 0:
            print(i + 1)
