##### Uses dataset with feature sets (to be described) #####

import math 
import csv
import os
import sys
import random

# Stores and returns the dataset with only significant features
def read_file(filename):
	
	# Empty structure for dataset
	dataset = {} 
	
	# Open the project dataset file
	with open(filename) as f:
		reader = csv.reader(f)
		i = 1
		# For every instance in dataset
		for line in reader:	
			# Store all the feature values of the instance
			dataset.update({i : line})
			i += 1

	# Return the stored dataset
	return dataset

def write_file(new_filename, new_data):
	
	# Store the selected features in another file
	with open(new_filename, 'a') as outfile:
		writer = csv.writer(outfile)

		for i in new_data.keys():
			writer.writerow(new_data[i])

def program_size(dataset):
	# Set 1: features 1 to 49
	set_1 = {}
	for j in range(0, 49):
		for i in dataset.keys():
			if j+1 not in set_1.keys():
				set_1.update({j+1: [dataset[i][j]]})

			else:
				set_1[j+1].append(dataset[i][j])
	
	set_1.update({0: []})
	for i in dataset.keys():
		set_1[0].append(dataset[i][-1])

	# print(len(set_1))
	return set_1

def mccabe_complexity(dataset):
	# Set 2: features 50 to 67
	set_2 = {}
	for j in range(49, 67):
		for i in dataset.keys():
			if j+1 not in set_2.keys():
				set_2.update({j+1: [dataset[i][j]]})

			else:
				set_2[j+1].append(dataset[i][j])

	set_2.update({0: []})
	for i in dataset.keys():
		set_2[0].append(dataset[i][-1])

	# print(len(set_2))
	return set_2

def halstead(dataset):
	# Set 3: features 68 to 76
	set_3 = {}
	for j in range(67, 76):
		for i in dataset.keys():
			if j+1 not in set_3.keys():
				set_3.update({j+1: [dataset[i][j]]})

			else:
				set_3[j+1].append(dataset[i][j])

	set_3.update({0: []})
	for i in dataset.keys():
		set_3[0].append(dataset[i][-1])

	# print(len(set_3))
	return set_3

def aging_related(dataset):
	# Set 4: features 77 to 82
	set_4 = {}
	for j in range(76, 82):
		for i in dataset.keys():
			if j+1 not in set_4.keys():
				set_4.update({j+1: [dataset[i][j]]})

			else:
				set_4[j+1].append(dataset[i][j])

	set_4.update({0: []})
	for i in dataset.keys():
		set_4[0].append(dataset[i][-1])

	# print(len(set_4))
	return set_4

def significant(dataset, k, results):

	set_5 = {}

	# Open the project dataset file
	with open(results) as f:
		reader = csv.reader(f)
		p = 0
		for line in reader:
			if p == k-1:
				for j in range(0, len(line)):
					if line[j] == '1':
						for i in dataset.keys():
							if j+1 not in set_5.keys():
								set_5.update({j+1: [dataset[i][j]]})
							else:
								set_5[j+1].append(dataset[i][j])
				break
			p += 1

	set_5.update({0: []})
	for i in dataset.keys():
		set_5[0].append(dataset[i][-1])

	# print(len(set_5))
	return set_5

def correlation(dataset, k, results):
	
	set_6 = {}

	# Open the project dataset file
	with open(results) as f:
		reader = csv.reader(f)
		p = 0
		for line in reader:
			if p == k-1:
				for j in range(0, len(line)):
					if line[j] == '1':
						for i in dataset.keys():
							if j+1 not in set_6.keys():
								set_6.update({j+1: [dataset[i][j]]})
							else:
								set_6[j+1].append(dataset[i][j])
				break
			p += 1

	set_6.update({0: []})
	for i in dataset.keys():
		set_6[0].append(dataset[i][-1])

	# print(len(set_6))
	return set_6	

def invert(dataset):

	set_7 = {}
	for j in range(0, 82):
		for i in dataset.keys():
			if j+1 not in set_7.keys():
				set_7.update({j+1: [dataset[i][j]]})

			else:
				set_7[j+1].append(dataset[i][j])

	set_7.update({0: []})
	for i in dataset.keys():
		set_7[0].append(dataset[i][-1])

	# print(len(set_7))
	return set_7
