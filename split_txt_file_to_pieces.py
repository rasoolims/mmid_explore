import os, sys
import math

f = os.path.abspath(sys.argv[1])
contents = open(f, "r").read().strip().split("\n")

clen = len(contents)
split_len = math.ceil(clen/10)

print(clen, split_len)
for i in range(10):
    start = i*split_len
    end = min((i+1)*split_len, clen)
    print(start, end)
    content_part = "\n".join(contents[start:end])
    f_name = f+"."+str(i)
    with open(f_name, "w") as writer:
        writer.write(content_part)
        writer.write("\n")