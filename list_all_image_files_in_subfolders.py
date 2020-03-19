import os,sys

input_folder = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

with open(output_file, "w") as writer:
    for folder in os.listdir(input_folder):
        print(folder)
        folder_path = os.path.join(input_folder, folder)
        for file in os.listdir(folder_path):
            fl = file.lower()
            if fl.endswith("jpg") or fl.endswith("png"):
                file_num = fl[:-4]
            elif fl.endswith("jpeg"):
                file_num = fl[:-5]
            else:
                continue
            writer.write(file_num+"\t"+folder+"/"+file+"\n")
print("done!")
