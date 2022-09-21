
import os
import seaborn as sns
import pandas as pd
from matplotlib import pyplot

# Create data frame
d = {
    'Method': [
        'AA (IG)', 'AA (IG)', 'AA (IG)',
        'AA (IG)', 'AA (IG)', 'AA (IG)',
        'AA (IG)', 'AA (IG)', 'AA (IG)',
        'AA (IG)', 'AA (IG)', 'AA (IG)',
        'AA (IG)', 'AA (IG)', 'AA (IG)',
        'AA (IG)', 'AA (IG)', 'AA (IG)',





        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',
        'UNIREX (AA-F)', 'UNIREX (AA-F)', 'UNIREX (AA-F)',




        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',

        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',

        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',

        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',

        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',
        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',

        'UNIREX (AA-FP)', 'UNIREX (AA-FP)', 'UNIREX (AA-FP)',





        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',

        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',

        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',

        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',

        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',
        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',

        'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)', 'UNIREX (DLM-FP)',





        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',

        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',

        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',

        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',

        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',
        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',

        'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)', 'UNIREX (SLM-FP)',










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
    'Plausibility (AUPRC)': [
        0.484307, 0.518821, 0.495017,
        0.484307, 0.518821, 0.495017,
        0.484307, 0.518821, 0.495017,
        0.484307, 0.518821, 0.495017,
        0.484307, 0.518821, 0.495017,
        0.484307, 0.518821, 0.495017,





        0.477779, 0.47211, 0.494068,
        0.477779, 0.47211, 0.494068,
        0.477779, 0.47211, 0.494068,
        0.477779, 0.47211, 0.494068,
        0.477779, 0.47211, 0.494068,
        0.477779, 0.47211, 0.494068,




        0.458373, 0.489701, 0.452086,
        0.462998, 0.466791, 0.504257,
        0.459972, 0.446527, 0.465832,

        0.458754, 0.469928, 0.447157,
        0.465375, 0.460165, 0.466135, 	
        0.46843, 0.478692, 0.447127,

        0.474131, 0.464631, 0.445119,
        0.452414, 0.451118, 0.484869,
        0.446793, 0.465607, 0.447214,

        0.467457, 0.450732, 0.448247,
        0.463326, 0.48577, 0.448031,
        0.4385, 0.479647, 0.454557,

        0.461396, 0.464939, 0.453772,
        0.479963, 0.460801, 0.478163,
        0.455808, 0.46529, 0.472363,

        0.493001, 0.486964, 0.448132,







        



        0.738065, 0.748839, 0.758172,
        0.756805, 0.761475, 0.753991,
        0.770592, 0.731161, 0.764446,

        0.760704, 0.746933, 0.76939,
        0.755778, 0.76621, 0.769747,
        0.749174, 0.770618, 0.768235,

        0.792761, 0.807567, 0.8126,
        0.794724, 0.799583, 0.789378,
        0.801097, 0.794209, 0.79713,

        0.80784, 0.805263, 0.791478,
        0.804669, 0.80962, 0.821513,
        0.79946, 0.810248, 0.809522,

        0.820026, 0.830365, 0.820887,
        0.818126, 0.819494, 0.827024,
        0.820815, 0.824453, 0.826267,           

        0.849493, 0.862304, 0.862194,







        0.755761, 0.742009, 0.745971,
        0.751316, 0.756081, 0.748035,
        0.73618, 0.735595, 0.711503,

        0.74989, 0.749348, 0.743431,
        0.747481, 0.758916, 0.759325,
        0.741599, 0.752747, 0.751145,

        0.788446, 0.789232, 0.784404,
        0.787581, 0.772964, 0.764787,
        0.782202, 0.784788, 0.773249,

        0.79559, 0.799834, 0.791275,
        0.798064, 0.786412, 0.786787,
        0.799637, 0.800898, 0.803664,

        0.818795, 0.810047, 0.81078,
        0.82076, 0.808344, 0.807226,
        0.812133, 0.814844, 0.811609,

        0.831192, 0.807304, 0.834166,        


    ]
}
df = pd.DataFrame(data=d)

# Plot data from data frame
pyplot.figure(figsize=(8, 6))
sns.set_theme(style="darkgrid")
plot = sns.lineplot(
    data=df, 
    x='Percentage of Train Instances with Gold Rationales',
    y='Plausibility (AUPRC)',
    hue='Method',
    marker='o',
)
plot.set(xlim=(-1.0, 101.0))

# Save plot to file
save_dir = '../save/plots'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
save_path = os.path.join(save_dir, 'data_eff_sst.png')
plot.figure.savefig(save_path, bbox_inches='tight')