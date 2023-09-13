# %%
from agent_utils import Agent
from item_utils import generate_items_from_schedule, get_bundle_from_allocation_matrix
from allocation_utils import initialize_allocation_matrix, initialize_exchange_graph, add_agent_to_exchange_graph, find_shortest_path, update_allocation, update_exchange_graph
import networkx as nx
import matplotlib.pyplot as plt
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


#### Yankee Swap exercise! ####
## Initialize allocation and exchange_graph
X=initialize_allocation_matrix(items2, agents)
print('Initial allocation: ',X)
G=initialize_exchange_graph(items2)
nx.draw(G, with_labels = True)
plt.show()

## Step 1
#Pick an agent and add to the exchange graph
agent_picked=1
G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
nx.draw(G, with_labels = True)
plt.show()

#Find shortest path from the agent to the pile of unasigned goods
path = find_shortest_path(G)
print(path)

#Remove the agent picked and all outcoming edges from it
G.remove_node('s')

#Given the path found, update allocation and exchange graph
X=update_allocation(X,path,agents,items2,agent_picked)
G=update_exchange_graph(X,G,path,agents,items2)

nx.draw(G, with_labels = True)
print(X)
plt.show()

## Step 2
#Pick an agent 
agent_picked=4
G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
nx.draw(G, with_labels = True)
plt.show()

#Find shortest path
path = find_shortest_path(G)
print(path)
G.remove_node('s')

#Update allocation and exchange graph
#Given the path found, update allocation and exchange graph
X=update_allocation(X,path,agents,items2,agent_picked)
G=update_exchange_graph(X,G,path,agents,items2)

nx.draw(G, with_labels = True)
print(X)
plt.show()

# ## Step 3
# #Pick an agent 
# agent_picked=3
# G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
# nx.draw(G, with_labels = True)
# plt.show()

# #Find shortest path
# path = find_shortest_path(G)
# print(path)
# G.remove_node('s')

# #Update allocation and exchange graph
# X,G=update_allocation(X,G,path,agents,items2,agent_picked)
# nx.draw(G, with_labels = True)
# print(X)
# plt.show()


# ## Step 4
# #Pick an agent 
# agent_picked=2
# G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
# nx.draw(G, with_labels = True)
# plt.show()

# #Find shortest path
# path = find_shortest_path(G)
# print(path)
# G.remove_node('s')

# #Update allocation and exchange graph
# X,G=update_allocation(X,G,path,agents,items2,agent_picked)
# nx.draw(G, with_labels = True)
# print(X)
# plt.show()

# ## Step 5
# #Pick an agent 
# agent_picked=1
# G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
# nx.draw(G, with_labels = True)
# plt.show()

# #Find shortest path
# path = find_shortest_path(G)
# print(path)
# G.remove_node('s')

# #Update allocation and exchange graph
# X,G=update_allocation(X,G,path,agents,items2,agent_picked)
# nx.draw(G, with_labels = True)
# print(X)
# plt.show()



# ## Step 5
# #Pick an agent 
# agent_picked=4
# G=add_agent_to_exchange_graph(G,X,items2,agents, agent_picked)
# nx.draw(G, with_labels = True)
# plt.show()

# #Find shortest path
# path = find_shortest_path(G)
# print(path)
# G.remove_node('s')
# %%
