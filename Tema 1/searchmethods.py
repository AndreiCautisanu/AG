import numpy
import math
import decode
import random
import functions as f

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
        if val < mincpy:
            flag = True
            mincpy = val
            firstImprov = nbor
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
        if bestOrFirst == "first":
            min, vn = improveFirst(bitList, best, L, d, func, a, b)
        elif bestOrFirst == "best":
            min, vn = improveBest(bitList, best, L, d, func, a, b)
    
        if min >= best:
            local = True
        else:
            bitList = vn
            best = min
    
    #print(decode.decode(bitList, -5.12, 5.12, L))
    return min

fnc = f.rast
minim = 100

for i in range(100):
    aya = hillClimb(30, 2, fnc, -5.12, 5.12, "best")
    if aya < minim:
        minim = aya
print(aya)