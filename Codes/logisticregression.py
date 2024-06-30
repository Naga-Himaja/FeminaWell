# -*- coding: utf-8 -*-
"""LogisticRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y8Mb0HTo2AqYMcahdeY-qdp2ahXIYeUk
"""

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

data_path = "/content/drive/My Drive/Academics SPIT/PROJECTS/SEM 4 - PCOS Prediction Research Project/Codes/Logistic Regression/data.csv"
data = pd.read_csv(data_path)

data.head()

del data['PCOS_from']
del data['City']
del data['relocated city']
del data['Unnamed: 0']

data.head()

data['PCOS_label'] = None
data = data.set_index('PCOS_label')
data = data.reset_index()
data.head()


def label(row):
    if row['PCOS'] == 'Yes':
        return 1
    else:
        return 0


data['PCOS_label'] = data.apply(lambda row: label(row), axis=1)

data.head()


PCOS_check = dict(zip(data.PCOS_label.unique(), data.PCOS.unique()))
PCOS_check

x = data.drop(['PCOS_label', 'PCOS'], axis=1)
y = data.PCOS_label

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=0)

xtrain, xtest, ytrain, ytest = train_test_split(
    x, y, test_size=0.25, random_state=0)

sc_x = StandardScaler()
xtrain = sc_x.fit_transform(xtrain)
xtest = sc_x.transform(xtest)

print(xtrain[0:10, :])

classifier = LogisticRegression(random_state=0)
classifier.fit(xtrain, ytrain)

y_pred = classifier.predict(xtest)

cm = confusion_matrix(ytest, y_pred)

print("Confusion Matrix : \n", cm)

print("Accuracy : ", accuracy_score(ytest, y_pred))
