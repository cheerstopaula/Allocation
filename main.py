# %%
from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from metric_functions import utilitarian_welfare, nash_welfare
import random
import numpy as np
seed = 1
random.seed(seed)
np.random.seed(seed)


items=generate_items_from_schedule('fall2023schedule.xlsx')
print(len(items))

agents=gen_random_agents(100,items)
for agent in agents:
    print(agent.id, 'cap:', agent.cap)
    print('desired items: ',agent.desired_items)

# ####TEST EXAMPLE
# #Create agents with preferences 
# agent1=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id], 10)
# agent2=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id], 10)
# agent3=Agent('student1',[items[0].item_id, items[1].item_id], 10)
# agent4=Agent('student1',[items[0].item_id], 10)
# agents=[agent1, agent2,agent3, agent4]
# # #agents=[agent1, agent2,agent3, agent4,agent1, agent2,agent3, agent4,agent1, agent2,agent3, agent4]

# # for i in range(100):
# #      num=random.randint(0, 3)    
# #      agents.append(agents[num])

# #Generate reduced list of items with capacity of 1
# #Reduce capacities
# items[0].capacity=2
# items[1].capacity=2
# items[20].capacity=2
# items[25].capacity=2
# items[30].capacity=2
# items[40].capacity=2
# items=[items[0], items[1],items[20],items[25], items[30], items[40]]


X=yankee_swap(agents, items, plot_exchange_graph=False)
print('YS Allocation')
print(X)
print('utilitarian: ',utilitarian_welfare(X))
X=round_robin(agents,items)
print('RR allocation')
print(X)
print('utilitarian: ',utilitarian_welfare(X))
X=SPIRE_algorithm(agents,items)
print('SPIRE allocation')
print(X)
print('utilitarian: ',utilitarian_welfare(X))
#print(nash_welfare(X))
# %%
