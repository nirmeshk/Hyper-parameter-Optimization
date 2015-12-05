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
    # DTLZ 1,3,5,7 with 2,4,6,8 objectives and 10,20,40 decisions
    
    #for obj in [2, 4, 6, 8]
    #for dec in [10, 20, 40]

    for model in [DTLZ_1, DTLZ_3, DTLZ_5, DTLZ_7]:
        for optimizer in [ga]:
            model_instance =  model(m = 2, n = 10)    
            baseline_population, population = optimizer().optimize(model_instance)
            
            en = cal_loss(baseline_population, population, model_instance)
            if optimizer.__name__ == 'ga':
                k = 0
            else:
                k = 1
            rdiv[k].extend(en)
        print([rdiv])
        rdivDemo(rdiv)
        print ("\n\n")
