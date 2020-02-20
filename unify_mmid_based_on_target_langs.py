import glob, os,sys

english_prefix = os.path.abspath(sys.argv[1])

for folder in glob.glob(english_prefix + "*"):
    print(folder)
    for subdir in os.listdir(folder):
        word = open(os.path.join(folder, subdir, "word.txt"),'r').read().strip()
        print(subdir, word)

