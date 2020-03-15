import os,sys

input_folder = os.path.abspath(sys.argv[1])

url_set = set()
for f in os.listdir(input_folder):
    print(f)
    with open(os.path.join(input_folder,f), "r") as reader:
        for line in reader:
            spl = line.strip().split("\t")
            if len(spl)<2: continue

            url_set.add(spl[1])


with open(os.path.abspath(sys.argv[2]), "w") as writer:
    for i, url in enumerate(url_set):
        writer.write(str(i)+"\t"+url+"\n")
print("done!")