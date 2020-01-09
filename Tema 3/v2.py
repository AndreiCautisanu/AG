import sys
import os
from copy import deepcopy
import random
from math import ceil
from datetime import timedelta
from timeit import default_timer as timer

import time
import pprint
import numpy
import json

cache = dict()

def sort_list(list1, list2): 
    zipped_pairs = zip(list2, list1) 
    z = [x for _, x in sorted(zipped_pairs)] 
    return z 

def readCnfFile(file):
    f = open(file, "r")
    in_data = f.readlines()

    clauses = [[int(n) for n in line.split() if n!= '0' and n != '\n'] for line in in_data if line[0] not in ('c', 'p', '\n')]
    numberOfLiterals = in_data[1].split()[2]
    return clauses, numberOfLiterals

def clsCheck(clspt,genom):
    
    isGud = False
    for pt in clspt:
        if int(pt) == abs(int(pt)) and genom[abs(int(pt))-1] == 1:
            isGud = True
            break
    
        if int(pt) != abs(int(pt)) and genom[abs(int(pt))-1] == 0:
            isGud = True
            break

    return isGud


def randomSolution(literalsNo):
    return [random.randint(0,1) for i in range(literalsNo)]

#########################

def rouletteSelect(pop, clauses, nrLit, fitness, fitnessSum):
    randomFit = numpy.random.uniform(0, fitnessSum)
    runningSum = 0
    for i in range(len(fitness)):
        runningSum += fitness[i]
        if runningSum > randomFit:
            return pop[i]


def cx(parent1, parent2):
    p1 = list(parent1)
    p2 = list(parent2)

    k = random.randint(0, len(p1))

    for i in range(k, len(p1)):
        p1[i], p2[i] = p2[i], p1[i]

    return p1, p2

def mutateGenome(genome, rate):
    prob = numpy.random.uniform(0, 1)

    if prob < rate:
        k = numpy.random.randint(0, len(genome))
        genome[k] = 1 - genome[k]

try:
    with open("cache.json", "r") as read_file:
        cache = json.load(read_file)
except:
    pass
        
cls, nrLit = readCnfFile("clause1.cnf")
cls = numpy.array(cls)
CX_RATE = 0.7
MUT_RATE = 0.01
ELIT_RATE = 0.5
POP_SIZE = 100

pop = list()
for i in range(POP_SIZE):
    pop.append(randomSolution(int(nrLit)))

abstime = time.time()

for i in range(2000):

    start = time.time()

    # newpop,bestInGen = select(cls,pop,nrLit)
    # newpop = crossover(newpop,nrLit)
    # newpop = mutate(newpop,0.05)

    newPop = []
    fitness = popFitness(pop, cls)
    fitnessSum = sum(fitness)
    pop = sort_list(pop, fitness)
    pop.reverse()
    newPop = newPop + pop[:(int(POP_SIZE * ELIT_RATE) + 1)]

    for _ in range(int(((1 - ELIT_RATE) * POP_SIZE) / 2)):
        parent1 = rouletteSelect(pop, cls, nrLit, fitness, fitnessSum)
        parent2 = rouletteSelect(pop, cls, nrLit, fitness, fitnessSum)

        prob = numpy.random.uniform(0, 1)
        if prob < CX_RATE:
            child1, child2 = cx(parent1, parent2)
        else:
            child1, child2 = parent1, parent2
        
        mutateGenome(child1, 0.01)
        mutateGenome(child2, 0.01)

        newPop.append(child1)
        newPop.append(child2)

    passed = time.time() - start

    print("generation {} | best {} | time {} | abs time {}".format(i,fitness[0],passed,time.time()-abstime))

    pop = newPop[:POP_SIZE].copy()

    if i == 500:
        ELIT_RATE = 0.2
        CX_RATE = 0.75
        MUT_RATE = 0.02
    
    elif i == 750:
        ELIT_RATE = 0.02
        CX_RATE = 0.9
        MUT_RATE = 0.05
    
    elif i == 1250:
        ELIT_RATE = 0.01
        CX_RATE = 1
        MUT_RATE = 0.1
    
with open("cache.json", "w") as write_file:
    json.dump(cache, write_file)