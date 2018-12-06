import elm
import numpy as np
from sklearn import metrics

def run_model(X_train, X_test):
	print("\t\t\txxxxx ELM (polynomial) model xxxxx")
	# set parameters
	# params = ['poly', 0.5, [5]]

	# create a classifier ** mostly only classifier
	elmk = elm.ELMKernel()
	elmk.search_param(X_train, cv="kfold", of="accuracy", kf=["poly"], eval=10)
	#train and test
	# results are Error objects
	tr_result = elmk.train(np.array(X_train))
	te_result = elmk.test(np.array(X_test))

	# print(te_result.expected_targets)
	# print(te_result.predicted_targets)

	test_result = [1 if x > 0.5 else 0 for x in te_result.predicted_targets]
	# print(test_result)
	print('Accuracy: '+str(100*metrics.accuracy_score(te_result.expected_targets, test_result))+'%')

	print('F1 score: '+str(metrics.f1_score(te_result.expected_targets, test_result)))
	
	fpr, tpr, thresholds = metrics.roc_curve(te_result.expected_targets, test_result, pos_label=1)
	print("Area under curve: "+str(metrics.auc(fpr, tpr)))