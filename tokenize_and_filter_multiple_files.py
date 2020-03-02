import gzip, os, sys, math
import subprocess

path_dir_name = os.path.dirname(os.path.realpath(__file__))

"""
First, split a file to 40 files, then run the tokenizer on each in parallel.
Finally, merge them.
"""

all_lines = []
for line in gzip.open(os.path.abspath(sys.argv[1]), "rt"):
    all_lines.append(line.strip())

split_len = math.ceil(len(all_lines)/40)

output_path = os.path.abspath(sys.argv[2])

popopens = []
for i in range(40):
    start, end = i*split_len, min(len(all_lines), (i+1)*split_len)
    content = "\n".join(all_lines[start:end])
    with open(output_path+"."+str(i+1)+".input.gz","w") as writer:
        writer.write(content)

    command = ["python3", path_dir_name + "/tokenize_and_filter_text.py", output_path+"."+str(i+1)+".input.gz",
               output_path+"."+str(i+1)+".output.gz"]
    popopen = subprocess.Popen(command)
    popopens.append(popopen)
    print("ran", output_path+"."+str(i+1)+".input.gz")

for popopen in popopens:
    popopen.wait()

print("Concatenating")
os.system("cat "+ output_path+".*.output.gz > "+output_path)
os.system("rm "+ output_path+".*.output.gz")
os.system("rm "+ output_path+".*.input.gz")
print("finished")