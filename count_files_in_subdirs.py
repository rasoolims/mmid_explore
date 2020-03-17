import os
import sys

count = 0
for folder in os.listdir(os.path.abspath(sys.argv[1])):
    path = os.path.join(os.path.abspath(sys.argv[1]), folder)
    if not os.path.isdir(path):
        continue
    count += len(os.listdir(path))
print(count)
