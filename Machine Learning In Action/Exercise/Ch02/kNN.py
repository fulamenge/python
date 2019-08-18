from numpy import *
import operator
from os import listdir

import matplotlib
import matplotlib.pyplot as plt

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()     
    # print(sortedDistIndicies)
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # print("voteIlabel :" + voteIlabel)
        # print("classCount.get(voteIlabel,0) + 1 :" + repr(classCount.get(voteIlabel,0) + 1))
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    	# print("classCount.iteritems(): " + repr(classCount.iteritems()))
    print("operator.itemgetter(1): " + str(operator.itemgetter(1)))       
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    print("sortedClassCount : " + str(sortedClassCount))
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        # print("list: " + str(listFromLine[0:3]))
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector
    

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals


def TestArgSort():
	k = array([1,9,5,7])
	st = k.argsort()
	print(st)

def TestZeros():
	k = array([1,9,5,7])
	returnMat = zeros((2, 3));
	print(returnMat)

def TestStrip():
	s = " Hello World   ";
	print(s)
	s = s.strip()
	print(s)

def TestScat(datingDataMat, datingLabels):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0*array(datingLabels), 15.0*array(datingLabels))
	plt.show()

def TestList():
	list = [1,3,5,7,9,11,13]
	print(list[:0])
	print(list[:1])
	print(list[:2])

# TestArgSort()
group, labels = createDataSet()
 
datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
# print(datingDataMat)
# print(datingDataMat[:,1])
# TestScat(datingDataMat, datingLabels)

m = datingDataMat.shape[0]
print("m is :" + str(m))
minVals = datingDataMat.min(0)
normDataSet = datingDataMat - tile(minVals, (m,1))
print(tile(minVals, (m,1)))
print(normDataSet)
# value = classify0([0, 0], group, labels, 3)
# print(value)
# TestList()
