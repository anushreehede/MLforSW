import elm
import numpy as np
from sklearn import metrics

def run_model(X_train, X_test):
	
	# set parameters
	params = ['linear', 0.5, 5]

	# create a classifier ** mostly only classifier
	elmk = elm.ELMKernel(params)

	#train and test
	# results are Error objects
	tr_result = elmk.train(np.array(X_train))
	te_result = elmk.test(np.array(X_test))

	# print(te_result.expected_targets)
	# print(te_result.predicted_targets)

	print('Accuracy: '+str(metrics.accuracy_score(te_result.expected_targets, te_result.predicted_targets)))

	print('F1 score: '+str(metrics.f1_score(te_result.expected_targets, te_result.predicted_targets)))
	
	fpr, tpr, thresholds = metrics.roc_curve(te_result.expected_targets, te_result.predicted_targets, pos_label=1)
	print("Area under curve: "+str(metrics.auc(fpr, tpr)))

