import build_sets
import combine_batting_pitching
import mlb_xgboost 
import numpy as np
from sklearn import tree
import pandas as pd
from sklearn.externals.six import StringIO
# import pydot
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error

# SCRAPE DATA
'''import mlb_scraper'''

# COMBINES SCRAPED CHUNKS INTO FULL RAW SETS
# dumps to 'full_batting_dataset.csv' and 'full_pitching_dataset.csv'
'''build_sets.build_from_scratch(2010)'''


# COMBINES BATTING AND PITCHING DATA AND BUILDS FEATURES
'''combine_batting_pitching.combine_batting_pitching()'''

# BUILDS XGBOOST DATASETS
import build_xgboost_datasets


RBI_parameters = {
			   	 'bst:max_depth':5, 
				 'bst:eta':0.01, 
				 'silent':1, 
				 'gamma':0.7,
				 'lambda':0.7,
				 'subsample':0.7,
				 'colsample_bytree':0.7
				}

pred = mlb_xgboost.mlb_xgboost(RBI_parameters, 'RBI')


print 'here'
# run Amy's tree
train_file = 'final_RBI_train.csv'
train_label_file = 'final_RBI_train_label.csv'
test_file = 'final_RBI_cv.csv'
test_label_file = 'final_RBI_cv_label.csv'


'''
def draw_graph(clf, X_train):
	dot_data = StringIO() 
	tree.export_graphviz(clf, out_file=dot_data,
			     feature_names=list(X_train),
			     filled=True, rounded=True,
			     special_characters=True)
	graph = pydot.graph_from_dot_data(dot_data.getvalue())
	graph.write_pdf("treeimg.pdf")
'''


X_train = pd.read_csv(train_file)
Y_train = pd.read_csv(train_label_file, header = None)
X_test = pd.read_csv(test_file)
Y_test = pd.read_csv(test_label_file, header = None)
clf = tree.DecisionTreeRegressor(
	min_samples_leaf = 500, min_samples_split = 100, 
	min_weight_fraction_leaf = 0.2,
	max_depth = 10)
clf = clf.fit(X_train, Y_train)
print 'Score: '
print clf.score(X_test, Y_test)
Y_predict = clf.predict(X_test)
print 'RMSE: '
print np.sqrt(mean_squared_error(Y_test, Y_predict))


# combine results
combined = pd.DataFrame()

combined["Kurt"] = pred
combined["Amy"] = Y_predict
combined["Actual"] = Y_test
 
min_rmse = 999
weighting = 0
print np.sqrt(mean_squared_error(combined.Kurt, combined.Actual))

for i in xrange(1,1000):
	weight = float(i) / 1000
	weighted_pred = (1 - weight) * combined.Kurt + weight * combined.Amy
	rmse = np.sqrt(mean_squared_error(weighted_pred, combined.Actual))
	print rmse
	if rmse < min_rmse:
		min_rmse = rmse
		weighting = weight

print "BEST:"
print min_rmse
print weighting





