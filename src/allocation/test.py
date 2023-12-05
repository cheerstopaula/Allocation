import numpy as np
def check_allocation_matrix(X, items):
    sum_X=np.sum(X, axis=1)
    capacities=np.asarray([item.capacity for item in items])
    return np.count_nonzero(sum_X-capacities)==0