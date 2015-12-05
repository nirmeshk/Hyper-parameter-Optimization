from __future__ import print_function, division
from models import *
from algorithms import *
from util import *

"""
Calculates loss between baseline era and final era. 
Returns an array of losses
"""
def cal_loss(baseline_population, population, model):
#     base_energy = [model.energy(can) for can in baseline_population]
    pop_energy = [model.energy(can) for can in population]
    
    converge(baseline_population, population, model)
       
    return pop_energy
    

if __name__ == '__main__':
   
    for model in [DTLZ_1]:#, DTLZ_3, DTLZ_7, DTLZ_5]:
        rdiv = [['ga'],['de']]
        model = model(n=10, m=3)
        for optimizer in [ga, de]:            
            baseline_population, population = optimizer().optimize(model)
            en = cal_loss(baseline_population, population, model)
            if optimizer.__name__ == 'ga':
                k = 0
            else:
                k = 1
            rdiv[k].extend(en)
        print([rdiv])
        rdivDemo(rdiv)
        print ("\n\n")
