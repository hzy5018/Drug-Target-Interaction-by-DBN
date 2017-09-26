# DBN-Drug-Target-Interaction
- A tensorflow implementation of modified DeepDTI(http://pubs.acs.org/doi/abs/10.1021/acs.jproteome.6b00618). Besides using Protein Sequence Composition as the descriptors for proteins(described in paper), we add the contact maps(for proteins with structures) and DI scores(for those without structures) as additional descriptors for proteins, which include some long range information  between amino acids in the proteins.
- Instead of using the data from DrugBank, we extract data from CHEMBL for testing the model.
## Reference
- Deep-Learning-Based Drug–Target Interaction Prediction, Ming Wen, Zhimin Zhang, Shaoyu Niu, Haozhi Sha, Ruihan Yang, Yonghuan Yun, and Hongmei Lu, J. Proteome Res., 2017, 16 (4), pp 1401–1409
- A Python implementation of Deep Belief Networks built upon NumPy and TensorFlow with scikit-learn compatibility, albertbup, 2017
