import os
import sys

wiki_folder = os.path.abspath(sys.argv[1])
out_folder = os.path.abspath(sys.argv[2])

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

for c, wiki_dump_file in enumerate(os.listdir(wiki_folder)):
    if not wiki_dump_file.endswith(".xml"):
        continue
    lang = wiki_dump_file[:wiki_dump_file.find("wiki")]
    if lang == "en":
        continue  # because it is very slow, will do it manually!

    lang_out_folder = os.path.join(out_folder, lang)
    print(lang_out_folder)
    if not os.path.exists(lang_out_folder):
        os.makedirs(lang_out_folder)

    os.system('grep  --ignore-case  ".png" ' + os.path.join(wiki_folder, wiki_dump_file) + ' > ' + os.path.join(
        lang_out_folder, lang + ".png.txt &"))
    os.system('grep  --ignore-case  ".svg" ' + os.path.join(wiki_folder, wiki_dump_file) + ' > ' + os.path.join(
        lang_out_folder, lang + ".svg.txt &"))
    os.system('grep  --ignore-case  ".jpeg" ' + os.path.join(wiki_folder, wiki_dump_file) + ' > ' + os.path.join(
        lang_out_folder, lang + ".jpeg.txt &"))
    if c % 10 == 0:
        os.system('grep  --ignore-case  ".jpg" ' + os.path.join(wiki_folder, wiki_dump_file) + ' > ' + os.path.join(
            lang_out_folder, lang + ".jpg.txt"))
    else:
        os.system('grep  --ignore-case  ".jpg" ' + os.path.join(wiki_folder, wiki_dump_file) + ' > ' + os.path.join(
            lang_out_folder, lang + ".jpg.txt &"))

print("done!")
