
from agent_utils import Agent
from item_utils import Item
import networkx as nx
import matplotlib.pyplot as plt

class Allocation:
    def __init__(self,items, agents, allocation):
        '''
        Object Allocation has three parameters:
        - items: List of items that can be alllocated 
        - agents: List of agents who get the items
        - allocation: List of size len(agents)+1, with the current allocation of items
        '''
        self.items=items
        self.agents=agents
        self.allocation=self.initialize_allocation(items, agents, allocation)

    def initialize_allocation(self, items, agents,allocation):
        '''
        If an empty list is given as allocation, build list with the default initial allocation:
        - X[0] has all items
        - X[1]...X[len(agents)] are empty lists.
        '''
        if len(allocation)==0:
            allocation.append(items)
            for i in range(len(agents)):
                allocation.append([])
            return allocation
        else:
            return allocation
    
    def initialize_exchange_graph(self):
        exchange_graph = nx.DiGraph()
        for i in range(len(self.items)):
            exchange_graph.add_node(i)
        for i in range(len(self.items)):
            g=self.find_owner(self.items[i])
            if g>0:
                vg=self.agents[g-1].valuation(self.allocation[g])
                for j in range(len(self.items)):
                    if self.items[j].item_id!=self.items[i].item_id:
                        #write function to get the valuation of the bundle minus g and plus j
                        vj=self.agents[g-1].valuation(self.allocation[g])


        #nx.draw(exchange_graph, with_labels = True)
        #plt.show()
        #plt.close()
    
    def find_owner(self, item):
        '''
        Given an Allocation, find the current owner of a particular item, and return its index
        (If the item cannot be found, return False. This should never happen)
        '''
        for i in range(len(self.allocation)):
            for j in range(len(self.allocation[i])):
                if self.allocation[i][j].item_id==item.item_id:
                    return i
        return False

        

   
