# %%
from agent_utils import Agent
from item_utils import generate_items_from_schedule
from allocation_utils import yankee_swap
import random
import numpy as np
seed = 123
random.seed(seed)
np.random.seed(seed)


items=generate_items_from_schedule('fall2023schedule.xlsx')


####TEST EXAMPLE
#Create agents with preferences 
agent1=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id], 10)
agent2=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id], 10)
agent3=Agent('student1',[items[0].item_id, items[1].item_id], 10)
agent4=Agent('student1',[items[0].item_id], 10)
agents=[agent1, agent2,agent3, agent4]


#Generate reduced list of items with capacity of 1
#Reduce capacities
items[0].capacity=1
items[1].capacity=1
items[20].capacity=1
items[25].capacity=1
items[30].capacity=1
items[40].capacity=1
items2=[items[0], items[1],items[20],items[25], items[30], items[40]]


X=yankee_swap(agents, items2, plot_exchange_graph=True)
print(X)


# %%
