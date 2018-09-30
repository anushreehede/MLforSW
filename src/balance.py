# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

import os
import csv
import numpy as np

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE

from sklearn import model_selection
from sklearn.ensemble import AdaBoostClassifier

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

print(__doc__)

RANDOM_STATE = 42
seed = 7

# Datset directory
main_dir = "../RefactDataSetValidated"

### Reads the dataset file and extracts the training examples
def read_file(filename):
	
	# Feature value list
	feature_values = []
	# Target value list
	target_values = []
	# Number of minority class examples
	minor = 0
	with open(filename) as f:
		x = f.readline()
		reader = csv.reader(f)
		for line in reader:	
			# Get the feature values
			metrics = line[10:94]
			target = line[94]

			# Count number of minority class examples
			if target != '0':
				minor += 1
				target = '1'

			# Store the training example in list
			feature_values.append(metrics)
			target_values.append(target)

	# Return the final training set lists
	return np.array(feature_values).astype(np.float), np.array(target_values).astype(np.float), minor	

### Runs Gaussian Naive Bayes Classifier on the training data
### and tests with the test data for miclassification
def run_Gaussian_NB(X, y):

	# Split the training and test dataset 0.25 goes for test
	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_STATE)
	
	# print(str(len(X_train))+','+str(len(X_test)))
	
	# Instantiate Naive Bayes Classifier and fit the training data to the model
	gnb = GaussianNB()
	gnb.fit(
	    X_train,
	    y_train
	)
	y_pred = gnb.predict(X_test)
	# print(X_test.shape[0])
	
	# Print results for misclassification and accuracy
	print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%"
	      .format(
	          X_test.shape[0],
	          (y_test != y_pred).sum(),
	          100*(1-(y_test != y_pred).sum()/X_test.shape[0])
	))

### Runs C4.5 Decision Tree Classifier on the training data
### and tests with the test data for miclassification
def run_decision_tree(X, y):

	# Split the training and test dataset 0.25 goes for test
	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=RANDOM_STATE)

	# Instantiate C4.5 decision tree Classifier and fit the training data to the model
	dt = DecisionTreeClassifier(min_samples_split=5, random_state=99)
	dt.fit(X_train, y_train)
	y_pred = dt.predict(X_test)

	# Print results for misclassification and accuracy
	print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%"
	      .format(
	          X_test.shape[0],
	          (y_test != y_pred).sum(),
	          100*(1-(y_test != y_pred).sum()/X_test.shape[0])
	))

### Main method
def main():

	# Find the dataset csv file
	for directory in os.listdir(main_dir):
		directory_path = os.path.join(main_dir, directory)
		for outer_dir in os.listdir(directory_path):
			outer_dir_path = os.path.join(directory_path, outer_dir)
			filename = os.path.join(outer_dir_path,directory+"-Method.csv")
			print('\n\t\t\t'+filename)

			# Obtain dataset from file
			data, target, minor = read_file(filename)
			# print(data.dtype)
			# print(target)

		# Run NB classfier on raw data
			print('No balancing: Naive Bayes')
			run_Gaussian_NB(data, target)
		# Run DT classfier on raw data
			print('\nNo Balancing: Decision Tree')
			run_decision_tree(data, target)

		# 1. Random Undersampling
			# Get the new undersampled size for the majority class
			ratio = round((len(data) - minor)*0.1)
			# print(str(len(data)-minor)+','+str(ratio))
			# print(minor)

			# Fit the training data for the undersampled size and get new resampled training set
			rus = RandomUnderSampler(random_state=RANDOM_STATE, ratio={0: ratio})
			rus.fit(data, target)
			X_resampled, y_resampled = rus.sample(data, target)
			# print(str(len(X_resampled)))

			print('\nRandom Undersampling: Naive Bayes')
			# Run NB classifier on undersampled data
			run_Gaussian_NB(X_resampled, y_resampled)
			print('\nRandom Undersampling: Decision Tree')
			# Run DT classfier on raw data
			run_decision_tree(X_resampled, y_resampled)

		# 2. SMOTE 
			# Fit the training data using SMOTE and create the new training set
			smote = SMOTE(k_neighbors=2)
			X_sm, y_sm = smote.fit_sample(data, target)
			# print(str(len(X_sm))+','+str(len(data)))

			print('\nSMOTE: Naive Bayes')
			# Run NB classifier on the new dataset
			run_Gaussian_NB(X_sm, y_sm)
			print('\nSMOTE: Decision Tree')
			# Run DT classfier on raw data
			run_decision_tree(X_sm, y_sm)

		# 3. AdaBoost
			# Number of classifiers for AdaBoost
			num_trees = 30

			# K fold cross validation (with 10 splits)
			kfold = model_selection.KFold(n_splits=10, random_state=seed)

			# Define the AdaBoost classifier model
			model = AdaBoostClassifier(n_estimators=num_trees, random_state=seed)

			# Fit the training data using AdaBoost  
			results = model_selection.cross_val_score(model, data, target, cv=kfold)

			print('\nAdaBoost Classifier with 30 trees')
			print(results.mean()*100)




if __name__ == "__main__":
	main()
