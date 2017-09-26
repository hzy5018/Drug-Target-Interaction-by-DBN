import numpy as np
import tensorflow as tf

np.random.seed(1337)  # for reproducibility
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics.classification import accuracy_score

from dbn.tensorflow import SupervisedDBNClassification
# use "from dbn import SupervisedDBNClassification" for computations on CPU with numpy

# Loading dataset
X = np.loadtxt('X.txt')
Y = np.loadtxt('L.txt')

# Data scaling

# Splitting data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

# Training
classifier = SupervisedDBNClassification(hidden_layers_structure=[2000, 2000],
										learning_rate_rbm=0.01,
										learning_rate=0.01,
										n_epochs_rbm=10,
										n_iter_backprop=1000,
										batch_size=32,
										activation_function='relu',
										dropout_p=0.2)
classifier.fit(X_train, Y_train)

# Save the model
classifier.save('model.pkl')

# Restore it
classifier = SupervisedDBNClassification.load('model.pkl')

# Test
Y_pred = classifier.predict(X_test)
print('Done.\nAccuracy: %f' % accuracy_score(Y_test, Y_pred))

