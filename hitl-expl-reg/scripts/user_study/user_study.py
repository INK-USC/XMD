import os, argparse, random, json
import numpy as np
from tqdm import tqdm
import pickle5 as pickle
import torch
from transformers import AutoTokenizer

MIN_VAL = -1e5
CLASSES = {
    0: 'negative',
    1: 'positive',
}
METHODS = {
    'sgt+p': 'ER-9281',
    'a2r+p': 'ER-9754',
    'unirex_fp-aa': 'ER-9283',
    'unirex_fp-dlm': 'ER-8738',
    'gold': 'gold',
}


def build_user_study_dict(args, method, exp_id, data_dict, tokenizer, method_path):
    out_file = open(method_path, 'w', encoding='utf-8')

    if exp_id != 'gold':
        preds_path = os.path.join(args.save_dir, exp_id, 'model_outputs', args.dataset, f'{args.split}_preds.pkl')
        attrs_path = os.path.join(args.save_dir, exp_id, 'model_outputs', args.dataset, f'{args.split}_attrs.pkl')
        preds = pickle.load(open(preds_path, 'rb')).numpy()
        attrs = pickle.load(open(attrs_path, 'rb')).numpy()

    method_user_study = []
    num_examples = len(data_dict['input_ids'])
    for i in tqdm(range(num_examples), desc=f'Building user study dict for {method} ({exp_id})'):
        input_ids = data_dict['input_ids'][i]
        attn_mask = data_dict['attention_mask'][i]
        label = data_dict['label'][i]
        gold_rationale = data_dict['rationale'][i]
        
        num_tokens = sum(attn_mask)
        num_gold_tokens = int(sum(gold_rationale[:num_tokens]))
        input_tokens = tokenizer.convert_ids_to_tokens(input_ids)[:num_tokens]

        if exp_id == 'gold':
            attr = np.array(gold_rationale)
        else:
            attr = attrs[i][:num_tokens]
            attr[0] = MIN_VAL
            attr[-1] = MIN_VAL

        expl_indices = np.sort(np.argsort(attr)[::-1][:num_gold_tokens])
        expl_tokens = [input_tokens[j] for j in expl_indices]
        target = CLASSES[label]
        pred = target if exp_id == 'gold' else CLASSES[preds[i]]

        cur_data = {
            'input_tokens': input_tokens,
            'expl_tokens': expl_tokens,
            'expl_indices': expl_indices.tolist(),
            'target': target,
            'pred': pred,
        }
        json.dump(cur_data, out_file, ensure_ascii=False)
        out_file.write('\n')

        method_user_study.append(cur_data)

    return method_user_study


def main(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    
    tokenizer = AutoTokenizer.from_pretrained(args.arch)
    keys = ['input_ids', 'attention_mask', 'label', 'rationale']
    data_dict = {}
    for key in keys:
        data_path = os.path.join(args.data_dir, args.dataset, args.arch, args.split, f'{key}.pkl')
        data_dict[key] = pickle.load(open(data_path, 'rb'))
    num_examples = len(data_dict['input_ids'])

    out_dir = os.path.join(args.save_dir, 'user_study', args.dataset)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    full_user_study_dict = {}
    for method, exp_id in METHODS.items():
        method_path = os.path.join(out_dir, f'{method}.jsonl')
        if os.path.exists(method_path):
            with open(method_path) as f:
                full_user_study_dict[method] = [json.loads(line) for line in f]
            print(f'Loaded {method} ({exp_id}).')
        else:
            full_user_study_dict[method] = build_user_study_dict(args, method, exp_id, data_dict, tokenizer, method_path)
    
    example_indices_filename = os.path.join(out_dir, 'example_indices.pkl')
    if os.path.exists(example_indices_filename):
        example_indices = pickle.load(open(example_indices_filename, 'rb'))
    else:
        example_indices = np.random.choice(num_examples, num_examples, replace=False)
        with open(example_indices_filename, 'wb') as f:
            pickle.dump(example_indices, f)

    user_study = []
    num_methods = len(METHODS)
    method_list = list(METHODS.keys())
    for i in example_indices:
        gold_expl = full_user_study_dict['gold'][i]['expl_tokens']
        all_expls = [full_user_study_dict[m][i]['expl_tokens'] for m in method_list]

        input_len = len(full_user_study_dict['gold'][i]['input_tokens'])
        expl_len = len(gold_expl)
        if (
            expl_len > 0.5 * input_len
            or sum([x == gold_expl for x in all_expls]) == num_methods
        ):
            continue

        cur_example = {
            'method': [],
            'input_tokens': full_user_study_dict['gold'][i]['input_tokens'],
            'expl_tokens': [],
            'expl_indices': [],
            'target': full_user_study_dict['gold'][i]['target'],
            'pred': [],
        }
        method_indices = np.random.choice(num_methods, num_methods, replace=False)
        for j in method_indices:
            cur_method = method_list[j]
            cur_expl_tokens = full_user_study_dict[cur_method][i]['expl_tokens']
            cur_expl_indices = full_user_study_dict[cur_method][i]['expl_indices']
            cur_pred = full_user_study_dict[cur_method][i]['pred']

            cur_example['method'].append(cur_method)
            cur_example['expl_tokens'].append(cur_expl_tokens)
            cur_example['expl_indices'].append(cur_expl_indices)
            cur_example['pred'].append(cur_pred)
            
        user_study.append(cur_example)
        if len(user_study) == args.num_user_study_examples:
            break

    user_study_path = os.path.join(out_dir, 'user_study.jsonl')
    user_study_out_file = open(user_study_path, 'w', encoding='utf-8')
    for u in user_study:
        json.dump(u, user_study_out_file, ensure_ascii=False)
        user_study_out_file.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='../data')
    parser.add_argument('--save_dir', type=str, default='../save')
    parser.add_argument('--dataset', type=str, default='sst', choices=['sst'])
    parser.add_argument('--arch', type=str, default='google/bigbird-roberta-base')
    parser.add_argument('--split', type=str, default='test')
    parser.add_argument('--num_user_study_examples', type=int, default=50)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    main(args)