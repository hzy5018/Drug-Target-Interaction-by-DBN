import os
import numpy as np
import pandas as pd

rootdir = './CDK_datasets'

#The below is a tedious, but easy understanding of using os to get all the rootdir ecfp files
subfolder = []
for root, dirs, files in os.walk(rootdir):
    a = []
    for name in files:
        if name.startswith("ecfp") or name.startswith("P_0"):
            a.append(os.path.join(root, name))
    subfolder.append(a)

sub =  subfolder[1:]# The fisrt element of subfolder is [], we need to drop it.
# print sub

def read1folder(a):
    if a[0].split('/')[-1][0:4] == "ecfp": # Determine which file is ecfp for drug.
        drug_file = a[0]
        protein_file = a[1]
    else:
        drug_file = a[1]
        protein_file = a[0]

    """
    First, read the ecfp file
    """
    target = []
    canonical_smiles = []
    ecfp = []
    measurement_value = []
    new_value = []
    measurement_type = []
    with open(drug_file) as f:
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

    df_sort = df.sort_values('new_value')

    path = drug_file.split('ecfp')[0]
    name = drug_file.split('ecfp')[1]

    df_sort.to_csv(path + "df" + name + '.csv')

for i in range(len(sub)):
    read1folder(sub[i])
