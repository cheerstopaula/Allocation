# %%
from agent_utils import Agent
from item_utils import generate_items_from_schedule
from allocation_utils import Allocation
import networkx as nx
import matplotlib.pyplot as plt


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

#X=Allocation(items2, agents, [[items[1],items[40]],[items[0],items[20]],[items[25]],[items[30]]],[[1],[0],[1],[2],[3],[0]])


#Initialize allocation
X=Allocation(items2, agents, [],[])

#Pick an agent 
agent_picked=1
s=len(items2)+1
X.exchange_graph.add_node(s)
for i in range(len(items2)):
    g=items2[i]
    if agents[agent_picked-1].marginal_contribution(X.allocation[agent_picked],g)==1:
        X.exchange_graph.add_edge(s, i)

#nx.draw(X.exchange_graph, with_labels = True)
p = nx.shortest_path(X.exchange_graph, source=s, target=6) 
#print(p)
#plt.show()

# remove the agent picked and all those edges
X.exchange_graph.remove_node(s)
#nx.draw(X.exchange_graph, with_labels = True)
#plt.show()

#Next to last node in the path is always going to be the item taken from the unnasigned pile
item_picked=p[len(p)-2]
print('item taken from unnasigned pile: ',item_picked)
#Add item to the allocation of agent_picked
X.allocation[agent_picked].append(items2[item_picked])
print('Allocation', X.allocation)
#add agent to the list of agents owning each item
X.owners[item_picked].append(agent_picked)
print('Owners:', X.owners)
#Add edges from that item to the correspoing ones according to the new owner
for i in range(len(items2)):
    g=items2[i]
    if i!=item_picked:
        if agents[agent_picked-1].exchange_contribution(X.allocation[agent_picked-1],items2[item_picked],g)==1:
            X.exchange_graph.add_edge(item_picked, i)




#reduce the capacity by one (a seat from the class was taken)
items2[item_picked].capacity+=-1
print('reduce item capacity: ',items2[item_picked].capacity)
print(len(X.allocation))
#if the capacity is reduced to zero, remove item from unassigned pile, agent 0 from owners, and edge from item_picked to t

if items2[item_picked].capacity==0:
    X.owners[0].remove(item_picked)
    X.exchange_graph.remove_edge(item_picked,s-1)
    print('AAA', item_picked, s-1)
    for i in range(len(X.allocation[0])):
        g=X.allocation[0][i]
        if g.item_id==items2[item_picked].item_id:
            X.allocation[0].pop(i)
            break
        
print('Allocation', X.allocation)
print('Owners:', X.owners)

nx.draw(X.exchange_graph, with_labels = True)
plt.show()



#Lets now pick a different agent, say agent 4, so we need to force to take item 0 from agent 1
agent_picked=4
s=len(items2)+1
X.exchange_graph.add_node(s)
print(s)
for i in range(len(items2)):
    g=items2[i]
    if agents[agent_picked-1].marginal_contribution(X.allocation[agent_picked-1],g)==1:
        X.exchange_graph.add_edge(s, i)

p = nx.shortest_path(X.exchange_graph, source=s, target=6) 
print(p)
nx.draw(X.exchange_graph, with_labels = True)
plt.show()
