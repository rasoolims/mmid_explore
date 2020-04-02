import os
import sys

input_folder = os.path.abspath(sys.argv[1])
file_sizes = {}
for file in os.listdir(input_folder):
    if not file.endswith(".txt"):
        continue
    file_path = os.path.join(input_folder, file)
    file_size = os.path.getsize(file_path)
    file_sizes[file_path] = file_size

file_handles = {f: open(f, "r") for f in file_sizes.keys()}
sum_sizes = sum(file_sizes.values())

random_share = []
for path in file_sizes.keys():
    share = max(1, int(file_sizes[path] / (1024 * 1024)))
    print(path, share)
    random_share += [path] * share

print(len(random_share))

for f in file_handles:
    file_handles[f].close()
