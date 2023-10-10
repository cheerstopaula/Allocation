from allocation_functions import get_bundle_from_allocation_matrix
from agent_functions import Agent
import numpy as np

def utilitarian_welfare(X, agents,items):
    util = 0
    for agent_index in range(len(agents)):
        agent=agents[agent_index]
        bundle=get_bundle_from_allocation_matrix(X,items,agent_index+1)
        val=agent.valuation(bundle)
        util += val
    return util/(len(agents)) #The number of agents is given by dim(X[(0)])-1, so as to not consider agent 0


def nash_welfare(X, agents,items):
    util = 0
    num_zeros = 0
    for agent_index in range(len(agents)):
        agent=agents[agent_index]
        bundle=get_bundle_from_allocation_matrix(X,items,agent_index+1)
        val=agent.valuation(bundle)
        if (val== 0):
            num_zeros+= 1
        else:
            util += np.log(val)
    return num_zeros, np.exp(util/(len(agents)-num_zeros))

def EF(X, agents,items):
    envy_count=0
    for agent_index in range(len(agents)):
        for agent_2_index in range(len(agents)):
            if agent_index!=agent_2_index:
                agent=agents[agent_index]
                current_bundle=get_bundle_from_allocation_matrix(X,items,agent_index+1)
                other_bundle=get_bundle_from_allocation_matrix(X,items,agent_2_index+1)
                current_utility=agent.valuation(current_bundle)
                other_utility=agent.valuation(other_bundle)
                if current_utility<other_utility:
                    envy_count+=1
    return envy_count

def leximin(X,agents,items):
    valuations=[]
    for agent_index in range(len(agents)):
        agent=agents[agent_index]
        bundle=get_bundle_from_allocation_matrix(X,items,agent_index+1)
        val=agent.valuation(bundle)
        valuations.append(val)
    valuations.sort()
    valuations.reverse()
    return valuations


