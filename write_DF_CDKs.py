import os
import numpy as np
import pandas as pd

rootdir = './CDK_datasets'

#The below is a tedious, but easy understanding of using os to get all the rootdir ecfp files
subfolder = []
for root, dirs, files in os.walk(rootdir):
    a = []
    for name in files:
        if name.startswith("id_df"):
            a.append(os.path.join(root, name))
    subfolder.append(a)

sub =  subfolder[1:]# The fisrt element of subfolder is [], we need to drop it.
print sub

def read1folder(a):
    df = pd.DataFrame.from_csv(a[0])
    CHEMBL_id = a[0].split('/')[2].split('-')[0]
    df2 = df.loc[:,['compound','new_value']]
    df2.set_index('compound',inplace = True)
    df2.rename(columns={'new_value': CHEMBL_id,}, inplace = True)
    return list(df['compound']), df2

drug_pool = []
DF = pd.DataFrame()
total_count = 0
for a in sub:
    tmp = pd.DataFrame()
    sub_pool, tmp = read1folder(a)
    DF = pd.concat([DF, tmp], axis=1)
    total_count = total_count + len(sub_pool)
    print len(sub_pool)
    for id in sub_pool:
        if id not in drug_pool:
            drug_pool.append(id)

print len(drug_pool), total_count
DF.to_csv('DF_for_CDKs.csv')

