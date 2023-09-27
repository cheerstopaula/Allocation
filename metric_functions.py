def utilitarian_welfare(X):
  util = 0
  for row in X:
    util += sum(row[1:]) #take out agent 0 that is the pile of unassigned items
  return util/(len(X[0])-1) #The number of agents is given by dim(X[(0)])-1, so as to not consider agent 0

def nash_welfare(X):
  util = 1
  num_zeros = 0
  for column in range(len(X[0])-1):
    c = sum(X[:,column+1])
    if (c == 0):
      numZeroes += 1
    else:
      util *= c
  return num_zeros, util/(len(X[0])-1-num_zeros)
