import numpy
import functions as f

mutateProb = 0.01
cxProb = 0.3

def fitness(pop, func, a, b, L):
    funcVals = [func(f.decode(pop[i], a, b, L)) for i in range(len(pop))]
    #fitnessArr = [1.1 * max(funcVals) - funcVals[i] for i in range(len(pop))]

    fitnessArr = [1 / funcVals[i]**2 for i in range(len(pop))]

    return fitnessArr

def mutate(pop):
    popCopy = list(pop)

    for chr in popCopy:
        for pos in range(len(chr)):
            rnd = numpy.random.uniform(0, 1)
            if rnd < mutateProb:
                chr[pos] = int(not(chr[pos]))

    return popCopy

def select(pop, func, a, b, L):

    fits = fitness(pop, func, a, b, L)

    fitnessSum = sum(fits)

    randomFitness = numpy.random.uniform(0, fitnessSum)
    runningSum = 0

    for i in range(len(fits)):
        runningSum += fits[i]
        if runningSum > randomFitness:
            return pop[i]

def getBest(pop, func, a, b, L):
    fits = fitness(pop, func, a, b, L)

    return fits.index(max(fits))

def crossover(pop, n, L):
    cxProb = 0.3

    pass
    