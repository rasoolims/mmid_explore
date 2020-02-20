import glob, os,sys

english_prefix = os.path.abspath(sys.argv[1])

for file in glob.glob(english_prefix + "*"):
    print(file)