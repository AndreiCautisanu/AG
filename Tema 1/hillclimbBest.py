import numpy
import decode as d
import functions as f

def neighbor(bitString, pos):
    tmp = bitString[:]
    tmp[pos] = int(not(bitString[pos]))
    
    return tmp