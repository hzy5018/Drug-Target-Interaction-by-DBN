import os
import numpy as np
import pandas as pd

rootdir = './CDK_datasets'

f_test =  [os.path.join(root, name)
           for root, dirs, files in os.walk(rootdir)
           for name in files
           if name.startswith("ecfp")]

print f_test

def read1folder(a):
    target = []
    canonical_smiles = []
    ecfp = []
    measurement_value = []
    new_value = []
    measurement_type = []
    with open(a) as f:
        # Skip the first line of file
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

    path =  a.split('ecfp')[0]
    name =  a.split('ecfp')[1].split('_info')[0]
    np.savetxt(path + 'X' + name + '.txt', b, fmt = '%d')
    np.savetxt(path + 'Y' + name + '.txt', log_value, fmt = '%d')
    print len(b), len(log_value)

for a in f_test:
    read1folder(a)

