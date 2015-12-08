#### Contributors:
- Nirmesh Khandelwal
- Anand Bora
- Ravi Singh

#### Summary
- As a part of this experiment, we used Differential Evolution (DE) to tune default "magic" parameters for Genetic Algorithms (GA).

#### Design Considerations:
- We used DE algorithm with following default settings: 
```
  Settings: 
    {	
      f = 0.75,         # extrapolate amount
      max = 50,         # number of repeats 
      np = 10,          # number of candidates
      cf = 0.3,         # prob of cross-over 
      epsilon = 0.01,
    }
```
- In order to optimize the GA algorithm, we created a GA model with four decisions and one objective 
  - Four decisions of GA model are the magic parameters of GA algorithm to be tuned.
```
        Decision(name="gens", low=200, high=600)
        Decision(name="era", low=50, high=200)
        Decision(name="retain", low=0.1, high=0.5)
        Decision(name="mutate_prob", low=0.25, high=0.75)
```
  - Single objective function of GA model, initializes an instance of GA algorithm with the decisions and passes the actual model we intend to optimize to GA algorithm. GA algorithm returns returns the final population. The objective function returns the "divergence distance" of the final population with the baseline population.  
- Note that all instances of GA algorithm are optimized with the same baseline population.
- At the end of the runs of DE, we get a frontier of tuned GAs. To compare it with untuned GA, we choose an untuned GA with magic parameters as the mean of individual decisions. Example: "gens" have low and high of 200 and 600 respectively, and untuned GA had "gens" set to 400.  

### Challenges:
- Slow performance of GA
- Used some form of memmoization to speedup things little bit. And it helped!!
  - Normally when we optimize a model, we do not care about "caching" objective scores as objecitve scores were some sort of mathematical function of decisions, and fairly fast calculations. But in this case, objective function of GA model calls an instance of GA algorithm and "caching" these values saved a lot of time. 
- Difficult to debug even small mistakes: seed of random, keeping same baseline population for all ga optimized by DE.
- A good objective score to measure for 1) Early termination 2) Comparing different GA optimizers.
- Even tried some easy models, but those models lack interesing results as they are easily optimized in very few generations. Also, the GA code n*n was the main culprit after we did some profiling.

### Results:
We observed that tuned GAs performed better than untuned GA.
We ran it for DTLZ1 (2 objectives and 5 decisions) and for GA algorithm for 80 and 200 candidate sizes.


|Model Name   |  Decisions  | Objectives  | Final Divergence | Final Best Energy | Hypervolume |
|-------------|-------------|-------------|------------------|-------------------|-------------|
| DTLZ_1      | 10          | 2           |   64.96506       |   3.37297         |  743671.4183|


### Future Work:
- Optimize the algorithm to make it faster. 
- GA Model is currently a single objective function. We might consider modifications to make it a multi-objective model and consider other properties from GA algorithm population such as Energy.
