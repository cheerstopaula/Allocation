# %%
from allocation.agent_functions import Agent, gen_random_agents
from allocation.item_functions import generate_items_from_schedule
from allocation.allocation_functions import yankee_swap, SPIRE_algorithm, round_robin, original_yankee_swap, yankee_swap_hold_graph
from allocation.metric_functions import utilitarian_welfare, nash_welfare, EF, EF_1, EF_X
import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np



items=generate_items_from_schedule('fall2023schedule-2.xlsx')
# for item in items:
#     print('Course:',item.item_id,'Timeslot:',item.timeslot,'Capacity:',item.capacity)
n=500
for seed in [0]:
    random.seed(seed)
    np.random.seed(seed)
    agents=gen_random_agents(n,items)
    # G1=original_yankee_swap(agents, items, plot_exchange_graph=False)
    # G2=yankee_swap(agents, items, plot_exchange_graph=False)
    # G3=yankee_swap_hold_graph(agents, items, plot_exchange_graph=False)

    # print('original YS and regular: ', nx.is_isomorphic(G1,G2))
    # print('original YS and hold graph: ',nx.is_isomorphic(G1,G3))
    # print('regular and hold graph: ',nx.is_isomorphic(G2,G3))
    
    # for agent in agents:
    #     print(agent.id, 'cap:', agent.cap)
    #     print('desired items: ',agent.desired_items)
    # X2,time_steps2,agents_involved_arr2=original_yankee_swap(agents, items, plot_exchange_graph=False)
    # print('########################################')
    # X1,time_steps1,agents_involved_arr1=yankee_swap(agents, items, plot_exchange_graph=False)
    # print('########################################')
    X3,time_steps3,agents_involved_arr3=yankee_swap_hold_graph(agents, items, plot_exchange_graph=False)

    # print(np.count_nonzero(X1-X2))
    # print(np.count_nonzero(X1-X3))
    # print(np.count_nonzero(X2-X3))

    # print(utilitarian_welfare(X1,agents,items), utilitarian_welfare(X2,agents,items),utilitarian_welfare(X3,agents,items))
    # print(nash_welfare(X1,agents,items), nash_welfare(X2,agents,items),nash_welfare(X3,agents,items))
    # print(EF(X1,agents,items), EF(X2,agents, items),EF(X3,agents, items))

        # plt.plot(range(len(time_steps1)), time_steps1, color='C0', label='yankee swap')
        # plt.plot(range(len(time_steps2)), time_steps2, color='C1', label='original')
        # plt.plot(range(len(time_steps3)), time_steps3, color='C2', label='hold graph')
        # plt.legend()
        # plt.show()
# plt.imshow(X1-X2)
# plt.show()
    np.savez(f'YS_hold_{n}_{seed}.npz',X=X3,time_steps=time_steps3,num_agents_involved=agents_involved_arr3)



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
# items[0].capacity=1
# items[1].capacity=1
# items[20].capacity=1
# items[25].capacity=1
# items[30].capacity=1
# items[40].capacity=1
# items=[items[0], items[1],items[20],items[25], items[30], items[40]]


##Running the algorithms

# X=yankee_swap(agents, items, plot_exchange_graph=False)
# print('Yankee Swap Allocation')
# print(X)
# print('Utilitatian: ',utilitarian_welfare(X,agents,items))
# print('Nash: ',nash_welfare(X, agents,items))
# print('EF: ',EF(X, agents,items))
# print('EF_1: ',EF_1(X, agents,items))
# print('EF_X: ',EF_X(X, agents,items))
# X=round_robin(agents,items)
# print('Round Robin Allocation')
# print(X)
# print('Utilitatian: ',utilitarian_welfare(X,agents,items))
# print('Nash: ',nash_welfare(X, agents,items))
# print('EF: ',EF(X, agents,items))
# print('EF_1: ',EF_1(X, agents,items))
# print('EF_X: ',EF_X(X, agents,items))
# X=SPIRE_algorithm(agents,items)
# print(X)
# print('SPIRE Allocation')
# print('Utilitatian: ',utilitarian_welfare(X,agents,items))
# print('Nash: ',nash_welfare(X, agents,items))
# print('EF: ',EF(X, agents,items))
# print('EF_1: ',EF_1(X, agents,items))
# print('EF_X: ',EF_X(X, agents,items))


# %%
