import argparse, os, sys, math

import numpy as np
import seaborn as sns
import torch
import torch.nn.functional as F
from matplotlib import pyplot as plt
from pickle5 import pickle
from tqdm import tqdm
from transformers import AutoTokenizer

sys.path.append(os.path.join(sys.path[0], '..'))

def main(args):

	assert args.exp_id != None or args.attr_algo == 'gold'
	assert args.arch != None
	assert args.dataset != None
	assert args.split != None


	# Get tokenizer
	tokenizer = AutoTokenizer.from_pretrained(args.arch)


	# Set up data paths
	base_path = os.path.join(args.data_dir, args.dataset, args.arch, args.split)
	data_paths = {}
	data_paths['input_ids'] = os.path.join(base_path, 'input_ids.pkl')
	data_paths['attention_mask'] = os.path.join(base_path, 'attention_mask.pkl')
	data_paths['label'] = os.path.join(base_path, 'label.pkl')

	if args.attr_algo != 'gold':
		data_paths['pred'] = os.path.join(args.save_dir, args.exp_id, 'model_outputs', args.dataset, f'{args.split}_preds.pkl')
	
	if args.attr_algo == 'attention':
		data_paths['expl'] = os.path.join(args.save_dir, args.exp_id, 'model_outputs', args.dataset, f'{args.split}_attns.pkl')
	elif args.attr_algo == 'gold':
		data_paths['expl'] = os.path.join(base_path, 'rationale.pkl')
	else:
		data_paths['expl'] = os.path.join(args.save_dir, args.exp_id, 'model_outputs', args.dataset, f'{args.split}_attrs.pkl')


	# Build dataset dict
	dataset_dict = {}
	for key in tqdm(data_paths.keys(), desc=f'Loading {args.split} dataset'):
		with open(data_paths[key], 'rb') as f:
			dataset_dict[key] = pickle.load(f)
	if args.attr_algo == 'gold':
		dataset_dict['expl'] = [torch.FloatTensor(x) for x in dataset_dict['expl']]


	# Get number of examples to save
	num_examples = len(dataset_dict['input_ids'])
	num_saved_examples = min(args.num_saved_examples, num_examples)


	# Set save dir
	if args.attr_algo == 'gold':
		save_dir = os.path.join(base_path, 'gold_expl_heatmaps')
	else:
		save_dir = os.path.join(args.save_dir, args.exp_id, 'expl_heatmaps', args.split, args.attr_algo)

	if args.attr_algo != 'attention':
		if args.binarize_attrs:
			save_dir = os.path.join(save_dir, 'binarized')
		if args.standardize_attrs:
			save_dir = os.path.join(save_dir, 'standardized')
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)


	# Plot and save heatmaps
	for i in tqdm(range(num_saved_examples), desc='Saving heatmaps'):
		# Gather input data
		cur_text = tokenizer.convert_ids_to_tokens(dataset_dict['input_ids'][i])
		cur_attn_mask = dataset_dict['attention_mask'][i]
		num_tokens = sum(cur_attn_mask)
		cur_text = cur_text[:num_tokens]
		cur_label = dataset_dict['label'][i]
		cur_pred = dataset_dict['pred'][i].item() if args.attr_algo != 'gold' else 'N/A'
		if args.attr_algo == 'attention':
			cur_expls = torch.stack([x[:num_tokens] for x in dataset_dict['expl'][i]])
		else:
			cur_expls = torch.stack([x[:num_tokens] for x in dataset_dict['expl'][i].unsqueeze(0)])

		# Process expl
		cur_expls = cur_expls[:, :num_tokens].float()
		if args.attr_algo not in ['gold', 'attention'] and args.standardize_attrs:
			cur_expls_mean = torch.mean(cur_expls)
			cur_expls_std = torch.std(cur_expls)
			cur_expls = (cur_expls - cur_expls_mean) / cur_expls_std * args.attr_scale_factor
		if args.attr_algo not in ['gold', 'attention'] and args.binarize_attrs:
			num_pos_tokens = max(1, torch.sum(cur_expls.flatten() > 0).item())
			topk_ = max(1, math.floor(num_tokens * args.k / 100))
			topk = min(topk_, num_pos_tokens)
			topk_indices = torch.topk(cur_expls.flatten(), topk, sorted=False).indices
			cur_expls = torch.ones_like(cur_expls) * -10000
			cur_expls = cur_expls.index_fill_(1, topk_indices, 1.0)
		if args.attr_algo not in ['gold', 'attention']:
			cur_expls = torch.sigmoid(cur_expls)

		# Plot expl heatmap
		fig, ax = plt.subplots(figsize=(18,2))
		xticklabels = cur_text
		yticklabels = [cur_label] if args.attr_algo == 'gold' else [cur_pred]
		ax = sns.heatmap(np.array(cur_expls.cpu().numpy()), xticklabels=xticklabels, yticklabels=yticklabels, linewidth=1.5, vmin=0, vmax=1)
		if args.attr_algo == 'attention':
			plt.ylabel('Attention Layer')
		elif args.attr_algo == 'gold':
			plt.ylabel('Target Label')
		else:
			plt.ylabel('Predicted Label')
		plt.title(f'arch={args.arch}, attr={args.attr_algo}, dataset={args.dataset}, split={args.split}, example={i}, target={cur_label}, pred={cur_pred}')

		# Save expl heatmap
		fig_file = f'{args.attr_algo}_{args.split}_{i}'
		if args.binarize_attrs:
			fig_file += f'_k={args.k}'
		if args.standardize_attrs:
			fig_file += f'_std={args.attr_scale_factor}'	
		fig_file += f'.png'
		plt.savefig(os.path.join(save_dir, fig_file), bbox_inches='tight')
		plt.close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Dataset preprocessing')
	parser.add_argument('--data_dir', type=str, default='../data/', help='Root directory for datasets')
	parser.add_argument('--save_dir', type=str, default='../save/', help='Root directory for saved files')
	parser.add_argument('--exp_id', type=str, help='Neptune experiment ID (e.g., ER-X)')
	parser.add_argument('--arch', type=str, default='google/bigbird-roberta-base', choices=['google/bigbird-roberta-base', 'bert-base-uncased'])
	parser.add_argument('--dataset', default='sst', type=str, choices=['sst', 'esnli'])
	parser.add_argument('--split', type=str, choices=['train', 'dev', 'test'])
	parser.add_argument('--attr_algo', type=str, default='integrated-gradients', help='Attribution method', choices=['integrated-gradients', 'input-x-gradient', 'attention', 'lm', 'self_lm', 'gold'])
	parser.add_argument('--num_saved_examples', type=int, default=30, help='Number of examples to save heatmaps for')
	parser.add_argument('--standardize_attrs', action='store_true', help='whether to standardize attrs before normalizing')
	parser.add_argument('--attr_scale_factor', type=float, default=1.0, help='scaling factor used during standardization for controlling entropy of explanation distribution')
	parser.add_argument('--binarize_attrs', action='store_true', help='whether to binarize attributions')
	parser.add_argument('--k', type=int, default=100, help='top-k% threshold')
	args = parser.parse_args()
	main(args)