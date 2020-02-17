import os, sys
import pickle
import torch
from transformers import *
from collections import defaultdict
tokenizer_class, weights, model_class= XLMRobertaTokenizer, 'xlm-roberta-base', XLMRobertaModel
tokenizer = tokenizer_class.from_pretrained(weights)
model = model_class.from_pretrained(weights)

print("Reading Tensors")
vector_dict = {}
batch = defaultdict(list)
batch_ids = defaultdict(list)

for line in open(os.path.abspath(sys.argv[1]), 'r', encoding="utf-8"):
	columns = line.strip().split("\t")
	entries = columns[1:]
	tokens = ["CLS"]
	for entry in entries:
		tokens += tokenizer.tokenize(entry) + ["[SEP]"]
	if len(tokens)>512:
		print("trimming the tokens", len(tokens))
		tokens = tokens[:512]
	tok_ids = tokenizer.convert_tokens_to_ids(tokens)
	tok_tensors = torch.tensor([tok_ids])
	batch[tok_tensors.size()[-1]].append(tok_tensors)
	batch[tok_tensors.size()[-1]].append(int(columns[0]))

	# with torch.no_grad():
	# 	class_hidden_state = model(tok_tensors)[0]
	# 	vector_dict[int(columns[0])] = class_hidden_state[0, 0]

	# if len(vector_dict)%100==0:
	# 	sys.stdout.write(str(len(vector_dict))+"...")

sys.stdout.write(str(len(vector_dict))+"\n")

for length in batch.keys():
	print("hi")
	import pdb
	pdb.set_trace()


sorted_tensors = sorted(vector_dict.values(), key = lambda kv:(kv[1], kv[0]))

"Writing the tensors!"
with open(os.path.abspath(sys.argv[2]), "wb") as fout:
	pickle.dump(sorted_tensors, fout, protocol=pickle.HIGHEST_PROTOCOL)
