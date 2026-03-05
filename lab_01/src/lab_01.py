import math
from scipy.spatial.distance import cityblock

with open ("/Users/candreavictor/IA/txtfile/input.txt","r") as f:
    a = f.readline().strip().split(",")
    b = f.readline().strip().split(",")

    print("a:",a)
    print("b:",b)
    final = 0

    if len(a) == len(b):
        for i in range(len(a)):
            dist =  math.fabs(float(a[i]) - float(b[i]))
            final = final + dist
distanta = cityblock([float(x) for x in a],[float(x) for x in b])
print("Distanta manhattan este:",final)
print("Distanta manhattan cu scipy este:",distanta)