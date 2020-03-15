import math
import os
import sys

f = os.path.abspath(sys.argv[1])
contents = open(f, "r").read().strip().split("\n")

clen = len(contents)
split_len = math.ceil(clen / int(sys.argv[2]))

print(clen, split_len)
for i in range(int(sys.argv[2])):
    start = i * split_len
    end = min((i + 1) * split_len, clen)
    print(start, end)
    content_part = "\n".join(contents[start:end])
    f_name = f + "." + str(i)
    with open(f_name, "w") as writer:
        writer.write(content_part)
        writer.write("\n")
