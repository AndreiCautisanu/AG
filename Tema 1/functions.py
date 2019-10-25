import math

def ackley(arg_list):
    sum1 = 0
    sum2 = 0
    a = 20
    b = 0.2
    c = 2 * math.pi

    for x in arg_list:
        sum1 += x**2
        sum2 += math.cos(c * x)
    
    term1 = -a * math.exp(-b * math.sqrt(sum1/len(arg_list)))
    term2 = -math.exp(sum2/len(arg_list))

    return term1 + term2 + a + math.exp(1)

#############################################

def dixonprice(arg_list):
    term1 = (arg_list[0] - 1)**2

    sum = 0
    for i in range(1, len(arg_list)):
        sum += (i+1) * (2 * arg_list[i]**2 - arg_list[i-1])**2

    return term1 + sum

##############################################

def rast(arg_list):
    sum = 0
    l = len(arg_list)
    for x in arg_list:
        sum = sum + (x**2 - 10 * math.cos(2*math.pi*x))
    return 10 * l + sum

###############################################

def rosembrock(arg_list):
    sum = 0

    for i in range(0, len(arg_list) - 1):
        sum += 100*(arg_list[i+1] - arg_list[i]**2)**2 + (arg_list[i] - 1)**2

    return sum