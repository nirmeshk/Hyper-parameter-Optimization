- Call the following method at each generation of your optimizer with the population at that generation.
- Keep the scale constant


```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

@staticmethod
def graph_it(population, model, scale):
    final_frontier = [ model.eval(can) for can in population ]
    # Create a directory with model name
    directory = model.__class__.__name__ + '/'
    
    # use epoch time as file name
    file_name = directory + str(int(time.time()))

    # Plot results only if 2 or 3 dimensional
    # Plot results
    f1 = np.array([x[0] for x in final_frontier])
    f2 = np.array([x[1] for x in final_frontier])
    f3 = np.array([x[2] for x in final_frontier])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(f1, f2, f3, s = 40, color = '#000080', alpha=0.80)
    ax.set_xlim((0, scale[0]))
    ax.set_ylim((0, scale[1]))
    ax.set_zlim((0, scale[2]))
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')
    ax.set_zlabel('f3')
    fig.savefig(file_name)
```

- Once you the optimization is done, your folder will contain multiple .png files , sorted according to timestamp.
- Run `convert *.png DTLZ_1.gif` inside the folder.This will create a nice GIF animation by combining all the images.
- Reference of convert tool: http://manpages.ubuntu.com/manpages/dapper/man1/convert.1.html
- Note: It is availale by default in OSX