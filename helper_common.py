from helper_classifier import *
import getopt
import sys
import random

def usage():
    print '$> python generaterawdata.py <required args> [optional args]\n' + \
        '\t-c <#>\t\tNumber of numClusters to generate\n' + \
        '\t-i <file>\tFilename for the input of the raw data\n' + \
        '\t-o <file>\tFilename for the output of the raw data\n' + \
        '\t-r [#]\t\tmax iterations for k means run\n'  \
        '\t-d \t\tdata type using dna\n'\
        '\t-p \t\tdata type using points\n'
        
def handleArgs(args):
    # set up return values
    numClusters = -1
    input = None
    output = None
    iterations = 100
    dataType = None
    try:
        optlist, args = getopt.getopt(args[1:], 'c:i:o:r:pd')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for key, val in optlist:
        # first, the required arguments
        if   key == '-c':
            numClusters = int(val)
        elif key == '-i':
            input = val
        elif key == '-o':
            output = val
        elif key == '-p':
            dataType = 'points'
        elif key == '-d':
            dataType = 'dna'
        # now, the optional argument
        elif key == '-r':
            iterations = int(val)
    # check required arguments were inputted  
    if numClusters < 0 or input is None or\
            output is None or dataType not in ('points', 'dna'):
        usage()
        sys.exit()
    return (numClusters, input, output, iterations, dataType)

    
#initialize centroids. random select cluster centroids from points list
def getInitialCentroids(points,numClusters):
    targetClusterSize = len(points)/numClusters
    centroids = []
    idx = random.randint(0,targetClusterSize)
    for i in range(numClusters):
        centroids.append(points[(idx+i*targetClusterSize)%len(points)])
    return centroids
    
#input    
def readinput(input, dataType):  
    points = []
    with open(input) as fin:
        for line in fin:
            if len(line.strip())==0:
                continue
            if line[0]=='#': # this sign is used as remarks for files here
                continue
            if dataType == 'points': #2d points
                x, y = line.rstrip().split(',')
                x, y = float(x), float(y)
                points.append((x,y))
            else: #dna
                points.append(line.rstrip())
    return points

#output
def writeoutput(output, points, centroids, classifier):
    with open(output, 'w') as fout:
        for point in points:
            print >> fout, str(point) + '\t' + str(classifier.classify(point, centroids))