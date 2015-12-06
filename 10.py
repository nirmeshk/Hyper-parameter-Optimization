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
    for model in [GA_MODEL]:
        dtlz1 = DTLZ_1(n=5, m=2)
        model = model(dtlz1)
        for optimizer in [de]:
            baseline_population, population = optimizer().optimize(model)
            
            population = [x for x in population if x.objs_score is not None]
            population.sort(key = lambda can: can.objs_score)
            for can in population:
                for dec_info, dec in zip(model.decs, can.decs):
                    print(dec_info.name,' = ', dec)
                print('Divergence Score = ', can.objs_score)                    
                print('#'*30)                    
            
        print ("\n\n")