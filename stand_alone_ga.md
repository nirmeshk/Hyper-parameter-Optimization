#### Contributors:
- Nirmesh Khandelwal
- Anand Bora
- Ravi Singh

#### Summary
- As a part of this experiment, we tried to implement A simple GA and analyse its behaviour on various DTLZ models.
- Part of this experiment, we tried to analyse the behaviour of GA on DTLZ using the animation.


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
