
from agent_functions import Agent
import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import time
from queue import Queue


def get_good_item(i, bundle, list_of_yes, agents, items):
    agenti = agents[i]
    list_of_yesses = list(list_of_yes.difference(bundle))
    low = 0
    high = len(list_of_yesses)
    if(agenti.valuation_new([*bundle, *list_of_yesses[low:high]], items) == len(bundle)):
        return -1
    while(high > low + 1):
        mid = int((low + high)/2)
        if(agenti.valuation_new([*bundle, *list_of_yesses[low:mid]], items) > len(bundle)):
            high = mid
        else: 
            low = mid
    return list_of_yesses[low]



def binary_breadth_first_search(i, agents, items, allocation_matrix):
    distances = {}
    previous_agent = {}
    previous_item = {}

    n = len(agents)
    m = len(items)

    if(np.sum(allocation_matrix[n, :]) == m):
        return -1, previous_agent, previous_item


    q = Queue()
    q.put(-1)

    list_of_yes = set(np.arange(m).flatten())

    while(not q.empty()):

        j = q.get()
        if(j == -1):
            # list_of_yesses =  list_of_yes.copy()
            bundle = [jdash for jdash in range(m) if allocation_matrix[i, jdash] == 1]

            jprime = get_good_item(i, bundle, list_of_yes, agents, items)
            while(jprime != -1):
                list_of_yes.remove(jprime)
                if(jprime not in distances):
                    previous_item[jprime] = -1
                    previous_agent[jprime] = -1
                    distances[jprime] = 1
                    if(allocation_matrix[n, jprime] != 0):
                        return jprime, previous_agent, previous_item
                    q.put(jprime)
                jprime = get_good_item(i, bundle, list_of_yes, agents, items)

        else:
            for iprime in [idash for idash in range(n) if allocation_matrix[idash, j] == 1]:
                # list_of_yesses =  list_of_yes.copy()
                bundle = [jdash for jdash in range(len(items)) if ((allocation_matrix[iprime, jdash] == 1)&(jdash != j))]
                jprime = get_good_item(iprime, bundle, list_of_yes, agents, items)
                while(jprime != -1):
                    list_of_yes.remove(jprime)
                    if(jprime not in distances):
                        previous_item[jprime] = j
                        previous_agent[jprime] = iprime
                        distances[jprime] = distances[j] + 1
                        if(allocation_matrix[n, jprime] != 0):
                            return jprime, previous_agent, previous_item
                        q.put(jprime)
                    jprime = get_good_item(iprime, bundle, list_of_yes, agents, items)

    return -1, previous_agent, previous_item



def augment_path(i, item, previous_agent, previous_item, allocation_matrix, agents):

    n = len(agents)

    new_allocation_matrix = np.copy(allocation_matrix)
    item_to_move = item
    agent_to_move_from = n

    if(previous_agent[item_to_move] != -1):
        new_allocation_matrix[previous_agent[item_to_move], item_to_move] = 1
        new_allocation_matrix[agent_to_move_from, item_to_move] -= 1

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    while(previous_agent[item_to_move] != -1):
        new_allocation_matrix[previous_agent[item_to_move], item_to_move] = 1
        new_allocation_matrix[agent_to_move_from, item_to_move] = 0

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    new_allocation_matrix[i, item_to_move] = 1
    new_allocation_matrix[agent_to_move_from, item_to_move] -= 1

    return new_allocation_matrix

        


     


def yankee_swap(agents,items):
    n = len(agents)
    m = len(items)
    count = 0


    u_vector = np.zeros(n,dtype=int)
    useful_u_vector = np.zeros(n,dtype=int)
    allocation_matrix = np.zeros((n+1, m),dtype=int)
    allocation_matrix[n, :] = np.array([int(items[j].capacity) for j in range(m)])


    U = set(np.arange(n).flatten())
    while(len(U) != 0):
        count += 1
        print("Iteration: %d" % count, end='\r')
        i = np.argmin(useful_u_vector)

        item, previous_agent, previous_item = binary_breadth_first_search(i, agents, items, allocation_matrix)

        if(item != -1):
            allocation_matrix = augment_path(i, item, previous_agent, previous_item, allocation_matrix, agents)
            u_vector[i] += 1
            useful_u_vector[i] +=1
        else:
            useful_u_vector[i] = 10000*m
            U.remove(i)

    print()
    print("Vignesh YS USW:", np.sum(u_vector))

    return allocation_matrix
            


            

    

