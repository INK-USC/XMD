import os, argparse
import numpy as np
import pandas as pd
from tqdm import tqdm

def main(args):
    data_path = os.path.join(args.data_dir, args.dataset, f'{args.dataset}_{args.filename}.csv')
    df = pd.read_csv(data_path)

    col_list = list(df.columns)
    for key in ['Id', 'Creation Time', 'Owner']:
        col_list.remove(key)
    df = df.drop_duplicates(subset=col_list)
   
    remove_list = [
        'logs/test_best_perf (last)', 'logs/dev_best_perf (last)',
        'logs/epoch (last)', 'logs/best_epoch (last)', 
        'parameters/seed', 'parameters/data/num_train_seed', 'parameters/data/pct_train_rationales_seed',
    ]
    for key in remove_list:
        if key in col_list:
            col_list.remove(key)

    df = df.fillna(-1)
    df_group = df.groupby(col_list)

    best_group = None
    if args.model_selection == 'mean':
        best_dev_perf = -float('inf')
        group_count = 0
    while best_group is None:
        dev_perfs = None
        for i, (_, group) in tqdm(enumerate(df_group.groups.items()), total=len(df_group.groups)):
            group = list(group)
            if args.pct_train_rationales or args.num_train > 0:
                if len(group) != args.num_seeds**2:
                    continue
            else:
                if len(group) != args.num_seeds:
                    continue
            
            filters = [
                all([df.loc[x]['parameters/model/optimizer/lr'] == args.lr for x in group]),
                all([df.loc[x]['parameters/data/num_train'] == args.num_train for x in group]),
            ]

            if args.pct_train_rationales:
                filters.append(all([df.loc[x]['parameters/data/pct_train_rationales'] == args.pct_train_rationales for x in group]))
            elif args.filename == 'er':
                filters.append(all([df.loc[x]['parameters/data/pct_train_rationales'] < 0 for x in group]))

            if args.filename == 'er':
                filters.append(all([df.loc[x]['parameters/model/attr_algo'] == args.attr_algo for x in group]))

                if args.pos_expl:
                    filters.append(all([df.loc[x]['parameters/model/pos_expl_wt'] > 0 for x in group]))
                else:
                    filters.append(all([df.loc[x]['parameters/model/pos_expl_wt'] == 0 for x in group]))

                if args.neg_expl:
                    filters.append(all([df.loc[x]['parameters/model/neg_expl_wt'] > 0 for x in group]))
                else:
                    filters.append(all([df.loc[x]['parameters/model/neg_expl_wt'] == 0 for x in group]))

                if args.pos_expl_criterion:
                    filters.append(all([df.loc[x]['parameters/model/pos_expl_criterion'] == args.pos_expl_criterion for x in group]))

                if args.neg_expl_criterion:
                    filters.append(all([df.loc[x]['parameters/model/neg_expl_criterion'] == args.neg_expl_criterion for x in group]))
            
            if not all(filters) and i < len(df_group.groups)-1:
                continue
            elif not all(filters) and i == len(df_group.groups)-1 and best_group is None:
                raise ValueError('No experiments passed the filters!')
            elif not all(filters) and i == len(df_group.groups)-1:
                break

            cur_dev_perfs = np.array([df.loc[x]['logs/dev_best_perf (last)'] for x in group])
            cur_dev_perfs = np.expand_dims(cur_dev_perfs, axis=0)
            if np.isnan(np.sum(cur_dev_perfs)):
                continue

            if args.model_selection == 'mean':
                if best_dev_perf < 0:
                    best_dev_perf = np.mean(cur_dev_perfs)
                    best_group = group
                elif np.mean(cur_dev_perfs) > best_dev_perf:
                    best_dev_perf = np.mean(cur_dev_perfs)
                    best_group = group

                group_count += 1

            elif args.model_selection == 'vote':
                if dev_perfs is None:
                    dev_perfs = cur_dev_perfs
                    best_group = group
                else:
                    dev_perfs = np.concatenate((dev_perfs, cur_dev_perfs), axis=0)
                    votes = np.bincount(np.argmax(dev_perfs, axis=0), minlength=len(dev_perfs))
                    best_group_idx = np.argmax(votes)
                    if best_group_idx == i:
                        best_group = group

    group_info = [df.loc[x] for x in best_group]

    dev_perf = np.array([x['logs/dev_best_perf (last)'] for x in group_info])
    test_perf = np.array([x['logs/test_best_perf (last)'] for x in group_info])

    mean_dev_perf = np.mean(dev_perf)
    std_dev_perf = np.std(dev_perf, ddof=1)

    mean_test_perf = np.mean(test_perf)
    std_test_perf = np.std(test_perf, ddof=1)

    print(f'\ndev perf: {mean_dev_perf:.2f} +/- {std_dev_perf:.2f}')
    print(f'test perf: {mean_test_perf:.2f} +/- {std_test_perf:.2f}\n')
    for x in group_info:
        print(x)
        print('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='../data/neptune/')
    parser.add_argument('--num_seeds', type=int, default=3)
    parser.add_argument('--model_selection', type=str, default='mean', choices=['mean', 'vote'])
    parser.add_argument('--dataset', type=str, choices=['sst', 'cose', 'movies', 'multirc', 'esnli', 'yelp', 'amazon', 'stf', 'olid', 'irony'])
    parser.add_argument('--filename', type=str, choices=['lm', 'er', 'fresh'])
    parser.add_argument('--attr_algo', type=str, choices=['input-x-gradient', 'integrated-gradients', 'saliency', 'deep-lift', 'gold', 'inv', 'rand', 'lm-gold'])
    parser.add_argument('--pos_expl', action='store_true')
    parser.add_argument('--neg_expl', action='store_true')
    parser.add_argument('--pos_expl_criterion', type=str, choices=['bce','mse','huber','l1', 'order'])
    parser.add_argument('--neg_expl_criterion', type=str, choices=['zero_all', 'l1', 'l1_incorrect'])
    parser.add_argument('--lr', type=float, default=2e-5)
    parser.add_argument('--num_train', type=int, default=-1)
    parser.add_argument('--num_train_seed', type=int, default=0)
    parser.add_argument('--pct_train_rationales', type=float)
    args = parser.parse_args()
    main(args)