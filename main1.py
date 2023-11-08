# %%
from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin, original_yankee_swap, yankee_swap_hold_graph
from metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X
import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np



items=generate_items_from_schedule('fall2023schedule-2.xlsx')
n=500
for seed in [0]:
    random.seed(seed)
    np.random.seed(seed)
    agents=gen_random_agents(n,items)


    data_def=np.load(f'YS_default_{n}_{seed}.npz')
    X_def=data_def['X']
    time_steps_def=data_def['time_steps']
    num_agents_involved_def=data_def['num_agents_involved']

    data_bfs=np.load(f'YS_bfs_{n}_{seed}.npz')
    X_bfs=data_bfs['X']
    time_steps_bfs=data_bfs['time_steps']
    num_agents_involved_bfs=data_bfs['num_agents_involved']

    data_og=np.load(f'YS_og_{n}_{seed}.npz')
    X_og=data_og['X']
    time_steps_og=data_og['time_steps']
    num_agents_involved_og=data_og['num_agents_involved']

    data_hold=np.load(f'YS_hold_{n}_{seed}.npz')
    X_hold=data_hold['X']
    time_steps_hold=data_hold['time_steps']
    num_agents_involved_hold=data_hold['num_agents_involved']

    print(np.count_nonzero(X_def-X_bfs))
    print(np.count_nonzero(X_def-X_og))
    print(np.count_nonzero(X_def-X_hold))
    print(np.count_nonzero(X_bfs-X_og))
    print(np.count_nonzero(X_bfs-X_hold))
    print(np.count_nonzero(X_og-X_hold))

    print(utilitarian_welfare(X_hold,agents,items), utilitarian_welfare(X_def,agents,items),utilitarian_welfare(X_bfs,agents,items),utilitarian_welfare(X_og,agents,items))
    print(nash_welfare(X_hold,agents,items), nash_welfare(X_def,agents,items),nash_welfare(X_bfs,agents,items),nash_welfare(X_og,agents,items))
    print(EF(X_hold,agents,items), EF(X_def,agents, items),EF(X_bfs,agents, items),EF(X_og,agents, items))

print('done')
plt.plot(range(len(time_steps_og)),num_agents_involved_og,color='C3', label='original')
plt.plot(range(len(time_steps_hold)),num_agents_involved_hold,color='C0', label='hold graph')
plt.plot(range(len(time_steps_def)),num_agents_involved_def,color='C1', label='dijstra')
plt.plot(range(len(time_steps_bfs)),num_agents_involved_bfs,color='C2', label='bfs')
plt.legend()
plt.show()

# %%
