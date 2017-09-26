import os
import numpy as np
import pandas as pd

# Step 1:
rootdir = './smart_drug_protein_testsets'

#The below is a tedious, but easy understanding of using os to get all the rootdir ecfp files
subfolder = []
for root, dirs, files in os.walk(rootdir):
    a = []
    for name in files:
        if name.startswith("ecfp") or name.startswith("ProtrWeb"):
            a.append(os.path.join(root, name))
    subfolder.append(a)

sub =  subfolder[1:]# The fisrt element of subfolder is [], we need to drop it.
print sub

"""
    'read1folder' is the function to read ONE folder with [1]ecfp and [2]protein sequence files
"""
def read1folder(a):
    
    """
        First, read the ecfp file
    """
    target = []
    canonical_smiles = []
    ecfp = []
    measurement_value = []
    new_value = []
    measurement_type = []
    with open(a[0]) as f:
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
    
    
    """"
        Then, read the proetin sequence descriptor
    """
    descriptor = []
    with open(a[1]) as f2:
        # skip the first line of file
        next(f2)
        for line in f2:
            one_line = line.split(',')
            descriptor = one_line[1:] # Drop the first element which is the name of protein.

    protein = ''
    for i in range(len(descriptor)):
        if float(descriptor[i])>0:
            protein = protein + '1'
        if float(descriptor[i])==0:
            protein = protein + '0'


    df['protein'] = protein
    
    path = a[0].split('ecfp')[0]
    name = a[0].split('ecfp')[1]
    
    df.to_csv(path+'test'+name )

for i in range(len(sub)):
    read1folder(sub[i])

# Step 2:
f_test =  [os.path.join(root, name)
           for root, dirs, files in os.walk(rootdir)
           for name in files
           if name.startswith("test")]

print f_test

def OneTest(a):
    DrugAndProtein = []
    df = pd.read_csv(a)
    if df.empty:# check if the dataframe is empty due to the new_value cutoff
        print a+' is empty'
        return [],[]
    else:
        ecfp = list(df['ecfp'])
        protein = list(df['protein'])[0]
        Y = list(df['Y'])
        Y0 = [0]*len(Y)
        for i in range(len(Y)):
            if Y[i] == True:
                Y0[i] = 1

        for i in range(len(ecfp)):
            DrugAndProtein.append(ecfp[i]+protein)
        
        b = []
        for i in DrugAndProtein:
            a = []
            for n in i:
                a.append(int(n))
            b.append(a)
        
        return b, Y0 # 'b' is the combined descriptor for drug and protein, 'Y0' is the labels.

X = []
L = []
for test in f_test:
    [a,b] = OneTest(test)
    X = X + a
    L = L + b

np.savetxt('X.txt', X, fmt = '%d')
np.savetxt('L.txt', L, fmt = '%d')
