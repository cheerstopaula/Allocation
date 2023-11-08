# %%
from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin, original_yankee_swap, yankee_swap_hold_graph, general_yankee_swap
from metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X
import matplotlib.pyplot as plt
import random
import numpy as np



items=generate_items_from_schedule('fall2023schedule.xlsx')

#Create agents with preferences 
agent1=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id], 10)
agent2=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id], 10)
agent3=Agent('student1',[items[0].item_id, items[1].item_id], 10)
agent4=Agent('student1',[items[0].item_id], 10)
agent5=Agent('student1',[items[0].item_id,items[40].item_id], 10)
agents=[agent1, agent2,agent3, agent4, agent5]

#Generate reduced list of items with capacity of 1
#Reduce capacities
items[0].capacity=1
items[1].capacity=1
items[20].capacity=1
items[25].capacity=1
items[30].capacity=1
items[40].capacity=1
items=[items[0], items[1],items[20],items[25], items[30], items[40]]


#Running the algorithms

X=general_yankee_swap(agents, items, criteria='WeightedLeximin',weights=[1,2,3,4,5])
print('Yankee Swap Allocation')
print(X)
X=general_yankee_swap(agents, items)
print('Yankee Swap Allocation')
print(X)
X=yankee_swap_hold_graph(agents, items)
print('Yankee Swap Allocation')
print(X)



# %%
