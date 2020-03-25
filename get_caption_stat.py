import json
import os
import sys
from collections import defaultdict

lang_dict = defaultdict(int)
with open(os.path.abspath(sys.argv[1]), "r") as reader:
    caption_dict = json.load(reader)
    print("number of images", len(caption_dict))

    max_caption, all_captions = 0, 0
    avg_lang, max_lang = 0, 0
    for k in caption_dict.keys():
        l = len(caption_dict[k])
        lens = []
        for v in caption_dict[k]:
            lang_dict[v] += len(caption_dict[k][v])
            lens.append(len(caption_dict[k][v]))
        slens = sum(lens)
        all_captions += slens
        max_caption = max(max_caption, slens)
        max_lang = max(max_lang, l)
        avg_lang += l
    print("number of captions", all_captions)
    print("average num of captions per image", all_captions / len(caption_dict))
    print("max num of captions per image", max_caption)
    print("average num of languages per image", avg_lang / len(caption_dict))
    print("max num of languages per image", max_lang)

    for l, v in sorted(lang_dict.items(), key=lambda kv: kv[1], reverse=True):
        print(l, v)
