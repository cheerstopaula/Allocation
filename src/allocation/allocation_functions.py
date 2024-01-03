from .agent_functions import Agent
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import time
from queue import Queue

    
'''Initializations functions: Players, Allocation Matrix, and Exchange Graph'''

def initialize_players(agents):
    players=[]
    for i in range(len(agents)):
        players.append(i)
    return players

def initialize_allocation_matrix(items, agents):
    n=len(items)
    m=len(agents)+1 
    X=np.zeros([n,m],dtype=int)
    for i in range(n):
        X[i][m-1]=items[i].capacity
    return X

def initialize_exchange_graph(items):
    exchange_graph = nx.DiGraph()
    for i in range(len(items)):
        exchange_graph.add_node(i)
    exchange_graph.add_node('t')
    for i in range(len(items)):
        exchange_graph.add_edge(i, 't')
    return exchange_graph

def get_max_items(items):
    max_items=0
    for i in range(len(items)):
        max_items+=items[i].capacity
    return max_items

# def initialize_factored_graph(items,agents):
#     exchange_graph = nx.DiGraph()
#     exchange_graph.add_node('t')
#     for i in range(len(items)):
#         exchange_graph.add_node(i)
#         if items[i].capacity>0:
#             exchange_graph.add_edge(i, 't')
#     for agent_index in range(1,len(agents)+1):
#         agent=agents[agent_index-1]
#         exchange_graph.add_node('s'+str(agent_index))
#         desired_items=agent.get_desired_items_indexes(items)
#         for desired_item in desired_items:
#             exchange_graph.add_edge('s'+str(agent_index), desired_item)
#     return exchange_graph


'''Pick agent functions'''

def pick_agent(X,max_items,items, agents,players):
    max_capacity=max_items
    for player in players:
        agent=agents[player]
        bundle=get_bundle_from_allocation_matrix(X, items, player)
        current_utility=agent.valuation(bundle)
        if current_utility<max_capacity:
                max_capacity=current_utility
                agent_picked=player
    return agent_picked

# def pick_agent_general_YS(X,items, agents,players,criteria,weights):
#     gain_list=get_gain_function(X,agents,items,players,criteria,weights)
#     gain_list=np.asarray(gain_list)
#     max_score_player_index=np.argmax(gain_list)
#     return players[max_score_player_index]

# def get_gain_function(X,agents,items,players,criteria,weights):
#     gain_list=[]
#     if criteria=='LorenzDominance':
#         for player in players:
#             agent=agents[player-1]
#             bundle = get_bundle_from_allocation_matrix(X, items, player)
#             val=agent.valuation(bundle)
#             gain_list.append(-val)
#     if criteria=='WeightedLeximin':
#         for player in players:
#             agent=agents[player-1]
#             bundle = get_bundle_from_allocation_matrix(X, items, player)
#             val=agent.valuation(bundle)
#             w_i=weights[player-1]
#             gain_list.append(-val/w_i)
#     if criteria=='WeightedNash':
#         M=2**(max(weights))
#         for player in players:
#             agent=agents[player-1]
#             bundle = get_bundle_from_allocation_matrix(X, items, player)
#             val=agent.valuation(bundle)
#             w_i=weights[player-1]
#             if val==0:
#                 gain_list.append(M)
#             else:
#                 gain_list.append((1+1/val)**w_i)
#     if criteria=='WeightedHarmonic':
#         for player in players:
#             agent=agents[player-1]
#             bundle = get_bundle_from_allocation_matrix(X, items, player)
#             val=agent.valuation(bundle)
#             w_i=weights[player-1]
#             gain_list.append(w_i/(val+1))
#     return gain_list

def get_gain_function(X,agents,items,agent_picked,criteria,weights):
    agent=agents[agent_picked]
    bundle=get_bundle_from_allocation_matrix(X,items, agent_picked)
    val=agent.valuation(bundle)
    if criteria=='LorenzDominance':
            return -val
    w_i=weights[agent_picked]
    if criteria=='WeightedLeximin':
        return -val/w_i
    if criteria=='WeightedNash':
        if val==0:
            return float('inf')
        else:
            return (1+1/val)**w_i
    if criteria=='WeightedHarmonic':
        return w_i/(val+1)
    
'''Retrieve information or update current allocation'''

def get_owners_list(X,item_index):
    item_list=X[item_index]
    owners_list=np.nonzero(item_list)
    return owners_list[0]

def get_bundle_from_allocation_matrix(X, items, agent_index):
    bundle0=[]
    items_list=X[:,agent_index]
    for i in range(len(items_list)):
        if int(items_list[i])==1:
            bundle0.append(items[i])
    return bundle0

def get_bundle_indexes_from_allocation_matrix(X, agent_index):
    bundle_indexes=[]
    items_list=X[:,agent_index]
    for i in range(len(items_list)):
        if int(items_list[i])==1:
            bundle_indexes.append(i)
    return bundle_indexes

def find_agent(agents,items,X,current_item_index,last_item_index):
    owners=get_owners_list(X,current_item_index)
    for owner in owners:
        agent=agents[owner]
        bundle=get_bundle_from_allocation_matrix(X,items,owner)
        if agent.exchange_contribution(bundle,items[current_item_index], items[last_item_index]):      
            return owner
    print('Agent not found') #this should never happen. If the item was in the path, then someone must be willing to exchange it

def update_allocation(X,path_og,agents,items,agent_picked):
    path=path_og.copy()
    path=path[1:-1]
    last_item=path[-1]
    agents_involved=[agent_picked]
    X[last_item,len(agents)]-=1
    while len(path)>0:
        last_item=path.pop(len(path)-1)
        # print('last item: ', last_item)
        if len(path)>0:
            next_to_last_item=path[-1]
            current_agent=find_agent(agents,items,X,next_to_last_item,last_item)
            agents_involved.append(current_agent)
            X[last_item,current_agent]=1
            X[next_to_last_item,current_agent]=0
        else:
            X[last_item,agent_picked]=1
        
    return X, agents_involved

'''Graph functions'''

def find_shortest_path(G,start,end):
    try:
        p = nx.shortest_path(G, source=start, target=end) 
        return p
    except:
        return False
    
# def find_shortest_path(G,start,end):
''' Implementation of BFS to find shortest path
    Dijsktra is faster as a networkx built-in function
'''
#     queue = deque([(start, [start])])
#     while queue:
#         current_node, path = queue.popleft()
#         if current_node == end:
#             # print(path)
#             return path

#         for neighbor in G.neighbors(current_node):
#             if neighbor not in path:
#                 new_path = path + [neighbor]
#                 queue.append((neighbor, new_path))
#     return False

def add_agent_to_exchange_graph(G,X,items,agents, agent_picked):
    G.add_node('s')
    bundle=get_bundle_from_allocation_matrix(X,items,agent_picked)
    agent=agents[agent_picked]
    for i in agent.get_desired_items_indexes(items):
        g=items[i]
        if g not in bundle:
            if agent.marginal_contribution(bundle,g)==1:
                G.add_edge('s', i)
    return G


def build_exchange_graph(X,items, agents):
    exchange_graph = nx.DiGraph()
    for i in range(len(items)):
        exchange_graph.add_node(i)
    exchange_graph.add_node('t')
    for item_index in range(len(items)):
        item_1=items[item_index]
        if X[item_index,len(agents)]>0:
            exchange_graph.add_edge(item_index, 't')
        owners=get_owners_list(X,item_index)
        for item_2_index in range(len(items)):
            if item_2_index!=item_index:
                item_2=items[item_2_index]
                exchangeable=False
                for owner in owners:
                    if owner!=0:
                        agent=agents[owner]        
                        bundle_owner=get_bundle_from_allocation_matrix(X, items, owner)
                        willing_owner=agent.exchange_contribution(bundle_owner,item_1, item_2)
                        if willing_owner:
                            exchangeable=True
                if exchangeable:
                    exchange_graph.add_edge(item_index,item_2_index)
    return exchange_graph

def get_multiple_agents_desired_items(agents_indexes,agents,items):
    lis=[]
    for agent_index in agents_indexes:
        agent=agents[agent_index]
        lis=lis+agent.get_desired_items_indexes(items)
    return list(set(lis))

def get_multiple_agents_bundles(agents_indexes,X):
    lis=[]
    for agent_index in agents_indexes:
        lis=lis+get_bundle_indexes_from_allocation_matrix(X,agent_index)
    return list(set(lis))


def update_exchange_graph(X,G,path_og,agents,items, agents_involved):
    path=path_og.copy()
    path=path[1:-1]
    last_item=path[-1]
    if X[last_item,len(agents)]==0:
        G.remove_edge(last_item,'t')
    agents_involved_desired_items=get_multiple_agents_desired_items(agents_involved,agents,items)
    agents_involved_bundles=get_multiple_agents_bundles(agents_involved, X)
    for item_idx in agents_involved_bundles:
        item_1=items[item_idx]
        owners=list(get_owners_list(X,item_idx))
        if len(agents) in owners:
            owners.remove(len(agents))
        owners_desired_items=get_multiple_agents_desired_items(owners,agents,items)
        items_to_loop_over=list(set(agents_involved_desired_items+owners_desired_items))
        for item_2_idx in items_to_loop_over:
            if item_2_idx!=item_idx:
                item_2=items[item_2_idx]
                exchangeable=False
                for owner in owners:
                    agent=agents[owner]       
                    bundle_owner=get_bundle_from_allocation_matrix(X, items, owner)
                    willing_owner=agent.exchange_contribution(bundle_owner,item_1, item_2)
                    if willing_owner:
                        exchangeable=True
                        break
                if exchangeable:
                    if not G.has_edge(item_idx, item_2_idx):
                        G.add_edge(item_idx,item_2_idx)
                else:
                    if G.has_edge(item_idx, item_2_idx):
                        G.remove_edge(item_idx,item_2_idx)
    return G

'''Allocation algorithms'''

def SPIRE_algorithm(agents, items):
    X=initialize_allocation_matrix(items, agents)
    agent_index=0
    for agent in agents:
        bundle=[]
        desired_items=agent.get_desired_items_indexes(items)
        for item in desired_items:
            if X[item,len(agents)]>0:
                current_val=agent.valuation(bundle)
                new_bundle=bundle.copy()
                new_bundle.append(items[item])
                new_valuation=agent.valuation(new_bundle)
                if new_valuation>current_val:
                    X[item,agent_index]=1
                    X[item,len(agents)]-=1
                    bundle=new_bundle.copy()
        agent_index+=1
    return X

def round_robin(agents, items):
    players=initialize_players(agents)
    X=initialize_allocation_matrix(items, agents)
    while len(players)>0:
        for player in players: 
            val=0
            current_item=[]
            agent=agents[player]
            desired_items=agent.get_desired_items_indexes(items)
            bundle=get_bundle_from_allocation_matrix(X, items, player)
            for item in desired_items:
                if X[item,len(agents)]>0:
                    current_val=agent.marginal_contribution(bundle,items[item])
                    if current_val>val:
                        current_item.clear()
                        current_item.append(item)
                        val=current_val
            if len(current_item)>0:
                X[current_item[0],player]=1
                X[current_item[0],len(agents)]-=1
            else:
                players.remove(player)
    return X

def round_robin_weights(agents, items, weights):
    players=initialize_players(agents)
    X=initialize_allocation_matrix(items, agents)
    weights_aux=weights.copy()
    while len(players)>0:
        weight=weights_aux[0]
        for player in players: 
            if weights[player]==weight:
                val=0
                current_item=[]
                agent=agents[player]
                desired_items=agent.get_desired_items_indexes(items)
                bundle=get_bundle_from_allocation_matrix(X, items, player)
                for item in desired_items:
                    if X[item,0]>0:
                        current_val=agent.marginal_contribution(bundle,items[item])
                        if current_val>val:
                            current_item.clear()
                            current_item.append(item)
                            val=current_val
                if len(current_item)>0:
                    X[current_item[0],player]=1
                    X[current_item[0],0]-=1
                else:
                    players.remove(player)
                    weights_aux.pop(0)
    return X

'''Instead of yankee_swap use general yankee swap with default parameters'''
# def yankee_swap(agents,items, plot_exchange_graph=False):
#     '''Vanilla Yankee Swap'''
#     players=initialize_players(agents)
#     X=initialize_allocation_matrix(items, agents)
#     G=initialize_exchange_graph(items)
#     if plot_exchange_graph:
#         nx.draw(G, with_labels = True)
#         plt.show()
#     max_items=get_max_items(items)
#     count=0
#     time_steps=[]
#     agents_involved_arr=[]
#     start=time.process_time()
#     while len(players)>0:
#         count+=1
#         agent_picked=pick_agent(X, max_items, items, agents,players)
#         print("Iteration: %d" % count, end='\r')
#         G=add_agent_to_exchange_graph(G,X,items,agents, agent_picked)
#         if plot_exchange_graph:
#             nx.draw(G, with_labels = True)
#             plt.show()

#         path = find_shortest_path(G,'s','t')
#         G.remove_node('s')

#         if path== False:
#             players.remove(agent_picked)
#             time_steps.append(time.process_time()-start)
#             agents_involved_arr.append(0)
#         else:
#             X, agents_involved=update_allocation(X,path,agents,items,agent_picked)
#             G=update_exchange_graph(X,G,path,agents,items, agents_involved)
#             if plot_exchange_graph:
#                 nx.draw(G, with_labels = True)
#                 plt.show()
#             time_steps.append(time.process_time()-start)
#             agents_involved_arr.append(len(agents_involved))
#     return X,time_steps,agents_involved_arr

def yankee_swap_hold_graph(agents,items, plot_exchange_graph=False):
    '''Vanilla Yankee Swap holding the generation of ex. graph until first transfer occurs'''
    players=initialize_players(agents)
    X=initialize_allocation_matrix(items, agents)
    graph=False
    max_items=get_max_items(items)
    count=0
    time_steps=[]
    agents_involved_arr=[]
    start=time.process_time()
    while len(players)>0:
        count+=1
        agent_picked=pick_agent(X, max_items, items, agents,players)
        if not graph:
            agent=agents[agent_picked]
            list_desired_items=agent.get_desired_items_indexes(items)
            bundle=get_bundle_from_allocation_matrix(X,items,agent_picked)
            empty_seat_found=False
            for desired_item in list_desired_items:
                if X[desired_item,0]>0 and agent.marginal_contribution(bundle,items[desired_item])>0:
                    X[desired_item,0]-=1
                    X[desired_item,agent_picked]+=1
                    time_steps.append(time.process_time()-start)
                    agents_involved_arr.append(1)
                    empty_seat_found=True
                    break
            if not empty_seat_found:
                graph=True
                G=build_exchange_graph(X,items, agents)
        if graph:
            G=add_agent_to_exchange_graph(G,X,items,agents, agent_picked)
            if plot_exchange_graph:
                nx.draw(G, with_labels = True)
                plt.show()

            path = find_shortest_path(G,'s','t')
            G.remove_node('s')

            if path== False:
                players.remove(agent_picked)
                time_steps.append(time.process_time()-start)
                agents_involved_arr.append(0)
            else:
                X, agents_involved=update_allocation(X,path,agents,items,agent_picked)
                G=update_exchange_graph(X,G,path,agents,items, agents_involved)
                if plot_exchange_graph:
                    nx.draw(G, with_labels = True)
                    plt.show()
                time_steps.append(time.process_time()-start)
                agents_involved_arr.append(len(agents_involved))
    return X,time_steps,agents_involved_arr

def original_yankee_swap(agents,items, plot_exchange_graph=False):
    '''Vanilla Yankee Swap building the ex. graph from scratch in every iteration'''
    players=initialize_players(agents)
    X=initialize_allocation_matrix(items, agents)
    G=build_exchange_graph(X,items,agents)
    if plot_exchange_graph:
        nx.draw(G, with_labels = True)
        plt.show()
    max_items=get_max_items(items)
    count=0
    time_steps=[]
    agents_involved_arr=[]
    start=time.process_time()
    while len(players)>0:
        count+=1
        print("Iteration: %d" % count, end='\r')
        agent_picked=pick_agent(X, max_items, items, agents,players)
        G=add_agent_to_exchange_graph(G,X,items,agents, agent_picked)
        if plot_exchange_graph:
            nx.draw(G, with_labels = True)
            plt.show()

        path = find_shortest_path(G,'s','t')
        G.remove_node('s')

        if path== False:
            players.remove(agent_picked)
            time_steps.append(time.process_time()-start)
            agents_involved_arr.append(0)
        else:
            X, agents_involved=update_allocation(X,path,agents,items,agent_picked)
            G=build_exchange_graph(X,items, agents)
            if plot_exchange_graph:
                nx.draw(G, with_labels = True)
                plt.show()
            time_steps.append(time.process_time()-start)
            agents_involved_arr.append(len(agents_involved))
    return X,time_steps,agents_involved_arr
            


def general_yankee_swap(agents,items, plot_exchange_graph=False,criteria='LorenzDominance',weights=0):
    '''General Yankee Swap'''
    players=initialize_players(agents)
    X=initialize_allocation_matrix(items, agents)    
    G=initialize_exchange_graph(items)
    gain_vector=np.zeros([len(agents)])
    count=0
    time_steps=[]
    agents_involved_arr=[]
    start=time.process_time()
    while len(players)>0:
        print("Iteration: %d" % count, end='\r')
        # print("Iteration: %d" % count)
        count+=1
        agent_picked=np.argmax(gain_vector)
        G=add_agent_to_exchange_graph(G,X,items,agents, agent_picked)
        if plot_exchange_graph:
            nx.draw(G, with_labels = True)
            plt.show()

        path = find_shortest_path(G,'s','t')
        G.remove_node('s')

        if path== False:
            players.remove(agent_picked)
            gain_vector[agent_picked]=float('-inf')
            time_steps.append(time.process_time()-start)
            agents_involved_arr.append(0)
        else:
            X, agents_involved=update_allocation(X,path,agents,items,agent_picked)
            G=update_exchange_graph(X,G,path,agents,items, agents_involved)
            gain_vector[agent_picked]=get_gain_function(X,agents, items, agent_picked,criteria,weights)

            if plot_exchange_graph:
                nx.draw(G, with_labels = True)
                plt.show()
            time_steps.append(time.process_time()-start)
            agents_involved_arr.append(len(agents_involved))
    return X,time_steps,agents_involved_arr



'''Vignesh's implementation'''

def find_desired(i, bundle, list_of_yes, agents, items):
    agenti = agents[i]
    list_of_yesses = list(list_of_yes.difference(bundle))
    low = 0
    high = len(list_of_yesses)
    if(agenti.valuation_index([*bundle, *list_of_yesses[low:high]], items) == len(bundle)):
        return -1
    while(high > low + 1):
        mid = int((low + high)/2)
        if(agenti.valuation_index([*bundle, *list_of_yesses[low:mid]], items) > len(bundle)):
            high = mid
        else: 
            low = mid
    return list_of_yesses[low]



def get_distances(i, agents, items, allocation_matrix):
    distances = {}
    previous_agent = {}
    previous_item = {}

    n = len(agents)
    m = len(items)

    if(np.sum(allocation_matrix[:,n]) == m):
        return -1, previous_agent, previous_item

    q = Queue()
    q.put(-1)

    list_of_yes = set(np.arange(m).flatten())

    while(not q.empty()):

        j = q.get()
        if(j == -1):
            # list_of_yesses =  list_of_yes.copy()
            bundle = [jdash for jdash in range(m) if allocation_matrix[jdash,i] == 1]
            jprime = find_desired(i, bundle, list_of_yes, agents, items)
            while(jprime != -1):
                list_of_yes.remove(jprime)
                if(jprime not in distances):
                    previous_item[jprime] = -1
                    previous_agent[jprime] = -1
                    distances[jprime] = 1
                    if(allocation_matrix[jprime,n] != 0):
                        return jprime, previous_agent, previous_item
                    q.put(jprime)
                jprime = find_desired(i, bundle, list_of_yes, agents, items)

        else:
            for iprime in [idash for idash in range(n) if allocation_matrix[j,idash] == 1]:
                # list_of_yesses =  list_of_yes.copy()
                bundle = [jdash for jdash in range(len(items)) if ((allocation_matrix[ jdash,iprime] == 1)&(jdash != j))]
                jprime = find_desired(iprime, bundle, list_of_yes, agents, items)
                while(jprime != -1):
                    list_of_yes.remove(jprime)
                    if(jprime not in distances):
                        previous_item[jprime] = j
                        previous_agent[jprime] = iprime
                        distances[jprime] = distances[j] + 1
                        if(allocation_matrix[jprime,n] != 0):
                            return jprime, previous_agent, previous_item
                        q.put(jprime)
                    jprime = find_desired(iprime, bundle, list_of_yes, agents, items)
    return -1, previous_agent, previous_item



def augment_path(i, item, previous_agent, previous_item, allocation_matrix, agents):

    n = len(agents)

    new_allocation_matrix = np.copy(allocation_matrix)
    item_to_move = item
    agent_to_move_from = n

    if(previous_agent[item_to_move] != -1):
        new_allocation_matrix[item_to_move,previous_agent[item_to_move]] = 1
        new_allocation_matrix[item_to_move,agent_to_move_from, ] -= 1

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    while(previous_agent[item_to_move] != -1):
        new_allocation_matrix[item_to_move,previous_agent[item_to_move]] = 1
        new_allocation_matrix[item_to_move,agent_to_move_from] = 0

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    new_allocation_matrix[item_to_move,i] = 1
    new_allocation_matrix[item_to_move,agent_to_move_from] -= 1

    return new_allocation_matrix


def bfs_yankee_swap(agents,items,criteria='LorenzDominance',weights=0):
    n = len(agents)
    m = len(items)
    count = 0

    #Initialize allocation matrix, players, and utility vector
    allocation_matrix = np.zeros((m,n+1),dtype=int)
    allocation_matrix[:,n] = np.array([int(items[j].capacity) for j in range(m)])
    U = set(np.arange(n).flatten())
    u_vector = np.zeros(n,dtype=int)
    utility_vector = np.zeros(n,dtype=float)

    while(len(U) != 0):
        count += 1
        print("Iteration: %d" % count, end='\r')
        agent_picked = np.argmin(utility_vector)
        item, previous_agent, previous_item = get_distances(agent_picked, agents, items, allocation_matrix)

        if(item != -1):
            allocation_matrix = augment_path(agent_picked, item, previous_agent, previous_item, allocation_matrix, agents)
            u_vector[agent_picked] += 1
            utility_vector[agent_picked] +=1
        else:
            utility_vector[agent_picked] = 10000*m
            U.remove(agent_picked)

    print("USW:", np.sum(u_vector))

    return allocation_matrix
            

