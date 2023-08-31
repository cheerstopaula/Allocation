
from agent_utils import Agent
from item_utils import Item
import networkx as nx
import matplotlib.pyplot as plt

class Allocation:
    def __init__(self,items, agents, allocation, owners):
        '''
        Object Allocation has three parameters:
        - items: List of items that can be alllocated 
        - agents: List of agents who get the items
        - allocation: List of size len(agents)+1, with the current allocation of items
        - owners: list of size len(items) with the agents that own each of the items. 
        '''
        self.items=items
        self.agents=agents
        self.allocation=self.initialize_allocation(items, agents, allocation)
        self.owners=self.initialize_owners(items, owners)
        self.exchange_graph=self.initialize_exchange_graph()

    def initialize_allocation(self, items, agents,allocation):
        '''
        If an empty list is given as allocation, build list with the default initial allocation:
        - X[0] has all items
        - X[1]...X[len(agents)] are empty lists.
        '''
        if len(allocation)==0:
            items_copy=items.copy()
            allocation.append(items_copy)
            for i in range(len(agents)):
                allocation.append([])
            return allocation
        else:
            return allocation
    
    def initialize_owners(self,items, owners):
        '''
        If an empty list is given as owners, build list with the default ownership, in which every item is owned bu agent zero. 
        '''
        if len(owners)==0:
            for i in range(len(items)):
                owners.append([0])
            return owners
        else:
            return owners
    
        
    
    def initialize_exchange_graph(self):
        exchange_graph = nx.DiGraph()
        for i in range(len(self.items)):
            exchange_graph.add_node(i)
        t=i+1
        exchange_graph.add_node(t)
        for i in range(len(self.items)):
            i_owners=self.owners[i]
            for g in i_owners:
                if g==0:
                    exchange_graph.add_edge(i, t)
                elif g>0:
                    for j in range(len(self.items)):
                        if self.items[j].item_id!=self.items[i].item_id:
                            exchangable=self.agents[g-1].exchange_contribution(self.allocation[g],self.items[i],self.items[j])
                            if exchangable:
                                exchange_graph.add_edge(i, j)
        return exchange_graph

        #nx.draw(exchange_graph, with_labels = True)
        #plt.show()
        #plt.close()
    

        

   
