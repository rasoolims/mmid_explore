import os, sys, re
from collections import defaultdict

indices_folder = os.path.abspath(sys.argv[1])
bilingual_dict_folder = os.path.abspath(sys.argv[2])
language_abbreviation_file = os.path.abspath(sys.argv[3])

en2foreign_dict = {}
foreign2en_dict = {}

# Step 1: Reading language abbreviations
language_abbreviations ={x.split("\t")[1]:x.split("\t")[0] for x in open(language_abbreviation_file, "r").read().strip().split("\n")}


# Step 2: Constructing the English to foreign dictionaries

# The following dictionary is used to create an initial dictonary of equivalents that can be used to find all equivalents.
all_linked_dict = defaultdict(set)

for file in os.listdir(bilingual_dict_folder):
    if not file.startswith("dict."):
        continue
    file_content = open(os.path.join(bilingual_dict_folder, file), "r", encoding="utf-8").read().strip().split("\n")
    language = language_abbreviations[file[file.rfind(".")+1:]]

    foreign2en_dict[language] = defaultdict(list)

    entries = {}
    for cline in file_content:
        line = cline.replace("\fowl", "fowl").replace("\\fowl", "fowl").replace("category: \\tutbol", "category: futbol")
        line = line.replace("xii \\twelfth", "xii twelfth")# specific treatment!
        spl = line.strip().replace("\\f","").replace("\f","").split("\t")

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

            if len(english_phrases)>1:
                for e2 in english_phrases:
                    all_linked_dict[english].add(e2)

print("size of english dictionary", len(en2foreign_dict))
print("all_linked_dict", len(all_linked_dict))

# Creating a fully linked graph of all equivalents
complete_eq_set = defaultdict(set)
for c1 in list(all_linked_dict.keys()):
    for c2 in all_linked_dict[c1]:
        complete_eq_set[c1].add(c2)
        for c3 in all_linked_dict[c2]:
            complete_eq_set[c1].add(c3)
print(len(complete_eq_set))

# Creating a list that should fall back to the original items
fallback_set = {}
for c1 in sorted(complete_eq_set.keys()):
    if c1 in fallback_set:
        continue
    for c2 in complete_eq_set[c1]:
        if c1==c2: continue
        fallback_set[c2] = c1
print("fall_back", len(fallback_set))

en_number_conversion = {}
number_counter = 0
for word in sorted(en2foreign_dict.keys()):  # Should be sorted for consistency with the previous step
    if word in fallback_set:
        if fallback_set[word] not in en_number_conversion:
            en_number_conversion[fallback_set[word]] = number_counter
            number_counter += 1
        en_number_conversion[word] = en_number_conversion[fallback_set[word]]
    elif word not in en_number_conversion:
        en_number_conversion[word] = number_counter
        number_counter+=1

print("en_number_conversion", number_counter, len(en_number_conversion))

file_number_conversion = defaultdict(int)

all_phrases = list()
all_phrases_set = set()
for file in os.listdir(indices_folder):
    if not file.endswith(".tsv"):
        continue
    if not "english" in file:
        continue
    file_content = open(os.path.join(indices_folder, file), "r", encoding="utf-8").read().strip().split("\n")
    entries = {}
    for cline in file_content:
        line=cline.replace("\fowl", "fowl").replace("xii \twelfth", "xii twelfth").replace("\\fowl", "fowl").replace("category: \tutbol", "category: futbol").replace("\f","").replace("\\t", "\t").replace(" \t", "\t")
        try:
            phrases, number = line.strip().split("\t")
        except:
            spl = line.strip().split("\t")
            phrases = " ".join(spl[:-1])
            number = spl[-1]

        # phrases = re.sub("\s\s+", " ", phrases)
        number = int(number.strip())
        phrase_candidates = [x.strip() for x in re.sub("\s\s+", " ", phrases).replace(";", ",").split(",")]
        entries[number] = phrase_candidates
        language_id = file[file.find("index-")+6:file.find("-package.")]
        file_number_conversion[language_id + "\t" + str(number)] = en_number_conversion[phrases]
        all_phrases.append(phrases)


print("en2foreign_dict", len(en2foreign_dict))
print("all_phrases", len(all_phrases))
# assert len(all_phrases) == len(en2foreign_dict)


foreign_number_conversion = {}

# Now converting all files
for file in os.listdir(indices_folder):
    if not file.endswith(".tsv"):
        continue
    if "english" in file:
        continue
    language = file[file.find("-")+1:file.rfind("-")]
    if language == "turkish-august":
        language = "turkish"
    # print(language)
    foreign_number_conversion[language] = {}
    file_content = open(os.path.join(indices_folder, file), "r", encoding="utf-8").read().strip().split("\n")
    entries = {}
    for line in file_content:
        line=line.replace("\\t", "\t")
        try:
            phrases, number = line.strip().split("\t")
        except:
            spl = line.strip().split("\t")
            phrases = "\t".join(spl[:-1])
            number = spl[-1]

        # phrases = re.sub("\s\s+", " ", phrases)
        number = int(number.strip())
        equivalents = foreign2en_dict[language][phrases]
        language_id = file[file.find("index-")+6:file.find("-package.")]
        try:
            file_number_conversion[language_id + "\t" + str(number)] = en_number_conversion[equivalents[0]]
        except:
            try:
                # no translation, finding the actual word in the English dictionary
                file_number_conversion[language_id + "\t" + str(number)] = en_number_conversion[phrases]
            except:
                print(">", language, number, phrases)
                # This usually happens for nonsense information. Thus we igonre it.
                file_number_conversion[language_id + "\t" + str(number)] = number_counter +1


print("file_number_conversion", len(file_number_conversion))

with open(os.path.abspath(sys.argv[4]), 'w') as writer:
    content = [f+"\t"+str(v) for f,v in file_number_conversion.items()]
    writer.write("\n".join(content))

print("finished with", number_counter+2, "classes")