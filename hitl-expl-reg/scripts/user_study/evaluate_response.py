import json, math
import numpy as np
import pandas as pd

NUM_INSTANCES = 25
CLASSES = {
    0: 'negative',
    1: 'positive',
}

# shuffle_key_path = 'shuffle_key.csv'
# shuffle_key = array = np.loadtxt(shuffle_key_path, delimiter=",", dtype='int')

response_path = 'v2/csv/Brihi_UserStudyB_v2 - Sheet1.csv'
response = pd.read_csv(response_path)

# user_study_path = 'v1/user_study.jsonl'
user_study_path = 'user_study_v2.jsonl'
with open(user_study_path) as f:
    user_study = [json.loads(line) for line in f]

if 'UserStudyA' in response_path:
    user_study = user_study[:NUM_INSTANCES]
    # shuffle_key = shuffle_key[:NUM_INSTANCES]
else:
    user_study = user_study[NUM_INSTANCES:]
    # shuffle_key = shuffle_key[NUM_INSTANCES:]

part1 = []
part2 = []
part3 = []
for row in response.itertuples():
    if row[1] not in ['Sentiment (0-1)', 'Plausibility (1-5)']:
        if isinstance(row[1], str):
            if len(part2) == 5*NUM_INSTANCES:
                v0 = int(row[1])
            else:
                v0, v1 = int(row[1]), int(row[2])
        else:
            continue

        if len(part1) < NUM_INSTANCES:
            part1.append([v0, v1])
        elif len(part2) < 5*NUM_INSTANCES:
            part2.append([v0, v1])
        else:
            part3.append(v0)

assert len(part1) == NUM_INSTANCES
assert len(part2) == 5*NUM_INSTANCES
assert len(part3) == 5*NUM_INSTANCES


forward_sim = {
    'baseline': 0,
    'sgt+p': 0,
    'a2r+p': 0,
    'unirex_fp-aa': 0,
    'unirex_fp-dlm': 0,
    'gold': 0,
}

confidence = {
    'baseline': 0,
    'sgt+p': 0,
    'a2r+p': 0,
    'unirex_fp-aa': 0,
    'unirex_fp-dlm': 0,
    'gold': 0,
}

# Part 1
for i, instance in enumerate(user_study):
    target = instance['target']
    user_pred, user_confidence = part1[i]

    if CLASSES[user_pred] == target:
        forward_sim['baseline'] += 1
    confidence['baseline'] += user_confidence

forward_sim['baseline'] /= NUM_INSTANCES
confidence['baseline'] /= NUM_INSTANCES


# Part 2
for i, instance in enumerate(user_study):
    methods = instance['method']
    target = instance['target']
    method_preds = instance['pred']
    user_info = part2[5*i:5*i+5]

    for j, m in enumerate(methods):
        # idx = shuffle_key[i,j]
        idx = j
        user_pred, user_confidence = user_info[idx]
        if CLASSES[user_pred] == method_preds[j]:
            forward_sim[m] += 1
        confidence[m] += user_confidence

for m in methods:
    forward_sim[m] /= NUM_INSTANCES
    confidence[m] /= NUM_INSTANCES



# Part 3
plausibility = {
    'sgt+p': 0,
    'a2r+p': 0,
    'unirex_fp-aa': 0,
    'unirex_fp-dlm': 0,
    'gold': 0,
}

for i, instance in enumerate(user_study):
    methods = instance['method']
    user_plaus = part3[5*i:5*i+5]
    for j, m in enumerate(methods):
        # idx = shuffle_key[i,j]
        idx = j
        plausibility[m] += user_plaus[idx]

for m in methods:
    plausibility[m] /= NUM_INSTANCES

print('\n')

print('forward sim')
print(forward_sim)
print('\n')

print('confidence')
print(confidence)
print('\n')

print('plausibility')
print(plausibility)
print('\n')

