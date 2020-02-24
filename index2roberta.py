import os, sys
import pickle
import torch
import numpy as np
from transformers import *
from collections import defaultdict
tokenizer_class, weights, model_class= XLMRobertaTokenizer, 'xlm-roberta-base', XLMRobertaModel
tokenizer = tokenizer_class.from_pretrained(weights)
model = model_class.from_pretrained(weights)

print("Reading Tensors")
vector_dict = {}
batch = defaultdict(list)
batch_ids = defaultdict(list)

for i, line in enumerate(open(os.path.abspath(sys.argv[1]), 'r', encoding="utf-8")):
	entries = line.strip().split("\t")
	tokens = ["CLS"]
	for entry in entries:
		tokens += tokenizer.tokenize(entry) + ["[SEP]"]
	if len(tokens)>512:
		print("trimming the tokens", len(tokens))
		tokens = tokens[:512]
	tok_ids = tokenizer.convert_tokens_to_ids(tokens)
	tok_tensors = torch.tensor([tok_ids])
	batch[tok_tensors.size()[-1]].append(tok_tensors)
	batch_ids[tok_tensors.size()[-1]].append(i)

for length in sorted(batch.keys()):
	print("length", length, len(batch[length]))
	cat_tensor = torch.cat(batch[length])
	max_batch_size, cat_len = 100, cat_tensor.size()[0]
	output_tensors = []
	for i in range(0, cat_len, max_batch_size):
		with torch.no_grad():
			current_batch = cat_tensor[i: min(i+max_batch_size, cat_len)]
			output_tensor = model(current_batch)[0]
			output_tensor = output_tensor[:, 0, :].cpu()
			output_tensors.append(output_tensor)

	complete_tensors = torch.cat(output_tensors)
	for i in range(len(batch_ids[length])):
		vector_dict[batch_ids[length][i]] = complete_tensors[i,:].numpy()

sorted_tensors = sorted(vector_dict.values(), key = lambda kv:(kv[1], kv[0]))

"Writing the tensors!"
with open(os.path.abspath(sys.argv[2]), "wb") as fout:
	pickle.dump(sorted_tensors, fout, protocol=pickle.HIGHEST_PROTOCOL)
