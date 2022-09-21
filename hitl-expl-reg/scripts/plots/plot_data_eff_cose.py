
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
            
        0.347224, 0.398512, 0.456498,
        0.347224, 0.398512, 0.456498,
        0.347224, 0.398512, 0.456498,
        0.347224, 0.398512, 0.456498,
        0.347224, 0.398512, 0.456498,
        0.347224, 0.398512, 0.456498,



        0.44977, 0.509025, 0.450322,
        0.44977, 0.509025, 0.450322,
        0.44977, 0.509025, 0.450322,
        0.44977, 0.509025, 0.450322,
        0.44977, 0.509025, 0.450322,
        0.44977, 0.509025, 0.450322,
        






        0.488356, 0.470429, 0.439143,
        0.397656, 0.412793, 0.412584,
        0.443253, 0.478669, 0.390269,

        0.438271, 0.453841, 0.488893,
        0.433924, 0.490801, 0.392881,
        0.375191, 0.465938, 0.464684,

        0.409342, 0.406359, 0.37871,
        0.372296, 0.295601, 0.421152,
        0.394051, 0.480183, 0.414518,

        0.346205, 0.421197, 0.463367,
        0.431589, 0.413809, 0.435685,
        0.33406, 0.368747, 0.382655,


        0.407076, 0.35754, 0.440676,
        0.435653, 0.398336, 0.426082,
        0.428805, 0.465088, 0.463426,

        0.426311, 0.426292, 0.503615,







        0.73013, 0.706226, 0.663068,
        0.705789, 0.699558, 0.699508,
        0.7123, 0.689101, 0.692644,

        0.702622, 0.69571, 0.724726,
        0.702976, 0.718955, 0.717681,
        0.709886, 0.705509, 0.717546,

        0.704045, 0.712954, 0.712981,
        0.72061, 0.714311, 0.696392,
        0.710506, 0.727718, 0.711908,

        0.725539, 0.710611, 0.737152,
        0.723994, 0.729524, 0.722143,
        0.704823, 0.683292, 0.712173,

        0.744817, 0.741937, 0.743026,
        0.752173, 0.742288, 0.721825,
        0.734714, 0.717322, 0.741418,

        0.766243, 0.754862, 0.767399,





        0.675856, 0.692624, 0.673095,
        0.661361, 0.666088, 0.66678,
        0.631435, 0.645257, 0.564349,

        0.682029, 0.70407, 0.689215,
        0.671182, 0.688239, 0.688982,
        0.661561, 0.677113, 0.683611,

        0.7119, 0.691271, 0.708163,
        0.699414, 0.712783, 0.70368,
        0.691761, 0.700049, 0.693595,

        0.737532, 0.715155, 0.716078,
        0.714748, 0.734923, 0.727052,
        0.712588, 0.715445, 0.736691,

        0.731834, 0.748692, 0.740771,
        0.744254, 0.722099, 0.743614,
        0.710977, 0.743892, 0.7408,

        0.748423, 0.755948, 0.749343,







        


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
save_path = os.path.join(save_dir, 'data_eff_cose.png')
plot.figure.savefig(save_path, bbox_inches='tight')