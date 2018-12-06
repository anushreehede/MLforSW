### Script to read performance values and create meaningful result tables ###

import xlrd
import statistics 
import numpy as np
import csv
import math 

def read_file(filename):

	wb = xlrd.open_workbook(filename) 
	sheet_accuracy = wb.sheet_by_index(0) 
	sheet_auc = wb.sheet_by_index(1)

	accuracy = []
	for i in range(sheet_accuracy.nrows):
		accuracy.append(sheet_accuracy.row_values(i))

	auc = []
	for i in range(sheet_auc.nrows):
		auc.append(sheet_auc.row_values(i))
	
	return accuracy, auc

def feature_sets(performance, project):
	# performance is the matrix of values (70x49)
	# project is the project number 

	sets = {}

	# select all the rows representing the particular project
	# original and up_sampled data 
	part = performance[project*5: (project*5) + 5] + performance[(project*5) + 35: (project*5) + 40]

	# for each of the 7 feature sets
	for i in range(7):
		# initialize an entry in the dictionary
		sets.update({i+1: []})
		
		# for each of the selected rows select only the portion 
		# containing values for feature set number i
		# and add to the dictionary entry
		for j in range(len(part)):
			sets[i+1].append(part[j][i*7: (i*7)+7])

	return sets

def sampling_techniques(performance):

	sets = {}
	# for each project
	for i in range(7):
		original = performance[i*5: (i*5) + 5]
		up_sampled = performance[(i*5) + 35: (i*5) + 40]
		project = {"original": original, "up_sampled": up_sampled}

		sets.update({i+1: project})

	return sets

def classifiers(performance, project):

	sets = {}

	# select all the rows representing the particular project
	# original and up_sampled data 
	part = performance[project*5: (project*5) + 5] + performance[(project*5) + 35: (project*5) + 40]
	
	# for every classifier
	for i in range(7):

		# initialize an entry in the dictionary
		sets.update({i+1: []})

		# make a list for every classifier
		class_list = []
		# for each of the selected rows
		for j in range(len(part)):
			# make a list
			cur_fold = []

			# for every selection technique, select the value 
			# corresponding to classifier i and add to above list
			for k in range(7):
				cur_fold.append(part[j][(k*7)+i])

			# add above obtained list to the classifier list 
			# containing values for all selected words
			class_list.append(cur_fold)

		# add the classifier list to the dictionary of classifiers
		sets[i+1] = class_list

	return sets

def print_results(result, which_stat):
	print(which_stat)
	if which_stat == "sampling":
		# for each project
		for project in range(7):
			print("Project: "+str(project+1))
			# for each sampling technique
			for technique in result[project+1].keys():
				print("\tTechnique: "+technique)
				for c in range(len(result[project+1][technique])):
					print(result[project+1][technique][c])
	else: 
		# for each project
		for project in range(7):
			print("Project: "+str(project+1))
			# for each of the technique (sampling, feature selection, classification)
			for technique in range(len(result[project+1])):
				print("\tTechnique: "+str(technique+1))
				for c in range(len(result[project+1][technique+1])):
					print(result[project+1][technique+1][c])

# Returns the list of AUC values with respect to each technique
def get_list(result, which_stat):
	
	if which_stat == "sampling":
		# Stores the lists
		values = {"original": [], "up_sampled": []}
		
		# For each sampling technique
		for tech in values.keys():
			# for each project
			for project in range(7):
				# print("Project: "+str(project+1))
				
				# Get results of the current sampling technique
				technique = result[project+1][tech]

				for c in range(len(technique)):
					# print(result[project+1][technique][c])

					for i in range(len(technique[c])):
						values[tech].append(technique[c][i])

		print(which_stat+str(len(values["original"])))

	elif which_stat == "classifiers":
		# Stores the lists
		values = {}

		# For each classifier
		for classifier in range(7):
			values.update({classifier+1: []})
			# for each project
			for project in range(7):
				# print("Project: "+str(project+1))
				
				# Get results of the current classifier
				technique = result[project+1][classifier+1]
				for c in range(len(technique)):
					# print(result[project+1][technique+1][c])

					for i in range(len(technique[c])):
						values[classifier+1].append(technique[c][i])
		print(which_stat+str(len(values[1])))
		

	else:
		# Stores the lists
		values = {}

		# For each feature selection technique
		for fs_tech in range(7):
			values.update({fs_tech+1: []})
			# for each project
			for project in range(7):
				# print("Project: "+str(project+1))
				
				# Get the results of the current feature selection technique
				technique = result[project+1][fs_tech+1]
				for c in range(len(technique)):
					# print(result[project+1][technique+1][c])

					for i in range(len(technique[c])):
						values[fs_tech+1].append(technique[c][i])

		print(which_stat+str(len(values[1])))
	return values

# Returns the statistics for a set of techniques as a CSV file
def get_statistics(table, filename):

	# Open file
	with open(filename, 'a') as outfile:
		writer = csv.writer(outfile)

		# For each technique in the set
		for technique in sorted(table.keys()):
			# print(len(table[technique]))

			# Replace any NaN with 0
			table[technique] = [0 if val == 'NaN' else val for val in table[technique]]
			print(len(table[technique]))
			# Minimum
			minimum = min(table[technique])
			# Maximum
			maximum = max(table[technique])
			# Mean
			mean = sum(table[technique])/len(table[technique])
			# Standard Deviation
			std_dev = statistics.stdev(table[technique])
			# Median
			median = statistics.median(table[technique])
			# 25th and 75th percentile
			arr = np.array(table[technique])
			q1 = np.percentile(arr, 25)
			q3 = np.percentile(arr, 75)
			
			# Store as a row in the CSV file
			values = [minimum, maximum, mean, median, std_dev, q1, q3]
			writer.writerow(values)

# Get the PCC value between two features
def get_pcc_value(f1, f2):
	# Mean of values of f1
	x_mean = sum(f1)/len(f1)
	# Mean of values of f2
	y_mean = sum(f2)/len(f2)

	# Numerator of PCC
	num = sum([(f1[i]-x_mean)*(f2[i]-y_mean) for i in range(len(f1))])
	# Denominator of PCC
	den = math.sqrt(sum([(f1[i]-x_mean)**2 for i in range(len(f1))])) * math.sqrt(sum([(f2[i]-y_mean)**2 for i in range(len(f2))]))
	# PCC value
	pcc = num/den;

	# Print and return
	return pcc	

# Get the similarity between twp techniques using PCC, store in CSV file
def get_similarity(table, filename, which_stat):
	
	# Open file
	with open(filename, 'a') as outfile:
		writer = csv.writer(outfile)
		if which_stat == "sampling":

			# Get PCC value and store 
			pcc = get_pcc_value(table["original"], table["up_sampled"])

			line = [1, pcc]
			writer.writerow(line)
			line = [pcc, 1]
			writer.writerow(line)

		else:
			# For each technique
			for i in range(7):
				line = []
				# Get a pair for the technique
				for j in range(7):
					# Find their PCC value and store it
					pcc = get_pcc_value(table[i+1], table[j+1])
					line.append(pcc)
				writer.writerow(line)

def main():

	# Read the performance file (containing results of 3430 datasets)
	accuracy, auc = read_file("../data/performance.xlsx")
	# print(accuracy)
	# print(auc)

	accuracy_feature_sets = {}
	auc_feature_sets = {}
	
	accuracy_classifiers = {}
	auc_classifiers = {}

	# for each project: 1 to 7
	for i in range(7):
		
		# Accuracy results wrt all feature sets
		sets_1 = feature_sets(accuracy, i)
		accuracy_feature_sets.update({i+1: sets_1})
		# Area Under Curve results wrt all feature sets
		sets_2 = feature_sets(auc, i)
		auc_feature_sets.update({i+1: sets_2})

		# print(accuracy_feature_sets)
		# print(auc_feature_sets)

		# Accuracy results wrt all classifiers
		sets_3 = classifiers(accuracy, i)
		accuracy_classifiers.update({i+1: sets_3})
		# AUC results wrt all classifiers
		sets_4 = classifiers(auc, i)
		auc_classifiers.update({i+1: sets_4})

		# print(accuracy_classifiers)

		# print(auc_classifiers)

	# Accuracy results wrt all sampling techniques
	accuracy_sampling = sampling_techniques(accuracy)
	# AUC results wrt all sampling techniques
	auc_sampling = sampling_techniques(auc)

	# print(accuracy_sampling)
	# print(auc_sampling)

	# print_results(accuracy_feature_sets, "feature_sets")
	# print_results(accuracy_classifiers, "classifiers")
	# print_sampling(accuracy_sampling, "sampling")

	# List all AUC values for each feature set
	values_feature_sets = get_list(auc_feature_sets, "feature_sets")
	# List all AUC values for each classifier
	values_classifiers = get_list(auc_classifiers, "classifiers")
	# List all AUC values for each sampling technique
	values_sampling = get_list(auc_sampling, "sampling")

	desc_feature_sets = "../data/desc_feature_sets.csv"
	sim_feature_sets = "../data/sim_feature_sets.csv"
	# Get descriptive statistics for all feature sets
	get_statistics(values_feature_sets, desc_feature_sets)
	# Get relative comparisons for all feature sets
	get_similarity(values_feature_sets, sim_feature_sets, "feature_sets")

	desc_classifiers = "../data/desc_classifiers.csv"
	sim_classifiers = "../data/sim_classifiers.csv"
	# Get descriptive statistics for all classifiers
	get_statistics(values_classifiers, desc_classifiers)
	# Get relative comparisons for all classifiers 
	get_similarity(values_classifiers, sim_classifiers, "classifiers")

	desc_sampling = "../data/desc_sampling.csv"
	sim_sampling = "../data/sim_sampling.csv"
	# Get descriptive statistics for all sampling techniques
	get_statistics(values_sampling, desc_sampling)
	# Get relative comparisons for all sampling techniques
	get_similarity(values_sampling, sim_sampling, "sampling")


if __name__ == "__main__":
	main()