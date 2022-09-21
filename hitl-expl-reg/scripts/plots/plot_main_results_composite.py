
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
# d = {
#     'Method': [
#         'AA (IG)', 'AA (IG)', 'AA (IG)', 'AA (IG)', 'AA (IG)',
#         'L2E', 'L2E', 'L2E', 'L2E', 'L2E',
#         'SGT', 'SGT', 'SGT', 'SGT', 'SGT',
#         'FRESH', 'FRESH', 'FRESH', 'FRESH', 'FRESH',
#         'A2R', 'A2R', 'A2R', 'A2R', 'A2R',
#         'SGT+P', 'SGT+P', 'SGT+P', 'SGT+P', 'SGT+P',
#         'FRESH+P', 'FRESH+P', 'FRESH+P', 'FRESH+P', 'FRESH+P',
#         'A2R+P', 'A2R+P', 'A2R+P', 'A2R+P', 'A2R+P',
#         'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
#         'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
#         'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
#     ],
#     'Dataset': [
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#         'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
#     ],
#     'Composite NRG': [
#         0.526, 0.439, 0.578, 0.499, 0.596,
#         0.557, 0.550, 0.544, 0.522, 0.606,
#         0.632, 0.553, 0.618, 0.594, 0.595,
#         0.330, 0.645, 0.302, 0.675, 0.518,
#         0.479, 0.431, 0.277, 0.217, 0.273,
#         0.596, 0.586, 0.601, 0.630, 0.608,
#         0.426, 0.491, 0.374, 0.404, 0.614,
#         0.695, 0.585, 0.488, 0.516, 0.800,
#         0.639, 0.601, 0.690, 0.711, 0.622,
#         0.897, 0.744, 0.814, 0.751, 0.857,
#         0.891, 0.754, 0.807, 0.784, 0.864,

#     ]

# }




d1 = {
    'Method': [
        'AA (IG)', 'AA (IG)', 'AA (IG)', 'AA (IG)', 'AA (IG)',
        'L2E', 'L2E', 'L2E', 'L2E', 'L2E',
        'SGT', 'SGT', 'SGT', 'SGT', 'SGT',
        'FRESH', 'FRESH', 'FRESH', 'FRESH', 'FRESH',
        'A2R', 'A2R', 'A2R', 'A2R', 'A2R',
        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
    ],
    'Dataset': [
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
    ],
    'Composite NRG': [
        0.526, 0.439, 0.578, 0.499, 0.596,
        0.557, 0.550, 0.544, 0.522, 0.606,
        0.632, 0.553, 0.618, 0.594, 0.595,
        0.330, 0.645, 0.302, 0.675, 0.518,
        0.479, 0.431, 0.277, 0.217, 0.273,
        0.639, 0.601, 0.690, 0.711, 0.622,

    ]

}


d2 = {
    'Method': [
        'SGT+P', 'SGT+P', 'SGT+P', 'SGT+P', 'SGT+P',
        'FRESH+P', 'FRESH+P', 'FRESH+P', 'FRESH+P', 'FRESH+P',
        'A2R+P', 'A2R+P', 'A2R+P', 'A2R+P', 'A2R+P',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
    ],
    'Dataset': [
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
        'SST', 'Movies', 'CoS-E', 'MultiRC', 'e-SNLI',
    ],
    'Composite NRG': [
        0.596, 0.586, 0.601, 0.630, 0.608,
        0.426, 0.491, 0.374, 0.404, 0.614,
        0.695, 0.585, 0.488, 0.516, 0.800,
        0.897, 0.744, 0.814, 0.751, 0.857,
        0.891, 0.754, 0.807, 0.784, 0.864,
    ]

}
df1 = pd.DataFrame(data=d1)
df2 = pd.DataFrame(data=d2)



# Plot data from data frame
sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(1, 2)
p1 = sns.barplot(  y='Composite NRG', x='Method', hue='Dataset', data=df1,  orient='v' , ax=axes[0])
p2 = sns.barplot(  y='Composite NRG', x='Method', hue='Dataset', data=df2,  orient='v' , ax=axes[1])
fig.set_size_inches(22, 6)
p1.set(xlabel=None)
p2.set(xlabel=None)
p2.set(ylabel=None)
p1.set(ylim=(0.0, 0.97))
p2.set(ylim=(0.0, 0.97))
p2.set(yticks=[])

p1.legend(loc='upper left')
p2.legend(loc='upper left')
change_width(p1, 0.15)
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
save_path = os.path.join(save_dir, 'main_results_composite.png')
# plot.figure.savefig(save_path, bbox_inches='tight')
fig.savefig(save_path, bbox_inches='tight')
# fig.savefig(save_path)