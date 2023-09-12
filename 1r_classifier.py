k = 6
import csv, random, math
from statistics import mode
file = open('star_data_training.csv')
type(file)
csvreader = csv.reader(file)
header = []
header = next(csvreader)
rows = []
for row in csvreader:
    r = row
    tup = (math.log(float(r[0])), math.log(float(r[1])), math.log(float(r[2])), float(r[3]), r[4])
    rows.append(tup)
population = rows
#print(rows)
means = random.sample(population, k)
clusters = [[] for i in range(k)]
d = {}
def makedict(population):
    global d
    for star in population:
        if(star[4] not in d):
            d[star[4]] = [star]
        else:
            d[star[4]].append(star)
makedict(population)
def bin(population, num_bins, index):
    #if 6 bins, need ? numbers
    #0-1 1-2 2-3 3-4 4-5 5-rest --> 1 2 3 4 5 max
    newarr = []
    for i in range(len(population)):
        newarr.append(population[i][index])
    step = int(len(newarr)/num_bins)
    returner = []
    newarr = sorted(newarr)
    for i in range(num_bins-1):
        returner.append(newarr[step*(1+i)])
    returner.append(newarr[len(newarr)-1])
    return returner
def assigntobin(star, bins, index):
    for i in range(len(bins)):
        if(float(star[index])<bins[i]):
            return i
    return len(bins)-1
def tuplify(bins):
    returner = []
    returner.append((-math.inf, bins[0]))
    for i in range(1, len(bins)-1):
        returner.append((bins[i], bins[i+1]))
    returner.append((bins[len(bins)+1], math.inf))
u = bin(population, 6, 2)
#print(u)
#print(assigntobin(population[0], u, 2))
#print(population[0])
errors = []
allbins = []
def fcalc(typestobins, characteristic, typ):
    mbin = [0 for i in range(6)]
    for i in range(len(typestobins[characteristic][typ])):
        mbin[typestobins[characteristic][typ][i]]+=1
    bestbin = mbin.index(max(mbin))
    error = len(typestobins[characteristic][typ])-max(mbin)
    return (bestbin, error)
#for characteristic
#assign all thingies to bin
#find out which bin is most accurate for each star type
#store that error
#return index of lowest error/best set of bins
typestobins = [] #array of dictionaries
""" for characteristic in range(4):
    typestobins.append({})
    bins = bin(population, 6, characteristic)
    errors.append(0)
    for typ in range(6):
        typestobins[characteristic][typ] = []
        for star in d[typ]:
            b = assigntobin(star, bins, characteristic)
            typestobins[characteristic][typ].append(b)
        b = fcalc(typestobins, characteristic, typ)
        bestbin = b[0]
        errortyp = b[1]
        errors[characteristic]+=errortyp
        typestobins[characteristic][typ]=bestbin """
for characteristic in range(4):
    typestobins.append({})
    bins = bin(population, 6, characteristic)
    errors.append(0)
    typestobins[characteristic] = [[] for i in range(6)]
    for typ in range(6):    
        #print(typ)
        #print(d[0])
        #print(d)    
        for star in d[str(typ)]:
            b = assigntobin(star, bins, characteristic)
            typestobins[characteristic][b].append(typ)
    for typ in range(6):
        b = fcalc(typestobins, characteristic, typ)
        bestbin = b[0]
        errortyp = b[1]
        errors[characteristic]+=errortyp
        typestobins[characteristic][typ]=bestbin
bestcharacteristic = errors.index(min(errors))
bins = bin(population, 6, bestcharacteristic)
print(bins)
print(bestcharacteristic)
bestbins = typestobins[bestcharacteristic]
print(bestbins)
file = open('star_data_test.csv')
type(file)
csvreader = csv.reader(file)
header = []
header = next(csvreader)
rows2 = []
for row in csvreader:
    r = row
    tup = (math.log(float(r[0])), math.log(float(r[1])), math.log(float(r[2])), float(r[3]), r[4])
    #print(r[4])
    rows2.append(tup)
testpopulation = rows2
c = [[] for i in range(6)]
for star in testpopulation:
    n = assigntobin(star, bins, bestcharacteristic)
    category = bestbins[n]
    c[category].append(star[4])
for i in range(len(c)):
    print(str(i))
    print(c[i])