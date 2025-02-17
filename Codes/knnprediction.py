from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import operator
import math
import random
import csv
import pandas as pd
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

#copied_path = "drive/My Drive/ML/KNN/data.csv"
copied_path = "/content/drive/My Drive/Academics SPIT/PROJECTS/SEM 4 - PCOS Prediction Research Project/Codes/KNN/data.csv"
data = pd.read_csv(copied_path)

data.head()
cols = [0]
data.drop(data.columns[cols], inplace=True, axis=1)

cols = list(data.columns.values)  # Make a list of all of the columns in the df
cols.pop(cols.index('City'))  # Remove b from list
cols.pop(cols.index('PCOS'))  # Remove x from list
cols.pop(cols.index('PCOS_from'))
data = data[cols+['City', 'PCOS_from', 'PCOS']]

data['PCOS'] = data['PCOS'].map(dict(Yes=1, No=0))

data.head()


def loadDataset(data, split, trainingSet=[], testSet=[]):
    dataset = data.values.tolist()
    for x in range(len(dataset)-1):
        for y in range(22):
            dataset[x][y] = int(dataset[x][y])
        if random.random() < split:
            trainingSet.append(dataset[x])
        else:
            testSet.append(dataset[x])


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
        return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []

    for x in range(k):
        neighbors.append(distances[x][0])

    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]

        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
            sortedVotes = sorted(classVotes.items(),
                                 key=operator.itemgetter(1), reverse=True)

    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0

    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1

    return (correct/float(len(testSet)))


# Python script for confusion matrix creation.


def main():  # prepare data
    trainingSet = []
    testSet = []
    split = 0.67

    loadDataset(data, split, trainingSet, testSet)

    print('Train set: ' + repr(len(trainingSet)))

    print('Test set: ' + repr(len(testSet)))

    # generate predictions
    predictions = []
    k = 3

    for x in range(len(trainingSet)):
        neighbors = getNeighbors(trainingSet, trainingSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)

    #print('> predicted=' + repr(result) + ', actual=' + repr(trainingSet[x][-1]))
    accuracy = getAccuracy(trainingSet, predictions)
    print('Accuracy Training: ' + repr(accuracy) + '%')

    predictions.clear()
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)

    #print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy Test: ' + repr(accuracy) + '%')

    actual = []

    for x in range(len(testSet)):
        actual.append(testSet[x][-1])

    results = confusion_matrix(actual, predictions)

    print('Confusion Matrix :')
    print(results)
    print('Accuracy Score :', accuracy_score(actual, predictions))
    print('Report : ')
    print(classification_report(actual, predictions))


main()
