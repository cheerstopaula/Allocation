def getUtilitarian(X):
  util = 0
  for i in X:
    util += sum(i)
  return util/len(X)

'''
Nash Welfare
This functions returns a tuple with the number of students with 0 utility and the normalized product of all nonzero agent utilities
'''
def getNash(X):
  util = 1
  numZeroes = 0
  for i in X:
    c = sum(i)
    if (c == 0):
      numZeroes += 1
    else:
      util *= c
  return numZeroes, util #take the log to view in a nicer format