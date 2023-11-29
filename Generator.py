import random
import math


def GenRandR():
    r = random.random()
    while r == 0 or r == 1:
        r = random.random()
    return r

def GenNormalRandVal():
    r1, r2 = GenRandR(), GenRandR()
    return math.sqrt(-2 * math.log(r1)) * math.cos(2*math.pi * r2)

def GenRandVal(norm_val, average, deviation):
    return average + norm_val * deviation * 0.5

def WriteToFile(average, deviation, N, filename):
    file = open(filename, 'w')
    for i in range(N):
        file.write(str(GenRandVal(GenNormalRandVal(), average, deviation)) + '\n')
    file.close()



"""if __name__ == '__main__':
    WriteToFile(10, 1, 10, 'test.txt')"""