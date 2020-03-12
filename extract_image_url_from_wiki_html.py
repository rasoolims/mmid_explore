import os, sys

def retrieve_url(file_path):
    with open(file_path, "r") as reader:
        content = reader.read()



input_folder = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

contents = []
with open(output_file, "w") as writer:
    for f in os.listdir(input_folder):
        url = retrieve_url(os.path.join(input_folder, f))
        if url is not None:
            contents.append(f+"\t"+url)
            if len(contents)%1000==0:
                writer.write("\n".join(contents))
                writer.write("\n")
                contents = []
    if len(contents)>0:
        writer.write("\n".join(contents))
        writer.write("\n")
print("done with", input_folder)