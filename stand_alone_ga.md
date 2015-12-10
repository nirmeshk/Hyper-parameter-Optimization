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

- Here is the basic code for the implementation (Just for explanation purpose):
```python
def GA(model):
	population = [model.generate() for _ in pop_size]
	
	for _ in range(number_of_gen):
		population.sort(key = lambda can: can.domination_score)
		parents = population[:x] + population[-y:]        # Keep top x% and bottom y%
		next_gen = parents[:]

		while len(next_gen)  < len(population):
			papa, mama = select(parents)
			son = crossover(papa, mama)
			son = mutate(son)
			next_gen.append(son)

		population = next_gen[:]
```

### Experimentation:

- Basic setup configuration:

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

- In order to know if the algorithm is working correctly, we used some visual pointers.
- Here are some of the problems that we faced and how we improved on them:
	+ **Binary domination vs Continuous domination issues:** we noticed that for 2-3 objetives, the bdom works fine. But as we move to higher dimensional space, the binary domination is not able to figure out the comparison between two candidates. So finally, we switched to continuous domination and it worked well.
	+ **Lack of variation (spread) in population because of Elite sampling:** Initially, we were choosing top x% of the population to be parents for next generation. Because of that, everything was converging to single point or small cluster. In order to solve this problem, we decided to choose some bad parents along with elites for next gen. This increased the spread of the solution. 
	+ **A good metric for comparing the results:** 
		- Hypervolume is a good metric. So we have used that. The problem with hypervolume is that, it is hard to know how far have we moved from baseline population after optimization. 
		- We were not able to use the spread as it requires True pareto frontiers for the problems. Jmetal website only provides two PF for few objectives.
		- A good metric is convergence to True pareto frontier. It is average distance of your frontier from the True PF. The problem is again, we do not have True PF for all the problems.
		- So in order to solve this problem, we came up with the `divergence score`. Diverence score is how far we came from the baseline: It is average distance of your frontier from the baseline population. This can be used as we have both baseline and final frontier available with us. Also, it does not require any True PF.

- Some visual aids that helped in deciding if we are going in correct direction. Here is the link on how to produce these animation [link](animations.md):

	+ DTLZ_1 ![DTLZ_1 Optimization using GA](http://i.imgur.com/BISkpyY.gifv) 
	+ DTLZ_3 ![DTLZ_3](http://i.imgur.com/KjtuaQd.gif) 
	+ DTLZ_5 ![DTLZ_5](http://i.imgur.com/XZlNEIw.gif)
	+ DTLZ_7 ![DTLZ_7](http://i.imgur.com/MbjngQ6.gif)  

### Results:
All the raw outputs can be found inside the folder `out/` . Here is the summary results

|Model Name   |  Decisions  | Objectives  | Final Divergence | Final Best Energy | Hypervolume |
|-------------|-------------|-------------|------------------|-------------------|-------------|
| DTLZ_1      | 10          | 2           | 64.9650607772    | ||
| DTLZ_1      | 30          | 2           | 317.831749634    | ||
| DTLZ_1      | 40          | 2           | 160.574922758    | ||
| DTLZ_1      | 10          | 3           | 122.950686056    | ||
| DTLZ_1      | 10          | 4           | 109.689910168    | ||
| DTLZ_1      | 10          | 6           | 90.509442913     | ||
| DTLZ_1      | 10          | 8           | 58.359461992     | ||
| DTLZ_3      | 10          | 2           | 135.721350287    | ||
| DTLZ_3      | 30          | 2           | 760.204008197    | ||
| DTLZ_3      | 40          | 2           | 903.483315609    | ||
| DTLZ_3      | 10          | 3           | 191.609929704    | ||
| DTLZ_3      | 10          | 4           | 158.073500707    | ||
| DTLZ_3      | 40          | 4           | 408.348147997    | ||
| DTLZ_5      | 10          | 2           | 0.00334231350105 | ||
| DTLZ_5      | 30          | 2           | 0.00168772790637 | ||
| DTLZ_5      | 40          | 2           | 0.00298688944974 | ||
| DTLZ_5      | 10          | 3           | 0.0144046707116  | ||
| DTLZ_7      | 10          | 2           | 1.31402313099    | ||
| DTLZ_7      | 30          | 2           | 2.01828183581    | ||
| DTLZ_7      | 40          | 2           | 2.36317104143    | ||
| DTLZ_7      | 10          | 3           | 1.75300752713    | ||
| DTLZ_7      | 40          | 4           | 3.19608899722    | ||

### Future Work:
The the parameters of GA to see which configuaration works best.
