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

def crossover(pop,nrLit):
    
    newpop = list()
    bitlen = len(pop[0])
    problist = list()

    for i in range(100):
        problist.append(random.uniform(0,1))

    problist.sort()

    newpop.append(pop[0])
    newpop.append(pop[1])
    newpop.append(pop[2])

    random.shuffle(pop)

    while len(newpop) < 99:
        for i in range(0,99,2):
            if problist[i] <= 0.3 and problist[i+1] <= 0.3:
                pos = random.randint(1,bitlen-1)
                newpop.append(pop[i][0:pos] + pop[i+1][pos:bitlen])
                newpop.append(pop[i+1][0:pos] + pop[i][pos:bitlen])
                if len(newpop) > 98:
                    break
    newpop.append(randomSolution(int(nrLit)))
    return newpop

def select(clauses, pop, nrLit):
    
    newpop = list()
    fitness = popFitness(pop,clauses)

    newpop = sort_list(pop,fitness)
    newpop.reverse()

    fitness.sort(reverse = True)

    return newpop,fitness[0]


def mutate(pop, rate):
    newpop = pop.copy()
    for genom in newpop:
        for bit in genom:
            if random.uniform(0,1) <= rate:
                bit = 1 - bit
    return newpop


def popFitness(pop, cls):
    fitness = list()
    for genom in pop:
        try:
            fit = cache[str(genom)]
        except:
            fit = 0
            for pt in cls:
                if clsCheck(pt,genom):
                    fit += 1
            cache[str(genom)] = fit
        fitness.append(fit/len(cls))
    return fitness


cls, nrLit = readCnfFile("clause1.cnf")
cls = numpy.array(cls)

pop = list()
for i in range(100):
    pop.append(randomSolution(int(nrLit)))

abstime = time.time()

for i in range(1000):

    start = time.time()

    newpop,bestInGen = select(cls,pop,nrLit)
    newpop = crossover(newpop,nrLit)
    newpop = mutate(newpop,0.05)

    passed = time.time() - start

    print("generation {} | best {} | time {} | abs time {}".format(i,bestInGen,passed,time.time()-abstime))

    pop = newpop.copy()
