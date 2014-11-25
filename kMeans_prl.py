import math
import random
from helper_classifier import *
from helper_common import *
from mpi4py import MPI
    
#mpi start
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
name = MPI.Get_processor_name()
num_nodes = comm.size
num_participants = num_nodes - 1
status = MPI.Status()
    
# start by reading the command line
numClusters, \
input, \
output, \
iterations, \
dataType = handleArgs(sys.argv)

#all nodes read input
points = readinput(input, dataType)

#initialize
if dataType == 'points':
    Classifier = PointsClassifier
    updateCentroids = updateCentroidsPoint
else:
    setStrandLength(len(points[0]))
    Classifier = DNAClassifier
    updateCentroids = updateCentroidsDNA

if rank == 0: #master   
    for iteration in range(iterations):
        #get initial centroids
        centroids = getInitialCentroids(points,numClusters)
        #broadcast updated centroid list
        for i in range(1, num_nodes):
            comm.send(centroids, dest=i)
        # receive stats from worker nodes
        stats = []
        for i in range (1, num_nodes):
            stats.append(comm.recv(source=i, tag=MPI.ANY_TAG, status=status))
        #update centroids using collected worker stats
        centroids = updateCentroids(stats,numClusters)
    #send empty centroids to workers, as a signal to break
    for i in range (1, num_nodes):
        comm.send([], dest=i)
    #output
    writeoutput(output, points, centroids, Classifier(numClusters))
else: #worker
    #each worker only handlers its own chunk of data
    chunkSize = len(points)/num_participants + 1
    points = points[(rank-1)*chunkSize:rank*chunkSize]
    while True:
        #receive new centroids from master
        centroids = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        #if centroids are empty, break. job done.
        if len(centroids)==0:
            break
        #initialize a new classfier, classify to gather statistic
        classifier = Classifier(numClusters)
        for point in points:
            classifier.classify(point, centroids)
        #send stat of this classifier to master
        comm.send(classifier.getStat(), dest=0)
