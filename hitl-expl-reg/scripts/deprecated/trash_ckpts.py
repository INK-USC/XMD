import os
import shutil

SAVE_EXPS = [
                # STF Vanilla
                4528, 4605 

]



SAVE = '/home/aaron/SaliencyLM/save'

def check_empty(dir):
    isEmpty = True
    for root, dirs, files in os.walk(dir, topdown=False):
        if len(files) != 0:
            isEmpty = False
    return isEmpty

def get_exps(save_dir):
    exps = []
    others = []
    for d in os.listdir(save_dir):
        abs_d = os.path.join(save_dir, d)
        if os.path.isdir(abs_d):
            exps.append(abs_d)
        else:
            others.append(abs_d)

    return exps, others

def empty_filter(exps):
    empty_dirs, non_empty_dirs = [], []
    for e in exps:
        if check_empty(e):
            empty_dirs.append(e)
        else:
            non_empty_dirs.append(e)
    return non_empty_dirs, empty_dirs

def neptune_filter(exps):
    nept_exps, non_nept_exps = [], []
    for e in exps:
        if 'SLM-' in e:
            nept_exps.append(e)
        else:
            non_nept_exps.append(e)
    return nept_exps, non_nept_exps

def direct_filter(exps, save_exps):
    selected, non_selected = [], []
    exp_str = [os.path.join(SAVE, 'SLM-{}'.format(e)) for e in save_exps]
    for e in exps:
        if e in exp_str:
            selected.append(e)
        else:
            non_selected.append(e)
    
    for e in exp_str:
        if not e in selected:
            print(e)
    return selected, non_selected

if __name__ == '__main__':
    trash = []
    exps, others = get_exps(SAVE)
    trash.extend(others)

    non_empty_dirs, empty_dirs = empty_filter(exps)
    print(f'empty dirs: {len(empty_dirs)}, non-empty dirs: {len(non_empty_dirs)}')
    trash.extend(empty_dirs)

    nept_dirs, non_nept_dirs = neptune_filter(non_empty_dirs)
    print(f'neptune dirs: {len(nept_dirs)}, non-neptune dirs: {len(non_nept_dirs)}')
    trash.extend(non_nept_dirs)

    selected, non_selected = direct_filter(nept_dirs, SAVE_EXPS)
    print(f'whitelisted: {len(SAVE_EXPS)}, selected: {len(selected)}, not selected: {len(non_selected)}')

    trash.extend(non_selected)
    print(f'trashed: {len(trash)}')

    for e in trash:
        try:
            paths = os.path.split(e)
            if not paths[1].startswith('trash_'):
                os.rename(e, os.path.join(paths[0], 'trash_' + paths[1]))
        except:
            print("ERROR: {}".format(e))