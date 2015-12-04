from __future__ import print_function, division
from models import *
from algorithms import *

if __name__ == '__main__':
   
    for model in [DTLZ_1]:#, DTLZ_3, DTLZ_7, DTLZ_5]:
        for optimizer in [ga]:
            optimizer().optimize(model(n=10, m=3))
        print ("\n\n")
