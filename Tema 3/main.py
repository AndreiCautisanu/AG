import sys
import os
from copy import deepcopy
from random import randint, choice, random
from math import ceil
from datetime import timedelta
from timeit import default_timer as timer

def readCnfFile(file):
    f = open(file, "r")
    in_data = f.readlines()

    clauses = [[int(n) for n in line.split() if n!= '0' and n != '\n'] for line in in_data if line[0] not in ('c', 'p', '\n')]
    numberOfLiterals = in_data[1].split()[2]
    return clauses, numberOfLiterals


def checkUnsatisfiedClauses(clauses, sol):
    # unsatClauses = deepcopy(clauses)

    # for lit in sol:
    #     i = 0
    #     while i < len(unsatClauses):
    #         if lit in unsatClauses[i]:
    #             unsatClauses.remove(unsatClauses[i])
    #         else:
    #             i = i + 1

    # return len(unsatClauses)

    satisfiedClausesNo = 0

    for clause in clauses:
        for lit in clause:
            if lit in sol:
                satisfiedClausesNo += 1
                break
    
    return len(clauses) - satisfiedClausesNo



def randomSolution(literalsNo):
    sol = []
    for i in range(1, int(literalsNo)+1):
        sign = randint(0,1)
        if sign: 
            sol.append(i)
        else:
            sol.append(0-i)

    return sol


def sortPop(clauses, pop, popSize, unsatclausesNo):
    temp = [0] * popSize

    for i in range(popSize):
        for j in range(i, popSize):
            if unsatclausesNo[i] > unsatclausesNo[j]:
                unsatclausesNo[i], unsatclausesNo[j] = unsatclausesNo[j], unsatclausesNo[i]
                pop[i], pop[j] = pop[j], pop[i]


def crossover(pop, popSize):
    newPop = [0] * popSize
    literalsNo = len(pop[0])
    
    for i in range(popSize):
        cutoffPoint = randint(0, literalsNo-1)
        newPop[i] = pop[randint(0, popSize-1)][:cutoffPoint] + pop[randint(0, popSize-1)][cutoffPoint:]

    return newPop


def select(clauses, pop, popSize, unsatClausesNo):
    newPop = []
    fits = []
    clausesNo = len(clauses)

    for i in range(popSize):
        fits = fits + ([i] * ( ceil((clausesNo - unsatClausesNo[i] ) / 10)))

    for i in range(popSize):
        newPop.append(pop[choice(fits)])

    return newPop


def mutate(pop, rate):
    literalsNo = len(pop[0])
    rate = random()%rate
    popSize = len(pop)
    limit = int(popSize * rate)

    for i in range(limit):
        r = randint(0, literalsNo - 1)
        pop[randint(2, popSize - 1)][r] = pop[i][r] * -1


def popFitness(pop, clauses, unsatClausesNo):
    fit = 0.0
    clausesNo = len(clauses)
    for i in range(len(pop)):
        fit = fit + (clausesNo - unsatClausesNo[i]) / float(clausesNo)

    return fit / len(pop)



def genetic(clauses, literalsNo, popSize, iterations, rate):
    clausesNo = len(clauses)
    iterations = 100
    pop = [0] * popSize

    start = timer()
    for i in range(popSize):
        pop[i] = randomSolution(literalsNo)
    end = timer()
    print("random solution generated in {}\n".format(timedelta(seconds=end-start)))
    
    lastBest = 0
    bestVal = 0

    for i in range(iterations):

        unsatClausesNo = []
        start = timer()
        for sol in pop:
            unsatClausesNo.append(checkUnsatisfiedClauses(clauses, sol))
        end = timer()
        print("unsatClausesNo generated in {}\n".format(timedelta(seconds=end-start)))


        start = timer()
        sortPop(clauses, pop, popSize, unsatClausesNo)
        end = timer()
        print("population sorted in {}\n".format(timedelta(seconds=end-start)))

        start = timer()
        bestVal = (len(clauses) - checkUnsatisfiedClauses(clauses[:], pop[0])) / float(len(clauses))
        end = timer()
        print("bestval determined in {}\n".format(timedelta(seconds=end-start)))

        if bestVal == 1:
            print(str(bestVal))
            return pop[0], bestVal

        start = timer()
        fitness = popFitness(pop, clauses, unsatClausesNo)
        end = timer()
        print("pop fitness determined in {}\n".format(timedelta(seconds=end-start)))

        print("Pop avg fitness = {} \n Best value = {}".format(fitness, bestVal))
        results.write("{}\n".format(fitness))

        start = timer()
        selectPop = select(clauses, pop, popSize, unsatClausesNo)
        end = timer()
        print("selection done in {}\n".format(timedelta(seconds=end-start)))

        start = timer()
        newPop = crossover(selectPop, popSize)
        end = timer()
        print("crossover done in {}\n".format(timedelta(seconds=end-start)))

        start = timer()
        mutate(newPop, rate)
        end = timer()
        print("mutation done in {}".format(timedelta(seconds=end-start)))

        pop = newPop

    sortPop(clauses, pop, popSize, unsatClausesNo)
    return pop[0], bestVal


results = open("results.txt", "a+")

clauses, literalNo = readCnfFile("clause1.cnf")
popSize = 50
iterations = 50
rate = 0.02

bestPop, bestVal = genetic(clauses, literalNo, popSize, iterations, rate)
print(bestVal)