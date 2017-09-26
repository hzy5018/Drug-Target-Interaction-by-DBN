import os
import numpy as np
import pandas as pd

rootdir = './DTI_Model_datasets_structures'

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
