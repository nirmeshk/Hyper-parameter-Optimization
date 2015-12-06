from __future__ import print_function, division
from models import *
from algorithms import *
import logging

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
    logging.basicConfig(filename='10.log',filemode='w+', level=logging.INFO)

    for model in [GA_MODEL]:
        dtlz1 = DTLZ_1(n=5, m=2)
        model = model(dtlz1)
        for optimizer in [de]:
            baseline_population, population = optimizer().optimize(model)
            
            population = [x for x in population if x.objs_score is not None]
            population.sort(key = lambda can: can.objs_score, reverse = True)
            for can in population:
                for dec_info, dec in zip(model.decs, can.decs):
                    logging.info(str(dec_info.name + ' = ' + str(dec)))
                logging.info('Divergence Score = ' + str(can.objs_score))                    
                logging.info(str('#'*30))                    
            
        print ("\n\n")