import os
import numpy as np
import pandas as pd

rootdir = './DTI_Model_datasets_structures'

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
    if a[0].split('/')[-1][0:4] == "ecfp": # Determine which file is ecfp for drug.
        drug_file = a[0]
        protein_file = a[1] # The other one is file for protein/pocket
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
    df['Y'] = pd.Series(df['new_value']<=10)
    
    df_sort = df.sort_values('new_value')
    
    # '(df['Y']==True).sum()' will gives the number of compounds that have measurement values less that 100
    df_sort_Y = df_sort[:(df['Y']==True).sum()] # Pick all positive drugs
    df_sort_N = df_sort[(df['Y']==True).sum():].sample(n=(df['Y']==True).sum())# randomly select the same amount of negative drugs
    df_sort_YN = pd.concat([df_sort_Y,df_sort_N])
    
    """"
        Then, read the proetin sequence descriptor
    """
    descriptor = []
    with open(protein_file) as f2:
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

    """
    df_sort_YN is the data frame that has equal number of positive and negative drugs, with ecfp and protein descriptor
    """
    df_sort_YN['protein'] = protein

    path = drug_file.split('ecfp')[0]
    name = drug_file.split('ecfp')[1]
    
    df_sort_YN.to_csv(path+'test'+name )

for i in range(len(sub)):
    read1folder(sub[i])
