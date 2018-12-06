##### Creates the 5-fold cross validation datasets and runs all classification models #####

import os
import sys
import csv
from sklearn.model_selection import KFold
from numpy import array

import feature_sets
import model1
import model2
import model3
import model4
import model5
import model6
import model7

directory = "../data"

# Converts dataset into form usable by classifiers
def make_list(dataset, size):

	data = []
	# print(size)
	for j in range(0, size):
		v = []
		# print(j+1)
		for i in sorted(dataset.keys()):
			# print(i)
			# if i != 0:
			v.append(float(dataset[i][j]))

		# if float(dataset[0][j]) != 0 and float(dataset[0][j]) != 1:
		# 	print('ERROR')
		# v.append(float(dataset[0][j]))
		# v.insert(0, float(dataset[0][j]))
		data.append(v)

	# print(len(data))
	# print(len(data[0]))
	n_data = array(data)
	return n_data

def main():

	##### Original Data #####
	# Directory particular balanced dataset indicated by command line arg
	data_dir = os.path.join(directory, sys.argv[1])

	# For each project
	for k in range(1, 8):
		# Read files and get the data
		filepath = os.path.join(data_dir, str(k)+'_'+sys.argv[1]+'.csv')
		print(filepath)

		# Store data points of only signficant features
		dataset = feature_sets.read_file(filepath)

		size = len(dataset)

		# File containing the results of significance test
		sig = os.path.join(data_dir, sys.argv[1]+'_sig_results.csv')
		# File containing the results of Pearson test
		pcc = os.path.join(data_dir, sys.argv[1]+'_pcc_results.csv')

		# Feature set 1
		f1 = feature_sets.program_size(dataset)
		# Feature set 2
		f2 = feature_sets.mccabe_complexity(dataset)
		# Feature set 3
		f3 = feature_sets.halstead(dataset)
		# Feature set 4
		f4 = feature_sets.aging_related(dataset)
		# Feature set 5
		f5 = feature_sets.significant(dataset, k, sig)
		# Feature set 6
		f6 = feature_sets.correlation(dataset, k, pcc)
		# Feature set 7
		f7 = feature_sets.invert(dataset)

		# combine all 7 feature sets data into one list
		all_sets = [f1, f2, f3, f4, f5, f6, f7]

		# For each feature set d
		for d in range(len(all_sets)):
			print('* '+str(len(all_sets[d])))
			# for s in all_sets[d].keys():
			# 	print('\t'+str(len(all_sets[d][s])))
			print("\t----- Feature set: "+str(d+1))

			# Convert the dataset into a form usable by the classifiers
			data = make_list(all_sets[d], size)
			
			# m = [x[-1] for x in data]
			# print(len(m))

			# prepare 5-fold cross validation
			kfold = KFold(5, True, 1)
			
			# enumerate splits	
			j = 1
			for train, test in kfold.split(data):
				# print('train: %s, test: %s' % (len(data[train]), len(data[test])))

				print('\t\tFold: '+str(j))
				j+=1 # increment split number

				# Run each of the seven classifiers on the current split fold
				model1.run_model(data[train], data[test])
				model2.run_model(data[train], data[test])
				model3.run_model(data[train], data[test])
				model4.run_model(data[train], data[test])
				model5.run_model(data[train], data[test])
				# model6.run_model(data[train], data[test])
				model7.run_model(data[train], data[test])

	
	##### Up-sampled Data #####
	# Directory particular balanced dataset indicated by command line arg
	data_dir = os.path.join(directory, sys.argv[2])

	# For each project
	for k in range(1, 8):
		# Read files and get the data
		filepath = os.path.join(data_dir, str(k)+'_'+sys.argv[2]+'.csv')
		print(filepath)

		# Store data points of only signficant features
		dataset = feature_sets.read_file(filepath)

		size = len(dataset)

		# File containing the results of significance test
		sig = os.path.join(data_dir, sys.argv[2]+'_sig_results.csv')

		# File containing the results of Pearson test
		pcc = os.path.join(data_dir, sys.argv[2]+'_pcc_results.csv')

		# Feature set 1
		f1 = feature_sets.program_size(dataset)
		# Feature set 2
		f2 = feature_sets.mccabe_complexity(dataset)
		# Feature set 3
		f3 = feature_sets.halstead(dataset)
		# Feature set 4
		f4 = feature_sets.aging_related(dataset)
		# Feature set 5
		f5 = feature_sets.significant(dataset, k, sig)
		# Feature set 6
		f6 = feature_sets.correlation(dataset, k, pcc)
		# Feature set 7
		f7 = feature_sets.invert(dataset)

		# combine all 7 feature sets data into one list
		all_sets = [f1, f2, f3, f4, f5, f6, f7]

		# For each feature set d
		for d in range(len(all_sets)):
			# print('* '+str(len(all_sets[d])))
			# for s in all_sets[d].keys():
			# 	print('\t'+str(len(all_sets[d][s])))
			
			# Convert the dataset into a form usable by the classifiers
			data = make_list(all_sets[d], size)


			# prepare 5-fold cross validation
			kfold = KFold(5, True, 1)
			
			# enumerate splits	
			for train, test in kfold.split(data):
				# print('train: %s, test: %s' % (len(data[train]), len(data[test])))

				# Run each of the seven classifiers on the current split fold
				model1.run_model(data[train], data[test])
				model2.run_model(data[train], data[test])
				model3.run_model(data[train], data[test])
				model4.run_model(data[train], data[test])
				model5.run_model(data[train], data[test])
				model6.run_model(data[train], data[test])
				model7.run_model(data[train], data[test])



if __name__ == '__main__':
	main()



