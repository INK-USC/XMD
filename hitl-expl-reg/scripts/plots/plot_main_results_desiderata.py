
import os
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

# Create data frame
d1 = {
    'Method': [
        'AA (IG)', 'L2E', 'SGT', 
        'FRESH', 'A2R', 'UNIREX (AA-F)',

        'AA (IG)', 'L2E', 'SGT', 
        'FRESH', 'A2R', 'UNIREX (AA-F)',

        'AA (IG)', 'L2E', 'SGT', 
        'FRESH', 'A2R', 'UNIREX (AA-F)'

    ],
    'Desiderata': [
        'Faithfulness', 'Faithfulness', 'Faithfulness', 
        'Faithfulness', 'Faithfulness', 'Faithfulness',

        'Plausibility', 'Plausibility', 'Plausibility', 
        'Plausibility', 'Plausibility', 'Plausibility',

        'Task Performance', 'Task Performance', 'Task Performance',
        'Task Performance', 'Task Performance', 'Task Performance',

    ],
    'NRG': [
        0.310, 0.450, 0.492,
        0.669, 0.638, 0.697,

        0.300, 0.244, 0.314,
        0.339, 0.297, 0.330,

        0.973, 0.973, 0.989,
        0.474, 0.071, 0.931,

    ]
}
df1 = pd.DataFrame(data=d1)







d2 = {
    'Method': [
        'SGT+P', 'FRESH+P', 'A2R+P', 
        'UNIREX (DLM-FP)', 'UNIREX (SLM-FP)',

        'SGT+P', 'FRESH+P', 'A2R+P', 
        'UNIREX (DLM-FP)', 'UNIREX (SLM-FP)',

        'SGT+P', 'FRESH+P', 'A2R+P', 
        'UNIREX (DLM-FP)', 'UNIREX (SLM-FP)',



    ],
    'Desiderata': [
        'Faithfulness', 'Faithfulness', 'Faithfulness', 
        'Faithfulness', 'Faithfulness',

        'Plausibility', 'Plausibility', 'Plausibility', 
        'Plausibility', 'Plausibility',

        'Task Performance', 'Task Performance', 'Task Performance',
        'Task Performance', 'Task Performance',

    ],
    'NRG': [
        0.533, 0.616, 0.678, 0.498, 0.528,
        0.302, 0.632, 0.978, 0.995, 0.976,
        0.977, 0.137, 0.195, 0.945, 0.956,
    ]
}




df2 = pd.DataFrame(data=d2)




# Plot data from data frame
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(1, 2)
p1 = sns.barplot(  y='NRG', x='Desiderata', hue='Method', data=df1,  orient='v' , ax=axes[0], palette='rocket')
p2 = sns.barplot(  y='NRG', x='Desiderata', hue='Method', data=df2,  orient='v' , ax=axes[1], palette='mako')
fig.set_size_inches(22, 6)
p1.set(xlabel=None)
p2.set(xlabel=None)
p2.set(ylabel=None)
p1.set(ylim=(0.0, 1.1))
p2.set(ylim=(0.0, 1.1))
p2.set(yticks=[])

p1.legend(loc='upper left')
p2.legend(loc='upper left')
change_width(p1, 0.13)
change_width(p2, 0.15)

for container in p1.containers:
    p1.bar_label(container, rotation=45, fmt='%.2f')

for container in p2.containers:
    p2.bar_label(container, rotation=45, fmt='%.2f')

# plt.subplots_adjust(hspace = 0.1)
plt.tight_layout()

# p1._legend.remove()
# plt.figure(figsize=(20, 6))
# plot = sns.barplot(
#     data=df, 
#     x='Method',
#     y='Composite NRG',
#     hue='Dataset',
# )
# plot.set(xlabel=None)

# Save plot to file
save_dir = 'save'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
save_path = os.path.join(save_dir, 'main_results_desiderata.png')
# plot.figure.savefig(save_path, bbox_inches='tight')
fig.savefig(save_path, bbox_inches='tight')
# fig.savefig(save_path)