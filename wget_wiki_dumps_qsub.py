import os
import sys

langs = ["zu", "zh_yue", "zh_min_nan", "zh_classical", "zh", "zea", "za", "yo", "yi", "xmf", "xh", "xal", "wuu", "wo",
         "war", "wa", "vo", "vls", "vi", "vep", "vec", "ve", "uz", "ur", "uk", "ug", "udm", "tyv", "ty", "tw", "tum",
         "tt", "ts", "tr", "tpi", "to", "tn", "tl", "tk", "ti", "th", "tg", "tet", "te", "tcy", "ta", "szl", "sw", "sv",
         "su", "stq", "st", "ss", "srn", "sr", "sq", "so", "sn", "sm", "sl", "sk", "si", "sh", "sg", "se", "sd", "sco",
         "scn", "sc", "sat", "sah", "sa", "rw", "rue", "ru", "roa_tara", "roa_rup", "ro", "rn", "rmy", "rm", "qu", "pt",
         "ps", "pnt", "pnb", "pms", "pl", "pih", "pi", "pfl", "pdc", "pcd", "pap", "pam", "pag", "pa", "os", "or", "om",
         "olo", "oc", "ny", "nv", "nso", "nrm", "nov", "no", "nn", "nl", "new", "ne", "nds_nl", "nds", "nap", "nah",
         "na", "mzn", "myv", "my", "mwl", "mt", "ms", "mrj", "mr", "mn", "ml", "mk", "min", "mi", "mhr", "mg", "mdf",
         "map_bms", "mai", "lv", "ltg", "lt", "lrc", "lo", "ln", "lmo", "lij", "li", "lg", "lfn", "lez", "lbe", "lb",
         "lad", "la", "ky", "kw", "kv", "ku", "ksh", "ks", "krc", "koi", "ko", "kn", "km", "kl", "kk", "ki", "kg",
         "kbp", "kbd", "kab", "kaa", "ka", "jv", "jbo", "jam", "ja", "iu", "it", "is", "io", "inh", "ilo", "ik", "ig",
         "ie", "id", "ia", "hy", "hu", "ht", "hsb", "hr", "hif", "hi", "he", "haw", "hak", "ha", "gv", "gu", "gu",
         "got", "gor", "gom", "gn", "glk", "gl", "gd", "gan", "gag", "ga", "fy", "fur", "frr", "frp", "fr", "fo", "fj",
         "fiu_vro", "fi", "ff", "fa", "ext", "eu", "et", "es", "eo", "en", "eml", "el", "ee", "dz", "dv", "dty", "dsb",
         "diq", "din", "de", "da", "cy", "cv", "cu", "csb", "cs", "crh", "cr", "co", "ckb", "chy", "chr", "ch", "ceb",
         "ce", "cdo", "cbk_zam", "ca", "bxr", "bug", "bs", "br", "bpy", "bo", "bn", "bm", "bjn", "bi", "bh", "bg",
         "be_x_old", "be", "bcl", "bat_smg", "bar", "ban", "ba", "azb", "az", "ay", "av", "atj", "ast", "as", "arz",
         "arc", "ar", "ang", "an", "am", "als", "ak", "af", "ady", "ace", "ab"]
config_folder = sys.argv[1]
output_folder = os.path.abspath(sys.argv[2])

if not os.path.exists(config_folder):
    os.makedirs(config_folder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

num_process = 0
file_num = 0
folders = []
output_folders = []

for lang in langs:
    content = ["#$ -N wget_" + lang]
    content += ["#$ -o " + os.path.join(config_folder, lang + ".stdout")]
    content += ["#$ -e " + os.path.join(config_folder, lang + ".stderr")]
    content += ["#$ -M rasooli@seas.upenn.edu"]
    content += ["#$ -l h_vmem=20G"]
    content += ["#$ -l mem=20G"]
    content += ["#$ -l h_rt=3:00:00"]
    content += ["#$ -cwd"]

    url = "http://download.wikimedia.org/"+lang+"wiki/latest/"+lang+"wiki-latest-pages-articles.xml.bz2"
    command = "wget -O " + os.path.join(output_folder, lang+".xml.bz2") +" " + url
    content += [command]
    content = "\n".join(content)
    config_path = os.path.join(config_folder, lang) + ".sh"
    with open(config_path, "w") as writer:
        writer.write(content)
    command = "qsub " + config_path
    print(command)
    os.system(command)
print("done!")
