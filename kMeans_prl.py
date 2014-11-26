import math
import random
from helper_classifier import *
from helper_common import *
from mpi4py import MPI
import datetime
    
#mpi start
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
name = MPI.Get_processor_name()
num_nodes = comm.size
status = MPI.Status()
    
# start by reading the command line
numClusters, \
input, \
output, \
iterations, \
dataType = handleArgs(sys.argv)

#all nodes read input
points = readinput(input, dataType)

#each node, work or master, only handlers its own chunk of data
chunkSize = len(points)/num_nodes + 1
chunk = points[rank*chunkSize:(rank+1)*chunkSize]

#initialize
if dataType == 'points':
    Classifier = PointsClassifier
    updateCentroids = updateCentroidsPoint
else:
    setStrandLength(len(points[0]))
    Classifier = DNAClassifier
    updateCentroids = updateCentroidsDNA

if rank == 0: #master   
    #start timing    
    t1 = datetime.datetime.now()
    for iteration in range(iterations):
        #get initial centroids
        centroids = getInitialCentroids(points,numClusters)
        #broadcast updated centroid list
        for i in range(1, num_nodes):
            comm.send(centroids, dest=i)
        #initialize a new classfier, classify to gather statistic for its chunk
        classifier = Classifier(numClusters)
        for point in chunk:
            classifier.classify(point, centroids)
        stats = [classifier.getStat()]
        # receive stats from other worker nodes
        for i in range (1, num_nodes):
            stats.append(comm.recv(source=i, tag=MPI.ANY_TAG, status=status))
        #update centroids using collected worker stats
        centroids = updateCentroids(stats,numClusters)
    #send empty centroids to workers, as a signal to break
    for i in range (1, num_nodes):
        comm.send([], dest=i)
    #print timing
    t2 = datetime.datetime.now()
    print (t2-t1).total_seconds()
    #output
    writeoutput(output, points, centroids, Classifier(numClusters))
else: #worker
    while True:
        #receive new centroids from master
        centroids = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        #if centroids are empty, break. job done.
        if len(centroids)==0:
            break
        #initialize a new classfier, classify to gather statistic for its chunk
        classifier = Classifier(numClusters)
        for point in chunk:
            classifier.classify(point, centroids)
        #send stat of this classifier to master
        comm.send(classifier.getStat(), dest=0)
