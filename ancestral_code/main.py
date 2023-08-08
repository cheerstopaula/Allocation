# %%
import pandas as pd
import numpy as np
from inputs import  get_schedule, genMany
from allocation_utils import YankeeSwap,RoundRobin,SpireAlloc
from metrics import getNash, getUtilitarian
from plots import plot_instances

class Agent:
    def __init__(self,id, valuations):
        self.id=id
        self.valuations=valuations

    
#if __name__ == '__main__':
classes = pd.read_excel('fall2023schedule.xlsx')
topics,instructors,numClasses,schedule,slots =get_schedule(classes)
n = 50
nseeds=4

plot_instances(classes, topics,instructors,numClasses,schedule,slots, n,nseeds)


# students = genMany(n, topics, instructors, numClasses,20)
# spire = SpireAlloc([3 for x in students], students, [x for x in students], [3 for y in students[0]])
# ## Three students,3 classes, student 1: wants a,b, 2: wants a,c, 3: wants a,c
# roundRobin = RoundRobin([3 for x in students], students, [x for x in students], list(classes["Enrl Capacity"]),
#                         slots)
# yankee = YankeeSwap([3 for x in students], students, list(classes["Enrl Capacity"]), slots)

# print("SPIRE", getUtilitarian(spire))
# print("round robin", getUtilitarian(roundRobin))
# print("yankee", getUtilitarian(yankee))

# print("SPIRE", getNash(spire))
# print("round robin", getNash(roundRobin))
# print("yankee", getNash(yankee))

# %%