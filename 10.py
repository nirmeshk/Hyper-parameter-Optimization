from __future__ import print_function, division
from models import *
from algorithms import *

"""
Calculates loss between baseline era and final era. 
Returns an array of losses
"""
def cal_loss(baseline_population, population, model):
#     base_energy = [model.energy(can) for can in baseline_population]
#     pop_energy = [model.energy(can) for can in population]
    print ('baseline :', [baseline_population])
    print ('frontier: ', [population])
    print ('model: ', type(model))
    
#     return pop_energy

if __name__ == '__main__':   
    for model in [GA_MODEL]:#, DTLZ_3, DTLZ_7, DTLZ_5]:
        dtlz1 = DTLZ_1(n=10, m=3)
        model = model(dtlz1)
        for optimizer in [de]:
            baseline_population, population = optimizer().optimize(model)
#             en = cal_loss(baseline_population, population, model)
#             print(en)

        print ("\n\n")
