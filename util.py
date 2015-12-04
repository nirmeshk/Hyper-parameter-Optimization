def lt(i, j): return i < j

def gt(i, j): return i > j

class O():
  """
  Default class which everything extends.
  """
  def __init__(self, **d):
    self.has().update(**d)

  def has(self):
    return self.__dict__

  def update(self, **d):
    self.has().update(d)
    return self

  def __repr__(self):
    show = [':%s %s' % (k,self.has()[k])
      for k in sorted(self.has().keys())
      if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show=map(lambda x: '\t'+x+'\n',show)
    return '{'+' '.join(show)+'}'

  def __getitem__(self, item):
    return self.has().get(item)

  def __setitem__(self, key, value):
    self.has()[key] = value

def norm(x, low, high):
  """
  Method to normalize value
  between 0 and 1
  """
  nor = (x - low)/(high - low)
  if nor > 1:
    return 1
  elif nor < 0:
    return 0
  return nor
  
"""
Returns true if both are similar. i.e. terminate, no improvement
"""
def earlyTermination(prev_era, cur_era, model):
    prev_obj_score = [model.eval(can) for can in prev_era]
    cur_obj_score = [model.eval(can) for can in cur_era]
    
    eps = 0.01
    
    for i in range(model.m):
        prev_sum_obj_i = sum(o[i] for o in prev_obj_score)
        cur_sum_obj_i = sum(o[i] for o in cur_obj_score)
        loss = (prev_sum_obj_i - cur_sum_obj_i) if model.objs[i].better == lt else (cur_sum_obj_i - prev_sum_obj_i)
        
        if loss > eps * prev_sum_obj_i:
            return False
    
    return True
