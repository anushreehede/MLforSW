### Performs the significance test to return the set of significant features ###

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import scipy.stats

# From pylab import plot, show, savefig, xlim, figure, hold, ylim, legend, boxplot, setp, axes
from scipy.stats import ranksums
import sys
import os
import csv
from string import ascii_lowercase

# Datset directory
directory = "../data"

# Function to get the confidence interval of some data
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m-h, m+h


def main():

	# Directory particular balanced dataset indicated by command line arg
	data_dir = os.path.join(directory, sys.argv[1])

	# If data is not randomly sampled
	if sys.argv[1] != 'random_sampled':

		results_array = {} # Structure to store the results of the significance tests

		# Iterate through each of the 7 project files
		for k in range(1, 8):

			# Read files and get the data
			filepath = os.path.join(data_dir, str(k)+'_'+sys.argv[1]+'.csv')
			print(filepath)
			aging_data = pd.read_csv(filepath, header=None)

			# Separating the target attribute
			aging_value = aging_data.iloc[:, 82];
			# Getting respective indices of instances belonging to a class
			aging_value_rows = aging_value[aging_value > 0]
			non_aging_value_rows = aging_value[aging_value == 0]

			p = [] # Structure to store the p values

			# Iterate through each of the features
			for i in range(0,82):
			    
				# Get the confidence interval of the feature
			    feature_column = aging_data.iloc[:, i]
			    feature_column_aging_value = feature_column.iloc[aging_value_rows.index]
			    feature_column_non_aging_value = feature_column.iloc[non_aging_value_rows.index]
			    confidance_interval_aging = mean_confidence_interval(feature_column_aging_value)
			    confidance_interval_non_aging = mean_confidence_interval(feature_column_non_aging_value)
			    pair = [confidance_interval_aging, confidance_interval_non_aging]
			    
			    # Plot the confidence interval of the data in boxplot
			    fig = plt.figure()
			    plt.boxplot(pair)
			    index = str(i+1)

			    # Save the plots
			    plot_dir = data_dir+"/boxplots"+str(k)
			    if not os.path.exists(plot_dir):
			    	os.mkdir(plot_dir)
			    fig.savefig(plot_dir+"/box"+index)
			    
			    # Get the p values
			    p.append(ranksums(feature_column_aging_value, feature_column_non_aging_value) )
			    # print(p[i])
		    
			l = []
			# Iterate through each of the features
			for i in range(0, 82):

				# If p values of feature is below threshold, include it as a significant feature
				if (p[i][1] <= 0.05):
					l.append(i+1)
					if k not in results_array.keys():
						results_array.update({k: [1]})
					else:
						results_array[k].append(1)
				else:
					if k not in results_array.keys():
						results_array.update({k: [0]})
					else:
						results_array[k].append(0)

			print(l)
			print(len(l))


		# Store the selected features in another file
		new_filename = os.path.join(data_dir, sys.argv[1]+"_sig_results.csv")
		with open(new_filename, 'a') as outfile:
			writer = csv.writer(outfile)

			for key in results_array.keys():
				writer.writerow(results_array[key])

	# If data is randomly sampled
	else:

		# Iterate through each of the 7 project files
		for k in range(1, 8):

			results_array = {} # Structure to store the results of the significance tests
			
			# Iterate through each of the 10 samples for each project
			for c in ascii_lowercase:

				if c == 'k':
					break

				# Read files and get the data
				filepath = os.path.join(data_dir, 'files/'+str(k)+'_'+sys.argv[1]+'_'+c+'.csv')
				print(filepath)
				aging_data = pd.read_csv(filepath, header=None)

				# Separating the target attribute
				aging_value = aging_data.iloc[:, 82];
				# Getting respective indices of instances belonging to a class
				aging_value_rows = aging_value[aging_value > 0]
				non_aging_value_rows = aging_value[aging_value == 0]

				p = [] # Structure to store the p values

				# Iterate through each of the features
				for i in range(0,82):
				    
					# Get the confidence interval of the feature
				    feature_column = aging_data.iloc[:, i]
				    feature_column_aging_value = feature_column.iloc[aging_value_rows.index]
				    feature_column_non_aging_value = feature_column.iloc[non_aging_value_rows.index]
				    confidance_interval_aging = mean_confidence_interval(feature_column_aging_value)
				    confidance_interval_non_aging = mean_confidence_interval(feature_column_non_aging_value)
				    pair = [confidance_interval_aging, confidance_interval_non_aging]
				    
				    # Plot the confidence interval of the data in boxplot
				    fig = plt.figure()
				    plt.boxplot(pair)
				    index = str(i+1)

				    # Save the plots
				    plot_dir = data_dir+"/boxplots"+str(k)
				    if not os.path.exists(plot_dir):
				    	os.mkdir(plot_dir)
				    fig.savefig(plot_dir+"/box"+index)
				    
				    # # Get the p values
				    p.append(ranksums(feature_column_aging_value, feature_column_non_aging_value) )
				    # print(p[i])
			    
				# Iterate through each of the features
				for i in range(0, 82):

					# If p values of feature is below threshold, include it as a significant feature
					if (p[i][1] <= 0.05):
						if c not in results_array.keys():
							results_array.update({c: [1]})
						else:
							results_array[c].append(1)
					else:
						if c not in results_array.keys():
							results_array.update({c: [0]})
						else:
							results_array[c].append(0)

			l = []
			results = []
			for j in range(0, 82):
				count = 0
				for d in results_array.keys():
					if results_array[d][j] == 1:
						count += 1
				# print(count)
				if count > 5:
					l.append(j+1)
					results.append(1)
				else:
					results.append(0)

			# print(results)
			print(l)
			print(len(l))

			# Store the selected features in another file
			new_filename = os.path.join(data_dir, sys.argv[1]+"_sig_results.csv")
			outfile = open(new_filename, 'a')
			writer = csv.writer(outfile)
			writer.writerow(results)
			outfile.close()



if __name__ == "__main__":
	main()