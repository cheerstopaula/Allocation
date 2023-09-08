
from agent_utils import Agent
from item_utils import Item, get_bundle_from_allocation_matrix
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

    

def initialize_allocation_matrix(items, agents):
    n=len(items)
    m=len(agents)+1 
    X=np.zeros([n,m])
    for i in range(n):
        X[i][0]=1
    return X

def initialize_exchange_graph(items):
    exchange_graph = nx.DiGraph()
    for i in range(len(items)):
        exchange_graph.add_node(i)
    t=i+1
    exchange_graph.add_node('t')
    for i in range(len(items)):
        exchange_graph.add_edge(i, 't')
    return exchange_graph

def add_agent_to_exchange_graph(G,X,items,agents, agent_picked):
    G.add_node('s')
    bundle=get_bundle_from_allocation_matrix(X,items,agent_picked)

    for i in range(len(items)):
        g=items[i]
        if agents[agent_picked-1].marginal_contribution(bundle,g)==1:
            G.add_edge('s', i)
    return G

def find_shortest_path(G):
    try:
        p = nx.shortest_path(G, source='s', target='t') 
        return p
    except:
        return False

def find_agent(agents,items,X,current_item,last_item):
    for i in range(len(agents)):
        bundle=get_bundle_from_allocation_matrix(X,items,i)
        if agents[i].exchange_contribution(bundle,current_item, last_item):
            return i+1
    print('Agent not found')

def get_owners_list(X,item_index):
    item_list=X[item_index]
    owners_list=np.nonzero(item_list)
    return owners_list[0]

def update_allocation(X,G,path,agents,items,agent_picked):
    path=path[1:-1]
    last_item=path[-1]
    if sum(X[last_item])>= items[last_item].capacity:
        G.remove_edge(last_item,'t')
        X[last_item,0]=0
    while len(path)>0:
        last_item=path.pop(len(path)-1)
        if len(path)>0:
            next_to_last_item=path[-1]
            current_agent=find_agent(agents,items,X,items[next_to_last_item],items[last_item])
            X[last_item,current_agent]=1
            X[next_to_last_item,current_agent]=0
        else:
            X[last_item,agent_picked]=1

        owners_list=get_owners_list(X,last_item)
        for owner in owners_list:
            for i in range(len(items)):
                item=items[i]
                agent=agents[int(owner)-1]
                bundle=get_bundle_from_allocation_matrix(X, items, owner)
                exchangeable=agent.exchange_contribution(bundle,items[last_item], item)
                if exchangeable:
                    if not G.has_edge(last_item, i):
                        if last_item!=i:
                            G.add_edge(last_item,i)
                else:
                    if G.has_edge(last_item, i):
                        G.remove_edge(last_item,i)
    return X,G




        
    

