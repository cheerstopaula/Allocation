
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

def find_agent(agents,items,X,current_item,last_item,current_item_index):
    #this could be made more efficiently, by going through only the owners and not every owner
    for i in range(len(agents)):
        bundle=get_bundle_from_allocation_matrix(X,items,i+1)
        if int(X[current_item_index,i+1]==1):
           if agents[i].exchange_contribution(bundle,current_item, last_item):        
                return i+1
    print('Agent not found')

def get_owners_list(X,item_index):
    item_list=X[item_index]
    owners_list=np.nonzero(item_list)
    return owners_list[0]

def update_allocation(X,path_og,agents,items,agent_picked):
    path=path_og.copy()
    path=path[1:-1]
    last_item=path[-1]
    if sum(X[last_item])>= items[last_item].capacity:
        X[last_item,0]=0
    while len(path)>0:
        last_item=path.pop(len(path)-1)
        #print('last item: ', last_item)
        if len(path)>0:
            next_to_last_item=path[-1]
            #print('next to last item: ', next_to_last_item)
            current_agent=find_agent(agents,items,X,items[next_to_last_item],items[last_item],next_to_last_item)
            #print('current agent: ', current_agent)
            X[last_item,current_agent]=1
            X[next_to_last_item,current_agent]=0
        else:
            X[last_item,agent_picked]=1
    return X


def update_exchange_graph(X,G,path_og,agents,items):
    path=path_og.copy()
    path=path[1:-1]
    last_item=path[-1]
    if sum(X[last_item])>= items[last_item].capacity:
        G.remove_edge(last_item,'t')
    while len(path)>0:
        last_item=path.pop(len(path)-1)
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
    return G

def get_max_items(items):
    max_items=0
    for i in range(len(items)):
        max_items+=items[i].capacity
    return max_items

def initialize_players(agents):
    players=[]
    for i in range(len(agents)):
        players.append(i+1)
    return players

def pick_agent(X,max_items, players):
    max_capacity=max_items
    for i in range(len(X[0])-1):
        if sum(X[:,i+1])<max_capacity:
            if i+1 in players:
                max_capacity=sum(X[:,i+1])
                agent_picked=i+1
    return agent_picked

def yankee_swap(agents,items, plot_exchange_graph):
    ## Initialize players, allocation, exchange_graph, and max utility
    players=initialize_players(agents)
    X=initialize_allocation_matrix(items, agents)
    print('Initial allocation:')
    print(X)
    G=initialize_exchange_graph(items)
    if plot_exchange_graph:
        nx.draw(G, with_labels = True)
        plt.show()
    max_items=get_max_items(items)
    ## Run Yankee Swap
    count=0
    while len(players)>0:
        count+=1
        print('STEP', count)
        agent_picked=pick_agent(X, max_items, players)
        print('Agent picked:',agent_picked)
        G=add_agent_to_exchange_graph(G,X,items,agents, agent_picked)
        if plot_exchange_graph:
            nx.draw(G, with_labels = True)
            plt.show()

        path = find_shortest_path(G)
        print('path found:', path)
        G.remove_node('s')
        
        if path== False:
            players.remove(agent_picked)
        else:
            #Given the path found, update allocation and exchange graph
            X=update_allocation(X,path,agents,items,agent_picked)
            G=update_exchange_graph(X,G,path,agents,items)
            print('Current allocation:')
            print(X)
            if plot_exchange_graph:
                nx.draw(G, with_labels = True)
                plt.show()
    return X
            

    

