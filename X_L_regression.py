import os
import numpy as np
import pandas as pd

drugfile = "CDK_datasets/CHEMBL301-P24941/ecfp_bit_CHEMBL301-P24941_info.csv"

target = []
canonical_smiles = []
ecfp = []
measurement_value = []
new_value = []
measurement_type = []
with open(drugfile) as f:
    # skip the first line of file
    next(f)
    for line in f:
        each_line = line.split('" "') # Seperate each column by " ".
        target.append( each_line[0].replace('"','') )
        canonical_smiles.append( each_line[1] )
        ecfp.append( each_line[2] )
        measurement_value.append( float(each_line[3]) )
        new_value.append( float(each_line[4]) )
        measurement_type.append( each_line[5] )

    df = pd.DataFrame()
    df['target'] = pd.Series(target)
    df['canonical_smiles'] = pd.Series(canonical_smiles)
    df['ecfp'] = pd.Series(ecfp)
    df['measurement_value'] = pd.Series(measurement_value)
    df['new_value'] = pd.Series(new_value)
    df['measurement_type'] = pd.Series(measurement_type)
    # df.to_csv('df.csv')

    df_sort = df.sort_values('new_value')
    # df_sort.to_csv('df_sort.csv')

    value = list(df_sort['new_value'])
    log_value = np.log10(value)

    b = []
    drug = list(df_sort['ecfp'])
    for i in drug:
        ecfp = []
        for n in i:
            ecfp.append(int(n))
        b.append(ecfp)

print len(b)

np.savetxt('Model/regression/X.txt', b, fmt = '%d')
np.savetxt('Model/regression/Y.txt', log_value, fmt = '%.3f')

