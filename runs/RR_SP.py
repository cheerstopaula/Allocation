# %%
from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin
from metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X
import matplotlib.pyplot as plt
import random
import numpy as np



items=generate_items_from_schedule('fall2023schedule-2.xlsx')
# for item in items:
#     print('Course:',item.item_id,'Timeslot:',item.timeslot,'Capacity:',item.capacity)
n=500
for seed in [0,1,2,3,4,5,6,7,8,9]:
    random.seed(seed)
    np.random.seed(seed)
    agents=gen_random_agents(n,items)
    for agent in agents:
        print(agent.id, 'cap:', agent.cap)
        print('desired items: ',agent.desired_items)
    X=round_robin(agents, items)
    np.savez(f'RR_{n}_{seed}.npz',X=X)
    X=SPIRE_algorithm(agents, items)
    np.savez(f'SP_{n}_{seed}.npz',X=X)





# %%
