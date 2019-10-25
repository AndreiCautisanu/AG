import numpy
import math
import decode
import random
import functions as f
from time import sleep

def neighbor(bitArray, pos):
    tmp = list(bitArray)
    tmp[pos] = int(not(bitArray[pos]))
    
    return tmp


def improveFirst(bitList, min, L, d, func, a, b):
    mincpy = min
    nbhood = [neighbor(bitList, i) for i in range(L*d)]

    flag = False
    for nbor in nbhood:
        dec = decode.decode(nbor, a, b, L)
        val = func(dec)
        if round(val, 4) < round(mincpy, 4):
            flag = True
            mincpy = val
            firstImprov = nbor
            #print(val)
            break
    
    if not(flag):
        firstImprov = []

    return mincpy, firstImprov

def improveBest(bitList, min, L, d, func, a, b):
    nbhood = [neighbor(bitList, i) for i in range(L*d)]

    minimum = func(nbhood[0])
    bestImprov = nbhood[0]

    for nbor in nbhood[1:]:
        dec = decode.decode(nbor, a, b, L)
        val = func(dec)
        if val < minimum:
            minimum = val
            bestImprov = nbor
    
    return minimum, bestImprov


def hillClimb(L, d, func, a, b, bestOrFirst):
    t = 0
    bitList = numpy.random.randint(2, size=L*d)
    random.shuffle(bitList)
    dec = decode.decode(bitList, a, b, L)
    best = func(dec)

    local = False

    while not(local):
        if bestOrFirst == "best":
            min, vn = improveBest(bitList, best, L, d, func, a, b)
        elif bestOrFirst == "first":
            min, vn = improveFirst(bitList, best, L, d, func, a, b)
    
        if min >= best:
            local = True
        else:
            bitList = vn
            best = min
    
    #print(decode.decode(bitList, -5.12, 5.12, L))
    return min, bitList

def simulatedAnnealing(L, d, func, a, b, dummy):
    t = 0
    Temp = 100
    bitList = numpy.random.randint(2, size=L*d)

    while round(Temp, 5) > 0: 
        currentEnergy = func(decode.decode(bitList, a, b, L))

        pos = numpy.random.randint(L*d)
        selected = neighbor(bitList, pos)
        selectedEnergy = func(decode.decode(selected, a, b, L))
        energyDelta = selectedEnergy - currentEnergy
        #print("HELLO LOOK AT ME E DELTA = {}".format(energyDelta))

        P = 1 if selectedEnergy < currentEnergy else numpy.exp(-(selectedEnergy - currentEnergy) / Temp)

        if numpy.random.uniform(0, 1) < P:
            bitList = selected
        
        Temp *= 0.95
        t += 1

    return func(decode.decode(bitList, a, b, L)), bitList

fnc = f.rast
minim = 100