
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
    current_value = len(bundle)
    if(agenti.valuation_new([*bundle, *list_of_yesses[low:high]], items) == current_value):
        return -1
    while(high > low + 1):
        mid = int((low + high)/2)
        if(agenti.valuation_new([*bundle, *list_of_yesses[low:mid]], items) > current_value):
            high = mid
        else: 
            low = mid
    return list_of_yesses[low]


def binary_breadth_first_search(i, agents, items, allocation_matrix, inverse_allocation_matrix, list_of_yes):
    distances = {}
    previous_agent = {}
    previous_item = {}

    n = len(agents)
    m = len(items)

    if(np.sum(allocation_matrix[n, :]) == 0):
        return -1, previous_agent, previous_item, list_of_yes


    q = Queue()
    q.put(-1)

    # list_of_yes = set(np.arange(m).flatten())

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
                        return jprime, previous_agent, previous_item, list_of_yes
                    q.put(jprime)
                jprime = get_good_item(i, bundle, list_of_yes, agents, items)

        else:
            for iprime in inverse_allocation_matrix[j]:
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
                            return jprime, previous_agent, previous_item, list_of_yes
                        q.put(jprime)
                    jprime = get_good_item(iprime, bundle, list_of_yes, agents, items)

    return -1, previous_agent, previous_item, list_of_yes


def augment_path(i, item, previous_agent, previous_item, allocation_matrix, agents, inverse_allocation_matrix):

    n = len(agents)

    new_allocation_matrix = np.copy(allocation_matrix)
    new_inverse_allocation_matrix = inverse_allocation_matrix.copy()
    item_to_move = item
    agent_to_move_from = n

    if(previous_agent[item_to_move] != -1):
        new_allocation_matrix[previous_agent[item_to_move], item_to_move] = 1
        new_inverse_allocation_matrix[item_to_move].add(previous_agent[item_to_move])
        new_allocation_matrix[agent_to_move_from, item_to_move] -= 1

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    while(previous_agent[item_to_move] != -1):
        new_allocation_matrix[previous_agent[item_to_move], item_to_move] = 1
        new_inverse_allocation_matrix[item_to_move].add(previous_agent[item_to_move])
        new_allocation_matrix[agent_to_move_from, item_to_move] = 0
        new_inverse_allocation_matrix[item_to_move].remove(agent_to_move_from)

        agent_to_move_from = previous_agent[item_to_move]
        item_to_move = previous_item[item_to_move]

    new_allocation_matrix[i, item_to_move] = 1
    new_inverse_allocation_matrix[item_to_move].add(i)
    new_allocation_matrix[agent_to_move_from, item_to_move] -= 1
    if(agent_to_move_from!= n):
        new_inverse_allocation_matrix[item_to_move].remove(agent_to_move_from)

    return new_allocation_matrix, new_inverse_allocation_matrix

        


     

def yankee_swap(agents,items):
    n = len(agents)
    m = len(items)
    count = 0


    u_vector = np.zeros(n,dtype=int)
    useful_u_vector = np.zeros(n,dtype=int)
    allocation_matrix = np.zeros((n+1, m),dtype=int)
    allocation_matrix[n, :] = np.array([int(items[j].capacity) for j in range(m)])
    inverse_allocation_matrix = [set() for i in range(m)]

    list_of_yes = set(np.arange(m).flatten())


    U = set(np.arange(n).flatten())
    while(len(U) != 0):
        count += 1
        print("Iteration: %d" % count, end='\r')
        i = np.argmin(useful_u_vector)

        item, previous_agent, previous_item, list_of_yes = binary_breadth_first_search(i, agents, items, allocation_matrix, inverse_allocation_matrix, list_of_yes)

        if(item != -1):
            allocation_matrix, inverse_allocation_matrix = augment_path(i, item, previous_agent, previous_item, allocation_matrix, agents, inverse_allocation_matrix)
            u_vector[i] += 1
            useful_u_vector[i] +=1
            list_of_yes = set(np.arange(m).flatten())
        else:
            useful_u_vector[i] = 10000*m
            U.remove(i)

    print()
    print("Vignesh YS USW:", np.sum(u_vector))

    return allocation_matrix
            


            

    

