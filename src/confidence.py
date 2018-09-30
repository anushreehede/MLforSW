import csv
import math
import matplotlib.pyplot as plt
import os

# Datset directory
main_dir = "../RefactDataSetValidated"

def get_intervals(metric_dict, index):
	# Get the values of the metrics for each method belonging to a class (ref, notref)
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

	return lower, upper, values

# Simple overlap checking of the two confidence intervals of the two classes
def check_overlap(CI_ref, CI_notref):
	if CI_ref[0] < CI_notref[0]:
		if CI_ref[1] < CI_notref[0]:
			return False
		else:
			return True
	else:
		if CI_notref[1] < CI_ref[0]:
			return False
		else:
			return True

# Read the dataset files and store separately based on two classes
def read_file(filename):
	i = 0
	method_ref = {}
	method_not_ref = {}
	with open(filename) as f:
		x = f.readline()
		reader = csv.reader(f)
		for line in reader:	
			metrics = line[10:95]
			# print(metrics)
			i += 1
			if metrics[-1] != '0':
				print(metrics[-1])
				method_ref.update({i : metrics})
			else:
				method_not_ref.update({i : metrics})
			# print('size='+str(len(metrics)))
	# print('methods='+str(i))

	return method_ref, method_not_ref

# Calculate the confidence intervals of the two classes and check for overlap. 
# Print their box plot diagrams as well. 
def check_significance(method_ref, method_not_ref, directory):
	num_metrics = len(method_not_ref[1])
	# print(str(num_metrics)+'\n')

	for j in range(num_metrics):
		
		lower_ref, upper_ref, values_ref = get_intervals(method_ref, j) 
		# print("CI for refactored methods is ("+str(lower_ref)+","+str(upper_ref)+")")

		lower_notref, upper_notref, values_notref = get_intervals(method_not_ref, j) 
		# print("CI for not refactored methods is ("+str(lower_notref)+","+str(upper_notref)+")")

		y = check_overlap((lower_ref, upper_ref), (lower_ref, upper_notref))
		if y == False:
			print('>>> '+str(j+1)+' is a significant metric')

		# print(values_ref)
		# print(values_notref)
		val = [values_ref, values_notref]
		plt.boxplot(val)
		plot_file = 'plots/'+directory+'/CIplot'+str(j+1)+'.png'
		plt.savefig(plot_file)
		# plt.show()

		

def main():

	for directory in os.listdir(main_dir):
		directory_path = os.path.join(main_dir, directory)
		for outer_dir in os.listdir(directory_path):
			outer_dir_path = os.path.join(directory_path, outer_dir)
			filename = os.path.join(outer_dir_path,directory+"-Method.csv")
			print('\n\t\t\t'+filename)
			method_ref, method_not_ref = read_file(filename)
			print(str(len(method_ref))+','+str(len(method_not_ref))+","+str((float)(len(method_not_ref))/((len(method_not_ref))+len(method_ref)) * 100))
			# check_significance(method_ref, method_not_ref, directory)

if __name__ == '__main__':
	main()


