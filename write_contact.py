import os
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt

rootdir = './DTI_Model_datasets_structures'

#The below is a tedious, but easy understanding of using os to get all the rootdir ecfp files
subfolder = []
for root, dirs, files in os.walk(rootdir):
    a = []
    for name in files:
        if name.endswith(".pdb"):
            a.append(os.path.join(root, name))
    subfolder.append(a)

sub =  subfolder[1:]# The fisrt element of subfolder is [], we need to drop it.
print sub

def OneContact(PDB):
    f = open(PDB[0]) # PDB is a list, thus we need a string which is PDB[0]

    # NO_atom: NO. for each atom, NO_Res: NO. for each Residue (nucleotide or amino-acid)
    NO_atom = []; NO_Res   = []
    x = []; y  = []; z  = []

    # We take the NO.atom, NO.residues, x, y, z from the PDB file
    for line in f.readlines():
        a1 = line.split()[1]
        a5 = line.split()[5]
        a6 = line.split()[6]
        a7 = line.split()[7]
        a8 = line.split()[8]
        NO_atom.append(a1)
        NO_Res.append(a5)
        x.append(a6)
        y.append(a7)
        z.append(a8)

    # To manipulate data easily, convert the list to np.asarray
    NO_atom = np.asarray(NO_atom, dtype = np.int)
    NO_Res  = np.asarray(NO_Res, dtype = np.int)
    x = np.asarray(x, dtype = np.float32)
    y = np.asarray(y, dtype = np.float32)
    z = np.asarray(z, dtype = np.float32)

    # Number of atoms in this PDB file should be the number of rows in this file
    nof_atom = NO_atom.shape[0]

    # Generate a new map for NO. of residues, starting from 1 to nof_Res
    New_NO_Res = np.ones(nof_atom)
    for i in range(1,nof_atom):
        if (NO_Res[i]-NO_Res[i-1]) != 0:
            New_NO_Res[i] = New_NO_Res[i-1] + 1
        else:
            New_NO_Res[i] = New_NO_Res[i-1]

    New_NO_Res = New_NO_Res.astype(int)
    # Number of residues in this PDB file, is the last entry of New_NO_Res
    nof_Res = New_NO_Res[nof_atom-1]

    # The distance matrix has size of nof_Res * nof_Res
    distance = np.zeros((nof_Res,nof_Res))
    distance.fill(100000)

    for i in range(nof_atom):
        for j in range(nof_atom):
            if abs(New_NO_Res[i]-New_NO_Res[j]) < 1:
                continue
            d_ij = ( (x[i]-x[j])**2.0 + (y[i]-y[j])**2.0 + (z[i]-z[j])**2.0 )**0.5
            if d_ij <= distance[New_NO_Res[i]-1][New_NO_Res[j]-1]:
                distance[New_NO_Res[i]-1][New_NO_Res[j]-1] = d_ij

    for i in range(nof_Res):
        distance[i][i] = 0

    # Need a map to match up the old NO. of residues and new NO. of residues
    map = np.column_stack((NO_Res,New_NO_Res))

    # Then we resize the distance to 100X100
    re_distance = cv2.resize(distance, (100,100))

    re_contact = np.zeros((100,100))
    for i in range(100):
        for j in range(100):
            if re_distance[i][j] <= 8:
                re_contact[i][j] = 1

    np.savetxt( PDB[0]+'.contact', list(re_contact[np.triu_indices(100)]) )# return the upper triangle of the contact

    plt.imshow(re_contact);
    plt.colorbar()
    plt.show()

"""
for i in sub:
    OneContact(i)
"""
