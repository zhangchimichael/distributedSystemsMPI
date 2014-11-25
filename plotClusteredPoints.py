import matplotlib.pyplot as plt
import getopt
import sys

def handleArgs(args):
    input = None
    try:
        optlist, args = getopt.getopt(args[1:], 'i:')
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for key, val in optlist:
        if key == '-i':
            input = val
    if input is None:
        usage()
        sys.exit()
    return input


inputfile = handleArgs(sys.argv)
xLists = dict()
yLists = dict()
with open(inputfile) as fin:
    for line in fin:
        point, idx = line.rstrip().split('\t')
        x, y = point.rstrip(')').lstrip('(').split(',')
        x = float(x.strip())
        y = float(y.strip())
        xList = xLists.get(idx)
        if not xList:
            xLists[idx], yLists[idx]=[],[]
        xLists[idx].append(x)
        yLists[idx].append(y)

fig, ax = plt.subplots()
plt.title('clusters')
shapes = ['.','o','v','x','+',',','s','p','h','D','*']
colors = ['blue','green','red','cyan','magenta','yellow','black','white']
for i, idx in enumerate(xLists.keys()):
    ax.scatter(xLists[idx],yLists[idx], label=idx, 
                marker=shapes[i%len(shapes)], c = colors[i%len(colors)])
legend = ax.legend(shadow=True)
plt.show()    