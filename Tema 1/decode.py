import numpy

def decode(binary_numbers, a, b, L):
    
    arrs = split(binary_numbers[:], L)
    returnArr = []
    
    for arr in arrs:
        x = 0
        for val in arr:
            x *= 2
            x += val

        x = x / (2 ** L - 1)
        x *= (b - a)
        x += a

        returnArr.append(x)

    return returnArr

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs