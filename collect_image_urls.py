import os,sys

input_folder = os.path.abspath(sys.argv[1])

already_used = {}
longest_id = 0

if len(sys.argv)>3:
    with open(os.path.abspath(sys.argv[3]), "r") as reader:
        for line in reader:
            spl = line.strip().split("\t")
            n, url = int(spl[0]), spl[1]
            longest_id = max(n, longest_id)
            already_used[url] = n
    print("already used urls", len(already_used))

url_set = set()
url_counts = 0
for f in os.listdir(input_folder):
    with open(os.path.join(input_folder,f), "r") as reader:
        for line in reader:
            spl = line.strip().split("\t")
            if len(spl)<2: continue
            url_counts += 1
            if spl[1] not in already_used:
                url_set.add(spl[1])
    print(f, url_counts)


with open(os.path.abspath(sys.argv[2]), "w") as writer:
    for i, url in enumerate(url_set):
        writer.write(str(i+longest_id)+"\t"+url+"\n")
print("done!", len(url_set))