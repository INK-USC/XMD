import json
from statsmodels.stats.inter_rater import fleiss_kappa
import numpy as np
import pandas as pd

NUM_INSTANCES = 25
CLASSES = {
    0: 'negative',
    1: 'positive',
}

NAMES = [
    'Brihi_UserStudyA',
    'Jun_UserStudyA',
    'Pei_UserStudyA',
    'Qinyuan_UserStudyA',
    'Soumya_UserStudyA',
    'Peifeng_UserStudyB',
    'Reina_UserStudyB',
    'Xisen_UserStudyB',
    'Peifeng_UserStudyB',
    'Brihi_UserStudyB',
]

annot_matrix_sentiment = np.zeros((150, 2), dtype=int)
annot_matrix_confidence = np.zeros((150, 4), dtype=int)
annot_matrix_plaus = np.zeros((125, 5), dtype=int)

for name in NAMES:

    response_path = f'v2/csv/{name}_v2 - Sheet1.csv'
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

    part_12 = np.array(part1 + part2)
    cur_sentiment = part_12[:,0]
    cur_confidence = part_12[:,1] - 1
    cur_plaus = np.array(part3) - 1

    for k, rating in enumerate(cur_sentiment):
        annot_matrix_sentiment[k, rating] += 1

    for k, rating in enumerate(cur_confidence):
        annot_matrix_confidence[k, rating] += 1

    for k, rating in enumerate(cur_plaus):
        annot_matrix_plaus[k, rating] += 1


print(f'\nFleiss Kappa (sentiment): {fleiss_kappa(annot_matrix_sentiment)}\n')
print(f'Fleiss Kappa (confidence): {fleiss_kappa(annot_matrix_confidence)}\n')
print(f'Fleiss Kappa (plaus): {fleiss_kappa(annot_matrix_plaus)}\n')
