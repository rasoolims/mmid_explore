import os
import random
import sys


def remove_from_list(cur_list, item_to_remove):
    new_list = []
    for i in cur_list:
        if i != item_to_remove:
            new_list.append(i)
    return new_list


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
    random_share += [path] * share

output_file = os.path.abspath(sys.argv[2])

with open(output_file, "w") as writer:
    line_num = 0
    while len(random_share) > 0:
        lang_index = random.randint(0, len(random_share))
        path = random_share[lang_index]

        line_read = file_handles[path].readline().strip()

        if len(line_read) == 0:
            # Used up all sentences for that file!
            file_handles[path].close()
            random_share = remove_from_list(random_share, path)
            print("Done with", path)
        else:
            writer.write(line_read + "\n")
            line_num += 1
            if line_num % 1000 == 0:
                print("processed", line_num)
print("Done!")
