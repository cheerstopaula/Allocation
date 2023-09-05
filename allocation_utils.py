
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
            return i
    print('Agent not found')

#def unpdate_allocation(X,path,agents,items):