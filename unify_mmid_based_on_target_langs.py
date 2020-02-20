import glob, os,sys
from collections import defaultdict


english_prefix = os.path.abspath(sys.argv[1])
bilingual_dict_folder = os.path.abspath(sys.argv[2])
language_abbreviation_file = os.path.abspath(sys.argv[3])
# Step 1: Reading language abbreviations
language_abbreviations = {x.split("\t")[1]: x.split("\t")[0] for x in
                          open(language_abbreviation_file, "r").read().strip().split("\n")}
target_languages = {"fa", "ar", "es", "id", "zh"}

output_en_folder = os.path.abspath(sys.argv[4])
if not os.path.exists(output_en_folder):
    os.makedirs(output_en_folder)

en2foreign_dict = {}
foreign2en_dict = {}
allowed_english_entries = set()

for file in os.listdir(bilingual_dict_folder):
    if not file.startswith("dict."):
        continue
    file_content = open(os.path.join(bilingual_dict_folder, file), "r", encoding="utf-8").read().strip().split("\n")
    lang_id = file[file.rfind(".") + 1:]
    if lang_id not in target_languages:
        continue

    language = language_abbreviations[lang_id]

    foreign2en_dict[language] = defaultdict(list)

    entries = {}
    for cline in file_content:
        line = cline.replace("\fowl", "fowl").replace("\\fowl", "fowl").replace("category: \\tutbol",
                                                                                "category: futbol")
        line = line.replace("xii \\twelfth", "xii twelfth")  # specific treatment!
        spl = line.strip().replace("\\f", "").replace("\f", "").split("\t")

        foreign = spl[0]
        english_phrases = spl[1:]

        for english in english_phrases:
            english = english.strip()
            if english.endswith("\\"):
                english = english[:-1]
            if english not in en2foreign_dict:
                en2foreign_dict[english] = {}
            if foreign not in en2foreign_dict[english]:
                en2foreign_dict[english][foreign] = set()
            en2foreign_dict[english][foreign].add(foreign)
            foreign2en_dict[language][foreign].append(english)
            allowed_english_entries.add(english)

print("number of allowed english labels", len(allowed_english_entries))

to_fetch_folders = set()
for folder in glob.glob(english_prefix + "*"):
    print(folder)
    index_path = os.path.join(folder, "index.tsv")
    path_dict = {}
    for line in open(index_path, 'r'):
        spl = line.strip().replace("\\t","\t").split("\t")
        path_dict[spl[0]] = spl[1]

    for word in path_dict.keys():
        if word in allowed_english_entries:
            to_fetch_folders.add(os.path.join(folder, path_dict[word]))
            copy_command = "cp -r " + os.path.join(folder, path_dict[word]) + " " + os.path.join(output_en_folder, str(len(to_fetch_folders)))
            print(copy_command)

print("number of fetched english folders", len(to_fetch_folders))

