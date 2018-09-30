import xlrd
import math
import os
import random
import csv 

# Datset directory
directory = "../sigmetris/data"

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
	# Give the location of the file 
	loc = (filename) 
	  
	# To open Workbook 
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 

	i = 0
	buggy = {}
	not_buggy = {}
	for i in range(sheet.nrows):
		instance = sheet.row_values(i)

		if instance[-1] != 0:
			buggy.update({i : instance})
		else:
			not_buggy.update({i : instance})
			
	return buggy, not_buggy, sheet.ncols

def main():

	for file in os.listdir(directory):
		filename = os.path.join(directory, file)
		print('\n\t\t\t'+filename)
		buggy, not_buggy, feature_num = read_file(filename)
		print(str(len(buggy))+','+str(len(not_buggy))+","+str((float)(len(not_buggy))/((len(not_buggy))+len(buggy)) * 100))

		num_artificial_instances = len(not_buggy) - len(buggy)

		artifical = {}
		count = 0
		for i in range(num_artificial_instances):
			count += 1
			artifical.update({count: []})

		for i in range(feature_num):
			lower, upper = get_intervals(buggy, i)

			# Create num_artificial_instances random values in range (lower, upper)
			# Store them in a list feature_values
			feature_values = []
			for j in range(num_artificial_instances):
				feature_values.append(random.uniform(lower, upper))

			for j in range(num_artificial_instances):
				artifical[j+1].append(feature_values[j])

		print('not buggy: '+str(len(not_buggy))+' buggy: '+str(len(buggy)+len(artifical)))

		new_filename = os.path.join(directory, file+'_scaled.csv')

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