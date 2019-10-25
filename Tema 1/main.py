import searchmethods as sm
import decode
import functions as fn
import sys

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

methods = {
    1: sm.simulatedAnnealing,
    2: sm.hillClimb
}

output = open("results.txt", "a+")

minimum = 100000

#output.write("{}, {} dimensiuni\n".format(str(functions[int(sys.argv[4])]), int(sys.argv[3])))
#for i in range(30):
 #   minimum = 100000
  #  for j in range(10):
   #     x, pars = methods[int(sys.argv[1])](int(sys.argv[2]), int(sys.argv[3]), functions[int(sys.argv[4])], float(sys.argv[5]), float(sys.argv[6]), str(sys.argv[7]))
    #    if x < minimum:
     #       minimum = x

    #output.write("{} at {}\n".format(minimum, decode.decode(pars, a, b, L)))
    
#for f in [1, 2, 3, 4]:


for f in [1, 2, 3, 4]:
    for d in [2, 5]:
        output.write("{}, {} dimensiuni, best improvement\n".format(functions[f], d))
        
        for t in range(30):
            minimum = 10000000
            for tt in range(200):
                result, points = sm.hillClimb(bits[f], d, functions[f], AB[f][0], AB[f][1], "best")
                if result < minimum:
                    minimum = result
            output.write("{} {}\n".format(t+1, minimum))
            print("{}, best, function {}, {} params. Found minimum of {}".format(t+1, f, d, minimum))

        output.write("{}, {} dimensiuni, first improvement\n".format(functions[f], d))
        for t in range(30):
            minimum = 10000000
            for tt in range(200):
                result, points = sm.hillClimb(bits[f], d, functions[f], AB[f][0], AB[f][1], "first")
                if result < minimum:
                    minimum = result
            output.write("{} {}\n".format(t+1, minimum))
            print("{}, first, function {}, {} params. Found minimum of {}".format(t+1, f, d, minimum))

        output.write("{}, {} dimensiuni, annealing\n".format(functions[f], d))
        for t in range(1000):
            minimum = 10000000
            for tt in range(1):
                result, points = sm.simulatedAnnealing(bits[f], d, functions[f], AB[f][0], AB[f][1], "b")
                if result < minimum:
                    minimum = result
            output.write("{} {}\n".format(t+1, minimum))
        print("annealing succesful")

#print(methods[int(sys.argv[1])](int(sys.argv[2]), int(sys.argv[3]), functions[int(sys.argv[4])], float(sys.argv[5]), float(sys.argv[6]), str(sys.argv[7])))