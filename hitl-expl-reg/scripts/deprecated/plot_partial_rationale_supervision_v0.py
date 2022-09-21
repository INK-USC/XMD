
import os
import seaborn as sns
import pandas as pd
from matplotlib import pyplot

# Create data frame
d = {
    'Method': [
        'Vanilla', 'Vanilla', 'Vanilla',
        'Vanilla', 'Vanilla', 'Vanilla',
        'Vanilla', 'Vanilla', 'Vanilla',
        'Vanilla', 'Vanilla', 'Vanilla',
        'Vanilla', 'Vanilla', 'Vanilla',
        'Vanilla', 'Vanilla', 'Vanilla',

        'UniREx (F-AA)', 'UniREx (F-AA)', 'UniREx (F-AA)',
        'UniREx (F-AA)', 'UniREx (F-AA)', 'UniREx (F-AA)',
        'UniREx (F-AA)', 'UniREx (F-AA)', 'UniREx (F-AA)',
        'UniREx (F-AA)', 'UniREx (F-AA)', 'UniREx (F-AA)',
        'UniREx (F-AA)', 'UniREx (F-AA)', 'UniREx (F-AA)',
        'UniREx (F-AA)', 'UniREx (F-AA)', 'UniREx (F-AA)',

        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',

        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',

        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',

        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',

        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',

        'UniREx (FP-SLM)', 'UniREx (FP-SLM)', 'UniREx (FP-SLM)',
    ],
    'Percentage of Train Instances with Gold Rationales': [
        0.5, 0.5, 0.5,
        1.0, 1.0, 1.0,
        5.0, 5.0, 5.0,
        10.0, 10.0, 10.0,
        20.0, 20.0, 20.0,
        100.0, 100.0, 100.0,

        0.5, 0.5, 0.5,
        1.0, 1.0, 1.0,
        5.0, 5.0, 5.0,
        10.0, 10.0, 10.0,
        20.0, 20.0, 20.0,
        100.0, 100.0, 100.0,

        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,
        0.5, 0.5, 0.5,

        1.0, 1.0, 1.0,
        1.0, 1.0, 1.0,
        1.0, 1.0, 1.0,

        5.0, 5.0, 5.0,
        5.0, 5.0, 5.0,
        5.0, 5.0, 5.0,

        10.0, 10.0, 10.0,
        10.0, 10.0, 10.0,
        10.0, 10.0, 10.0,

        20.0, 20.0, 20.0,
        20.0, 20.0, 20.0,
        20.0, 20.0, 20.0,

        100.0, 100.0, 100.0,
    ],
    'Rationale Plausibility (AUPRC)': [
        0.498858, 0.542804, 0.513218,
        0.498858, 0.542804, 0.513218,
        0.498858, 0.542804, 0.513218,
        0.498858, 0.542804, 0.513218,
        0.498858, 0.542804, 0.513218,
        0.498858, 0.542804, 0.513218,

        0.46685, 0.49405, 0.452482,
        0.46685, 0.49405, 0.452482,
        0.46685, 0.49405, 0.452482,
        0.46685, 0.49405, 0.452482,
        0.46685, 0.49405, 0.452482,
        0.46685, 0.49405, 0.452482,

        0.728857, 0.75474, 0.739423,
        0.751546, 0.755904, 0.759902,
        0.749934, 0.733653, 0.729902,

        0.748539, 0.763397, 0.743894,
        0.756074, 0.767833, 0.748305,
        0.746192, 0.749993, 0.741152,

        0.795666, 0.783404, 0.791579,
        0.764232, 0.79, 0.741159,
        0.788614, 0.785225, 0.784981,

        0.794706, 0.79569, 0.791316,
        0.786241, 0.783007, 0.782295,
        0.798315, 0.803672, 0.804498,

        0.810047, 0.818795, 0.81078,
        0.82076, 0.807226, 0.808344,
        0.814844, 0.812133, 0.811609,

        0.815972, 0.828574, 0.831871,
    ]
}
df = pd.DataFrame(data=d)

# Plot data from data frame
pyplot.figure(figsize=(8, 6))
sns.set_theme(style="darkgrid")
plot = sns.lineplot(
    data=df, 
    x='Percentage of Train Instances with Gold Rationales',
    y='Rationale Plausibility (AUPRC)',
    hue='Method',
    marker='o',
)
plot.set(xlim=(-1.0, 101.0))

# Save plot to file
save_dir = '../save/plots'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
save_path = os.path.join(save_dir, 'partial_rationale_supervision_plot.png')
plot.figure.savefig(save_path)