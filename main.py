# %%
from agent_functions import Agent, gen_random_agents
from item_functions import generate_items_from_schedule
from allocation_functions import yankee_swap, SPIRE_algorithm, round_robin, original_yankee_swap, yankee_swap_hold_graph
import vignesh_allocation_functions
from metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X
import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np
import time



items=generate_items_from_schedule('fall2023schedule-2.xlsx')
# for item in items:
#     print('Course:',item.item_id,'Timeslot:',item.timeslot,'Capacity:',item.capacity)
n=2000
for seed in [0]:
    random.seed(seed)
    np.random.seed(seed)
    agents=gen_random_agents(n,items)

    # start = time.time()
    # X3,time_steps3,agents_involved_arr3=yankee_swap_hold_graph(agents, items, plot_exchange_graph=False)
    # mid = time.time()

    # mnw = 1
    # usw = 0
    # for i in range(len(agents)):
    #     mnw *= (np.sum(X3[j][i+1] for j in range(len(items))))**(1/n)
    #     usw += np.sum(X3[j][i+1] for j in range(len(items)))

    # print("Paula USW:", usw)
    # print("Paula MNW:", mnw)
    # print("Paula time:", mid-start)

    mid2 = time.time()

    Xv=vignesh_allocation_functions.yankee_swap(agents, items)
    end = time.time()

    mnw = 1
    for i in range(len(agents)):
        mnw *= (np.sum(Xv[i, :]))**(1/n)

    for i in range(len(agents)):
        bundle = [jdash for jdash in range(len(items)) if Xv[i, jdash] == 1]
        if(agents[i].valuation_new(bundle, items) != len(bundle)):
            print("Major error at", i)
    print("My MNW:", mnw)
    print("My YS:", end-mid2)


    # np.savez(f'YS_hold_{n}_{seed}.npz',X=X3,time_steps=time_steps3,num_agents_involved=agents_involved_arr3)
    # np.savez(f'YS_v_{n}_{seed}.npz',X=Xv)





# %%
