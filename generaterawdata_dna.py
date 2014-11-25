import sys
import csv
import numpy
import getopt
import math
import random

def usage():
    print '$> python generaterawdata.py <required args> [optional args]\n' + \
        '\t-c <#>\t\tNumber of clusters to generate\n' + \
        '\t-p <#>\t\tNumber of points per cluster\n' + \
        '\t-o <file>\tFilename for the output of the raw data\n' + \
        '\t-l [#]\t\tstrand length for points\n'  

#hamming distance for dna strands        
def hamming(point1, point2):
    return sum([0 if point1[i]==point2[i] else 1 for i in range(len(point1))])

def tooClose(point, points, minDist):
    '''
    Computes the hamming distance between the point and all points
    in the list, and if any points in the list are closer than minDist,
    this method returns true.
    '''
    for pair in points:
        if hamming(point, pair) < minDist:
                return True
    return False

def handleArgs(args):
    # set up return values
    numClusters = -1
    output = None
    strandLength = -1
    try:
        optlist, args = getopt.getopt(args[1:], 'c:p:l:o:')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for key, val in optlist:
        if   key == '-c':
            numClusters = int(val)
        elif key == '-p':
            numPoints = int(val)
        elif key == '-o':
            output = val
        elif key == '-l':
            strandLength = int(val)
    # check required arguments were inputted  
    if numClusters < 0 or numPoints < 0 or \
            strandLength < 1 or \
            output is None:
        usage()
        sys.exit()
    return (numClusters, numPoints, output, strandLength)

def drawOrigin(strandLength):
    return ''.join([random.choice('AGCT') for _ in range(strandLength)])

def variant(num_changes, string):
    changeList = {'A': 'GCT', 'C': 'AGT', 'T': 'AGC', 'G': 'ACT'}
    #make changes num_changes times. it's possible after changes it is same with original string
    strandLength = len(string)
    for i in range(num_changes):
        #pick an index, random change the letter at this index to another
        idx = random.choice(range(strandLength))
        string = string[0:idx]+random.choice(changeList[string[idx]])+string[idx+1::]
    return string
    
# start by reading the command line
numClusters, \
numPoints, \
output, \
strandLength = handleArgs(sys.argv)
minDistance = strandLength/2


# step 1: generate each centroid
centroids_radii = []
minDistance = 0
for i in range(0, numClusters):
    centroid_radius = drawOrigin(strandLength)
    # is it far enough from the others?
    while (tooClose(centroid_radius, centroids_radii, minDistance)):
        centroid_radius = drawOrigin(strandLength)
    centroids_radii.append(centroid_radius)
    
# step 2: generate the points for each centroid
with open(output, 'w') as fout:
    print >> fout, '#centroids:', centroids_radii
    points = []
    minClusterVar = 0
    maxClusterVar = strandLength/2
    for i in range(0, numClusters):
        # compute the variance for this cluster
        variance = random.choice(range(maxClusterVar+1))
        cluster = centroids_radii[i]
        for j in range(0, numPoints):
            string = variant(variance, cluster)
            print >> fout, string