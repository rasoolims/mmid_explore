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
file_sizes = sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)
print(file_sizes)
