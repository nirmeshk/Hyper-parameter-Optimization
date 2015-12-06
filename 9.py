from __future__ import print_function, division
from models import *
from algorithms import *
from util import * 
import logging

if __name__ == '__main__':
    # DTLZ 1,3,5,7 with 2,4,6,8 objectives and 10,20,40 decisions
    
    #for obj in [2, 4, 6, 8]
    #for dec in [10, 20, 40]


    for model in [DTLZ_1, DTLZ_3, DTLZ_5, DTLZ_7]:
        for optimizer in [ga]:
            with open('out/' + model.__name__ + '_' + str(2) + '_' + str(10), 'w+') as fp:
                model_instance =  model(m = 2, n = 10)    
                baseline_population, population = optimizer(fp=fp).optimize(model_instance)      
                c = divergence_from_baseline(baseline_population, population, model_instance)
                log_base_and_final(baseline_population, population, model_instance, fp)
                fp.write("divergence_from_baseline:{}".format(c))
                fp.write('\n')
