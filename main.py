# %%
from agent_utils import Agent
from item_utils import generate_items_from_schedule, get_bundle_from_allocation_matrix
from allocation_utils import initialize_allocation_matrix, initialize_exchange_graph, add_agent_to_exchange_graph, find_shortest_path, update_allocation
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
seed = 123
random.seed(seed)
np.random.seed(seed)


items=generate_items_from_schedule('fall2023schedule.xlsx')
# agent1=Agent('student1',[items[0].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id, items[50].item_id], 10)
# agent2=Agent('student2',[items[1].item_id,  items[20].item_id, items[30].item_id,items[45].item_id,items[48].item_id, items[50].item_id], 10)
# agent3=Agent('student3',[items[0].item_id,  items[20].item_id, items[30].item_id,items[45].item_id,items[48].item_id, items[50].item_id], 10)
agent1=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id,items[25].item_id,items[40].item_id], 10)
agent2=Agent('student1',[items[0].item_id, items[1].item_id,  items[20].item_id, items[30].item_id], 10)
agent3=Agent('student1',[items[0].item_id, items[1].item_id], 10)
agent4=Agent('student1',[items[0].item_id], 10)
agents=[agent1, agent2,agent3, agent4]


#Reduce capacities
items[0].capacity=1
items[1].capacity=1
items[20].capacity=1
items[25].capacity=1
items[30].capacity=1
items[40].capacity=1

#Define reduced list of items
items2=[items[0], items[1],items[20],items[25], items[30], items[40]]


#initialize allocation and exchange_graph
X=initialize_allocation_matrix(items2, agents)
print(X)
G=initialize_exchange_graph(items2)
nx.draw(G, with_labels = True)
plt.show()


#Pick an agent 
agent_picked=1
G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
nx.draw(G, with_labels = True)
plt.show()


#Find shortest path
path = find_shortest_path(G)

# remove the agent picked and all those edges
G.remove_node('s')

item_picked=path[len(path)-2]
print('item taken from unnasigned pile: ',item_picked)

X,G=update_allocation(X,G,path,agents,items2,agent_picked)
nx.draw(G, with_labels = True)
print(X)
plt.show()



# #Add edges from that item to the corresponding ones according to the new owner
# for i in range(len(items2)):
#     g=items2[i]
#     bundle=get_bundle_from_allocation_matrix(X,items2,agent_picked)
#     if i!=item_picked:
#         if agents[agent_picked-1].exchange_contribution(bundle,items2[item_picked],g)==1:
#             G.add_edge(item_picked, i)

# nx.draw(G, with_labels = True)
# plt.show()

# #Check if theres still capacity in the class that was taken. 
# if sum(X[item_picked])> items2[item_picked].capacity:
#     G.remove_edge(item_picked,'t')
#     X[item_picked,0]=0

# print(X)


# nx.draw(G, with_labels = True)
# plt.show()






####START FROM SCRATCHHHHH
#Pick an agent 
agent_picked=4
G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)

nx.draw(G, with_labels = True)
plt.show()

path = find_shortest_path(G)
print(path)

X,G=update_allocation(X,G,path,agents,items2,agent_picked)
nx.draw(G, with_labels = True)
print(X)
plt.show()



# %%
