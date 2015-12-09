#### Contributors:
- Nirmesh Khandelwal
- Anand Bora
- Ravi Singh

### Abstract:
Genetic Algorithm is a class of Evolutionay algorithms used for optimizing multiobjective models. Genetic Algorithm is inspired by real life evolution. The basic idea is to try to generate better ppopulation by selection, crossover and mutation of current memebers of population. The main difficulty faced by optimizers is that it is difficult to get a good optimization before you know the problem charectristic or landscape. As a part of this experiment, we try to implement a GA and analyse its behaviour on various DTLZ models. 

### GA Algorithm implementation
Here is what we did:

- Generate a random population in the start.
- Sort the entire population based on their domination scores in increasing order. A domination score of candidate 'a' is number of other candidates that dominate 'a'.
- Choose first x% and last y% from the sorted population to be parents for next generation. 
- Produce `total_population_size - len(parents)` new children by select , crossover and mutate among parents. 
- parents + new children contitute next generation.




Here is the little animation for DTLZ 1 - 7 with following settings:
```
Settings: 
{   
  :better lt
    :candidates 500
    :era 100
    :gens 500
    :mutate_prob 0.25
    :patience 3       # For early termination
    :lives 3          # For early termination
    :retain 0.33      # % of parents that we retain for next generation
}
```



- DTLZ_1 ![DTLZ_1 Optimization using GA](http://i.imgur.com/BISkpyY.gifv) 
- DTLZ_3 ![DTLZ_3](http://i.imgur.com/KjtuaQd.gif) 
- DTLZ_5 ![DTLZ_5](http://i.imgur.com/XZlNEIw.gif)
- DTLZ_7 ![DTLZ_7](http://i.imgur.com/MbjngQ6.gif)  

|Model Name   |  Decisions  | Objectives  | Final Divergence | Final Best Energy | Hypervolume |
|-------------|-------------|-------------|------------------|-------------------|-------------|
| DTLZ_1      | 10          | 2           |                  | ||
