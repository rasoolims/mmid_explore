import os,sys

input_folder = os.path.abspath(sys.argv[1])
with open(os.path.abspath(sys.argv[2]), "w") as writer:
    for f in os.listdir(input_folder):
        print(f)
        with open(os.path.join(input_folder, f), "r") as reader:
            content = reader.read().strip()
            writer.write(content)
            writer.write("\n")
