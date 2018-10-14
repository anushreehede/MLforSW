### Creating similar instances of minority class ###

import math
import os
import random
import csv 

# Datset directory
directory = "../data"

def get_intervals(metric_dict, index):
	
	# Get the values of the metrics for each method belonging to buggy class
	values = [float(metric_dict[k][index]) for k in metric_dict.keys()]
	# Find the mean of those values
	mean = sum(values)/len(metric_dict)

	# Find the standard deviation of the values
	add_sq_sum = 0
	for k in metric_dict.keys():
		add_sq_sum += ((float(metric_dict[k][index]) - mean)**2)
	std_dev = math.sqrt(add_sq_sum/len(metric_dict))

	# Find the 95% CI assuming normal distribution of the values
	val = 1.96*std_dev/math.sqrt(len(metric_dict))
	lower = mean - val
	upper = mean + val 

	return lower, upper

# Read the dataset files and store separately based on two classes
def read_file(filename):
	
	i = 0 # instance number
	f_num = 0 # number of features 

	# Structures to store instances of same class together
	buggy = {} 
	not_buggy = {}
	
	# Open the project dataset file
	with open(filename) as f:
		reader = csv.reader(f)
		
		# For every instance in dataset
		for instance in reader:	
			
			if instance[-1] != '0':
				buggy.update({i : instance})
			else:
				not_buggy.update({i : instance})

			if f_num == 0:
				f_num = len(instance)

			i += 1

	return buggy, not_buggy, f_num

def main():

	# Directory containing the original dataset
	new_dir = os.path.join(directory, 'original')

	# Iterate through each of the 7 project files
	for k in range(1, 8):
		filename = os.path.join(new_dir, str(k)+'_original.csv')
		print('\n\t\t\t'+filename)

		# Read files and get the data
		buggy, not_buggy, feature_num = read_file(filename)
		print(str(len(buggy))+','+str(len(not_buggy))+","+str((float)(len(not_buggy))/((len(not_buggy))+len(buggy)) * 100))

		# Get the number of artificial instances to be generated
		num_artificial_instances = len(not_buggy) - len(buggy)

		# Instantiate structure to store the artificial instances
		artifical = {}
		count = 0
		for i in range(num_artificial_instances):
			count += 1
			artifical.update({count: []})

		# For every feature 
		for i in range(feature_num):

			# Get the confidence interval for the minority class
			lower, upper = get_intervals(buggy, i)

			# Create num_artificial_instances random values in range (lower, upper)
			# Store them in a list feature_values
			feature_values = []
			for j in range(num_artificial_instances):
				feature_values.append(random.uniform(lower, upper))

			for j in range(num_artificial_instances):
				artifical[j+1].append(feature_values[j])

		print('not buggy: '+str(len(not_buggy))+' buggy: '+str(len(buggy)+len(artifical)))

		# Store the new dataset in a new file
		new_filename = os.path.join(directory+'/up_sampled', str(k)+'_up_sampled.csv')
		with open(new_filename, 'w') as f:
			writer = csv.writer(f)

			for key in not_buggy.keys():
				writer.writerow(not_buggy[key])
			for key in buggy.keys():
				writer.writerow(buggy[key])
			for key in artifical.keys():
				writer.writerow(artifical[key])

if __name__ == '__main__':
	main()