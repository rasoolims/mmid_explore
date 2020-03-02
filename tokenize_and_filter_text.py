import os
import sys
import gzip
import Cutter

tokenized_label_dict = {}
tokenized_input_dict = {}

def tokenize_label(tokenizer, input):
    if input in tokenized_label_dict:
        return tokenized_label_dict[input]
    cur_output = []
    for x in tokenizer.cut(input):
        if len(x[0].strip())>0:
            cur_output.append(x[0].strip())
    tokenized_label_dict[input] = " ".join(cur_output)
    return tokenized_label_dict[input]

def tokenize_sentence(tokenizer, input):
    if input in tokenized_input_dict:
        return tokenized_input_dict[input]

    outputs = []
    cur_output = []
    for x in tokenizer.cut(input):
        if len(x[0].strip())>0:
            cur_output.append(x[0].strip())
        else:
            outputs.append(" ".join(cur_output))
            cur_output = []
    if len(cur_output)>0:
        outputs.append(" ".join(cur_output))
    tokenized_input_dict[input] = outputs
    return outputs


target_lang = sys.argv[2]

try:
    tokenizer = Cutter.Cutter(profile=target_lang)
except:
    tokenizer = Cutter.Cutter(profile="en")

sen_count, write_count, write_sen_count, all_sent_count = 0, 0, 0, 0
outputs = []
with gzip.open(os.path.abspath(sys.argv[3]), "wt") as writer:
    for line in gzip.open(os.path.abspath(sys.argv[1]), "rt"):
        sen_count+=1
        spl = line.strip().split("\t")
        label = tokenize_label(tokenizer, spl[0])
        image_path = spl[1]
        passages = spl[2:]
        output_sentences = []
        for passage in passages:
            tokenized_sentences = tokenize_sentence(tokenizer, passage)
            for sentence in tokenized_sentences:
                if label.lower() in sentence.lower():
                    output_sentences.append(sentence)
            all_sent_count += len(tokenized_sentences)
        if len(output_sentences)>0:
            outputs.append(label+"\t"+image_path+"\t"+"\t".join(output_sentences))
            write_count+=1
            write_sen_count+=len(output_sentences)
        if sen_count%100==0:
            print(str(sen_count)+"("+str(write_count)+","+str(write_sen_count)+"->",str(all_sent_count)+")")
            writer.write("\n".join(outputs))
            outputs = []
            writer.write("\n")

if len(outputs)>0:
    writer.write("\n".join(outputs))
    writer.write("\n")

print(str(sen_count)+"("+str(write_count)+","+str(write_sen_count)+"->",str(all_sent_count)+")")
print("finished")
