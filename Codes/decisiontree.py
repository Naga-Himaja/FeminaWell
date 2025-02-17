from IPython.display import Image
#from sklearn.externals.six import StringIO
#import pydotplus
#from sklearn.tree import export_graphviz
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd



path = "../Dataset/allData.csv"
data = pd.read_csv(path)
data.head()

del data['PCOS_from']

del data['City']

del data['relocated city']


data['PCOS_label'] = None
data.head()

data = data.set_index('PCOS_label')

data = data.reset_index()


def label(row):
    if row['PCOS'] == 'Yes':
        return 1
    else:
        return 0


data['PCOS_label'] = data.apply(lambda row: label(row), axis=1)

data.head()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib notebook
# from adspy_shared_utilities import plot_decision_tree

PCOS_check = dict(zip(data.PCOS_label.unique(), data.PCOS.unique()))
PCOS_check

X = data.drop(['PCOS_label', 'PCOS'], axis=1)
y = data.PCOS_label

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

X_train.head()

y_train.head()

clf = DecisionTreeClassifier(max_depth=6).fit(X_train, y_train)

tree_predicted = clf.predict(X_test)
confusion = confusion_matrix(y_test, tree_predicted)
print(confusion)

print('Accuracy: {:.2f}'.format(accuracy_score(y_test, tree_predicted)))
print('Precision: {:.2f}'.format(precision_score(y_test, tree_predicted)))
print('Recall: {:.2f}'.format(recall_score(y_test, tree_predicted)))
print('F1: {:.2f}'.format(f1_score(y_test, tree_predicted)))

print(classification_report(
    y_test, tree_predicted, target_names=['No', 'Yes']))

print('Accuracy on training set: {:.2f}'.format(clf.score(X_train, y_train)))

print('Accuracy on test set: {:.2f}'.format(clf.score(X_test, y_test)))

feature_cols = ['Period Length', 'Cycle Length', 'Age', 'Overweight', 'loss weight gain / weight loss', 'irregular or missed periods', 'Difficulty in conceiving', 'Hair growth on Chin', 'Hair growth  on Cheeks', 'Hair growth Between breasts',
                'Hair growth  on Upper lips ', 'Hair growth in Arms', 'Hair growth on Inner thighs', 'Acne or skin tags', 'Hair thinning or hair loss ', 'Dark patches', 'always tired', 'more Mood Swings', 'exercise per week', 'eat outside per week', 'canned food often']


# Create DOT data
dot_data = StringIO()

export_graphviz(clf, out_file=dot_data, filled=True, rounded=True,
                special_characters=True, feature_names=feature_cols)
# Draw graph
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

# show graph
Image(graph.create_png())

pcos_prediction = clf.predict(X_test)
PCOS_check[pcos_prediction[0]]

pcos1 = clf.predict(
    [[5, 6,	2,	1,	1,	1,	1,	1,	0,	0,	1,	0,	0,	1,	1,	1,	1,	1,	0,	7,	0]])
PCOS_check[pcos1[0]]

pcos2 = clf.predict(
    [[5,	1,	2,	0,	0,	0,	0,	1,	0,	0,	1,	1,	0,	1,	0,	1,	0,	0,	3,	3,	0]])
PCOS_check[pcos2[0]]
