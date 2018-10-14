### Performs the Pearson Correlation Coefficient test to return the set of uncorrelated features ###

import math 
import csv
import os
import sys
import random
from string import ascii_lowercase

# Dataset directory
directory = "../data"

# List of sub file names
alpha = []
for c in ascii_lowercase:
	if c == 'k':
		break
	alpha.append(c)


# Returns the Pearson Correlation Coefficient 
# for two features f1 and f2 in dataset 
def get_pearson_correlation(f1, f2, dataset):

	# Mean of values of f1
	x_mean = sum(dataset[f1])/len(dataset[f1])
	# Mean of values of f2
	y_mean = sum(dataset[f2])/len(dataset[f2])

	# Numerator of PCC
	num = sum([(dataset[f1][i]-x_mean)*(dataset[f2][i]-y_mean) for i in range(len(dataset[f1]))])
	# Denominator of PCC
	den = math.sqrt(sum([(dataset[f1][i]-x_mean)**2 for i in range(len(dataset[f1]))])) * math.sqrt(sum([(dataset[f2][i]-y_mean)**2 for i in range(len(dataset[f2]))]))
	# PCC value
	pcc = num/den;

	# Print and return
	return pcc	

# Stores and returns the dataset with only significant features
def read_file(filename, significant):
	
	# Empty structure for dataset
	dataset = {} 
	# List of target values
	target = []

	# Open the project dataset file
	with open(filename) as f:
		reader = csv.reader(f)
		
		# For every instance in dataset
		for line in reader:	
			# Loop through list of significant features
			# and store only data values under those features
			for i in range(len(significant)):
				if significant[i] == '1':
					if i+1 not in dataset.keys():
						dataset.update({i+1: [float(line[i])]})
					else:
						dataset[i+1].append(float(line[i]))

			# Store the target attribute values in a list
			target.append(float(line[-1]))

	# Append the target attribute list to dataset, giving it feature number 0
	dataset.update({0: target})

	# Return the stored dataset
	return dataset			

def main():

	# Directory particular balanced dataset indicated by command line arg
	data_dir = os.path.join(directory, sys.argv[1])

	# File containing the results of significance test
	results = os.path.join(data_dir, sys.argv[1]+'_sig_results.csv')
	
	# Open file containing the significant features of each project
	with open(results) as f:
		reader = csv.reader(f)
		k = 1 # Counter for projects

		# Iterate over each line corresponding to each project
		for line in reader:

			# Get any one dataset out of the 10 
			r = random.choice(alpha)

			# Create the filepath
			filepath = os.path.join(data_dir, 'files/'+str(k)+'_'+sys.argv[1]+'_'+r+'.csv')
			print('\t\t'+filepath)
			# filepath = "mini.csv"

			# Store data points of only signficant features
			dataset = read_file(filepath, line)
			# print(dataset)

			# Matrix containing Pearson CC values
			pearson_values = {}
			# Correlation feature list 
			flags = {}

			# All significant features are selected
			for i in range(len(line)):
				if line[i] == '1':
					flags.update({i+1: 1})

			# For every feature i
			for i in dataset.keys():
				# Except for target attribute
				if i != 0:
					# Create an empty row in the PCC matrix
					pearson_values.update({i: []})

					# For every feature j
					for j in dataset.keys():
						# Except for target attribute
						if j != 0:

							# If no feature is unselected
							if flags[i] and flags[j]:

								# Get the PCC value for features i and j
								pcc = get_pearson_correlation(i, j, dataset)
								# Add it to the PCC matrix
								pearson_values[i].append(pcc)
								# print('\nfeatures: '+str(i)+' and '+str(j))
								
								# If the features are highly correlated,
								# One of them must be dropped
								if i != j and (pcc >= 0.7 or pcc <= -0.7):

									# Get the PCC values of the features wrt the target attribute
									pcc1 = get_pearson_correlation(i, 0, dataset)
									pcc2 = get_pearson_correlation(j, 0, dataset)

									# Feature selection
									if pcc1 > pcc2:
										# print('choosing feature '+str(i))
										flags[j] = 0
									else:
										# print('choosing feature '+str(j))
										flags[i] = 0
			
			# Increment project counter
			k += 1

			# Print the list of significant features with low correlation
			selects = [i for i in flags.keys() if flags[i] == 1]
			print('\nselected feature list: ')
			print(selects)

			# Store the selected features in another file
			new_filename = os.path.join(data_dir, sys.argv[1]+'_pcc_results.csv')
			with open(new_filename, 'a') as outfile:
				writer = csv.writer(outfile)

				values = []
				for i in range(1, len(line)+1):
					if i in selects:
						values.append(1)
					else:
						values.append(0)
				
				writer.writerow(values)


if __name__ == '__main__':
	main()
