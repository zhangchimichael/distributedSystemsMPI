import math
import random
from helper_classifier import *
from helper_common import *
import datetime
        
# start by reading the command line
numClusters, \
input, \
output, \
iterations, \
dataType = handleArgs(sys.argv)

#read input
points = readinput(input, dataType)

#get initial centroids
centroids = getInitialCentroids(points,numClusters)

#initialize
if dataType == 'points':
    Classifier = PointsClassifier
    updateCentroids = updateCentroidsPoint
else:
    setStrandLength(len(points[0]))
    Classifier = DNAClassifier
    updateCentroids = updateCentroidsDNA

#start timing    
t1 = datetime.datetime.now()
#k means
for i in range(iterations):
    classifier = Classifier(numClusters)
    for point in points:
        classifier.classify(point, centroids)
    centroids = updateCentroids([classifier.getStat()],numClusters)

#print timing
t2 = datetime.datetime.now()
print (t2-t1).total_seconds()
#output
writeoutput(output, points, centroids, classifier)
