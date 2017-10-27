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
df['Y'] = pd.Series(df['new_value']<=10)

df_sort = df.sort_values('new_value')
# '(df['Y']==True).sum()' will gives the number of compounds that have measurement values less that 100
df_sort_Y = df_sort[:(df['Y']==True).sum()] # Pick all positive drugs, first N in dataframe
df_sort_N = df_sort[-(df['Y']==True).sum():] # Pick up last N in dataframe
df_sort_YN = pd.concat([df_sort_Y,df_sort_N])

"""Get the labels"""
Y = list(df_sort_YN['Y'])
Y0 = [0]*len(Y)
for i in range(len(Y)):
    if Y[i] == True:
        Y0[i] = 1

b = []
""""Get the ecfp"""
drug = list(df_sort_YN['ecfp'])
for i in drug:
    ecfp = []
    for n in i:
        ecfp.append(int(n))
    b.append(ecfp)

np.savetxt('X.txt', b, fmt = '%d')
np.savetxt('Y.txt', Y0, fmt = '%d')

