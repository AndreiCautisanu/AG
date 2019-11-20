import numpy
import random
import genetic as g
import functions as fn

functions = {
    1: fn.rast,
    2: fn.rosembrock,
    3: fn.ackley,
    4: fn.dixonprice
}

AB = {
    1: fn.rastAB,
    2: fn.rosenbrockAB,
    3: fn.ackleyAB,
    4: fn.dixonpriceAB
}

bits = {
    1: fn.rastBits,
    2: fn.rosenbrockBits,
    3: fn.ackleyBits,
    4: fn.dixonpriceBits
}

pop = [[numpy.random.randint(2) for __ in range(34)] for _ in range(100)]
# popcpy = pop
# popcpy = g.mutate(pop)
# print(popcpy)
# popcpy = g.mutate(pop)
# print(popcpy)
# popcpy = g.mutate(pop)
# print(popcpy)
# popcpy = g.mutate(pop)
# print(popcpy)
# popcpy = g.mutate(pop)
# print(popcpy)
# popcpy = g.mutate(pop)
# print(popcpy)
# print(type(popcpy))

generations = 0

# print(pop[1])

while generations <= 100:
    generations += 1

    pop = g.mutate(pop)

    newpop = [0 for _ in range(100)]
    newpop[0] = pop[g.getBest(pop, fn.rast, -5.12, 5.12, 17)]

    for i in range(1, len(newpop)):
        newpop[i] = g.select(pop, fn.rast, -5.12, 5.12, 17)

    pop = newpop
    for i in range(100):
        print(fn.rast(fn.decode(pop[i], -5.12, 5.12, 17)), end=" ")
    print("\n")
    


