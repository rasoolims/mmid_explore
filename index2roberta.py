import os, sys
import pickle
import torch
from transformers import *
tokenizer_class, weights, model_class= XLMRobertaTokenizer, 'xlm-roberta-base', XLMRobertaModel
tokenizer = tokenizer_class.from_pretrained(weights)
model = model_class.from_pretrained(weights)

print("Reading Tensors")
vector_dict = {}
for line in open(os.path.abspath(sys.argv[1]), 'r', encoding="utf-8"):
	columns = line.strip().split("\t")
	entries = columns[1:]
	tokens = ["CLS"]
	for entry in entries:
		tokens += tokenizer.tokenize(entry) + ["[SEP]"]
	tok_ids = tokenizer.convert_tokens_to_ids(tokens)
	tok_tensors = torch.tensor([tok_ids])

	with torch.no_grad():
		try:
			class_hidden_state = model(tok_tensors)[0]
			vector_dict[int(columns[0])] = class_hidden_state[0, 0]
		except:
			import pdb
			pdb.set_trace()
			print("exception in ", entries)

sorted_tensors = sorted(vector_dict.values(), key = lambda kv:(kv[1], kv[0]))

"Writing the tensors!"
with open(os.path.abspath(sys.argv[2]), "wb") as fout:
	pickle.dump(sorted_tensors, fout, protocol=pickle.HIGHEST_PROTOCOL)
