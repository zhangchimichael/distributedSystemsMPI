import math

#module points    
def updateCentroidsPoint(stats, numClusters):
    xTotal = [0 for _ in range(numClusters)]
    yTotal = [0 for _ in range(numClusters)]
    clusterCount = [0 for _ in range(numClusters)]
    for stat in stats:
        for c in range(numClusters):
            xTotal[c]+=stat[0][c]
            yTotal[c]+=stat[1][c]
            clusterCount[c]+=stat[2][c]
    centroidsX = [xTotal[c]/float(clusterCount[c]) for c in range(numClusters)]
    centroidsY = [yTotal[c]/float(clusterCount[c]) for c in range(numClusters)]
    return zip(centroidsX, centroidsY)

class PointsClassifier:
    def __init__(self, numClusters):
        self.xTotal = [0 for _ in range(numClusters)]
        self.yTotal = [0 for _ in range(numClusters)]
        self.clusterCount = [0 for _ in range(numClusters)]
    def euc(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    def classify(self, point, centroids):
        clusterIndex = reduce(lambda a, b: a if a[1]<b[1] else b,
            [(idx, self.euc(cent, point)) for idx, cent in enumerate(centroids)])[0]
        self.clusterCount[clusterIndex]+=1
        self.xTotal[clusterIndex]+=point[0]
        self.yTotal[clusterIndex]+=point[1]
        return clusterIndex
    def getStat(self):
        return (self.xTotal, self.yTotal, self.clusterCount)


#module dna
strandLength = None
def setStrandLength(length):
    global strandLength
    strandLength = length
    
def updateCentroidsDNA(stats, numClusters):
    global strandLength
    #3-dim array. [agct count] * strandLength * numClusters
    clusterCount = [[[0,0,0,0] for _ in range(strandLength)] for _ in range(numClusters)]
    for stat in stats:
        for i in range(numClusters):
            for j in range(strandLength):
                for k in range(4):
                    clusterCount[i][j][k]+=stat[i][j][k]
    idxToDNA = {0:'A', 1:'G', 2:'C', 3:'T'}
    dna = [['' for _ in range(strandLength)] for _ in range(numClusters)]
    for i in range(numClusters):
        for j in range(strandLength):
            dna[i][j] = idxToDNA[
                            reduce(lambda a,b:a if a[1]>b[1] else b,
                            [(k, cnt) for k, cnt in enumerate(clusterCount[i][j])])[0]]
    return [''.join(dna[i]) for i in range(numClusters)]

    
class DNAClassifier:
    def __init__(self,numClusters): 
        global strandLength
        #3-dim array. [agct count] * strandLength * numClusters
        self.clusterCount = [[[0,0,0,0] for _ in range(strandLength)] for _ in range(numClusters)]
        self.dnaIndex = {'A': 0, 'G': 1, 'C': 2, 'T': 3}
    def hamming(self, point1, point2):
        return sum([0 if point1[i]==point2[i] else 1 for i in range(len(point1))])
    def classify(self, dna, centroids):
        clusterIndex = reduce(lambda a, b: a if a[1]<b[1] else b,
            [(idx, self.hamming(cent, dna)) for idx, cent in enumerate(centroids)])[0]
        for i, x in enumerate(dna):
            self.clusterCount[clusterIndex][i][self.dnaIndex[x]]+=1
        return clusterIndex
    def getStat(self):
        return self.clusterCount
