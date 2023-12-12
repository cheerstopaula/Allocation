from .item_functions import Item
import random

class Agent:
    def __init__(self,id, desired_items, cap):
        '''
        Object Agent has three parameters:
        - id: Agent id (not really necessary or used at the moment, might be useful when assigning priority for example)
        - desired classes: list of item objects (from class Item) that the Agent values. If on this list, item gives 
                          Agent a utility of 1, if not on the list, utility of 0.
        - cap: maximum amount of items the agent can have 
        '''
        self.id=id
        self.desired_items=desired_items
        self.cap=cap

    def get_desired_items_indexes(self,items):
        desired_items_indexes=[]
        for item_index in range(len(items)):
            if items[item_index].item_id in self.desired_items:
                desired_items_indexes.append(item_index)
        return desired_items_indexes
    
    def valuation_index(self,bundle, items):   
        '''
        Compute the utility the agent gets from a particular bundle of items 

        @param bundle: list of items (from class Item)
        @return: utility given to the agent by that bundle (int)
        '''
        # T=bundle.copy()
        # # x=[*range(len(bundle))]
        # # x.reverse()
        # for g in bundle:
        #     if items[g].item_id not in self.desired_items:
        #         T.remove(g)
        slots=set()
        for g in bundle:
            if items[g].item_id in self.desired_items:
                slots.add(items[g].timeslot)
        return min(len(slots), self.cap)


    # def valuation(self,bundle):   
    #     '''
    #     Compute the utility the agent gets from a particular bundle of items 

    #     @param bundle: list of items (from class Item)
    #     @return: utility given to the agent by that bundle (int)
    #     '''
    #     T=bundle.copy()
    #     x=[*range(len(bundle))]
    #     x.reverse()
    #     for i in x:
    #         g=bundle[i]
    #         if g.item_id not in self.desired_items:
    #             T.pop(i)
    #     slots=[]
    #     for i in range(0,len(T)):
    #         slots.append(T[i].timeslot)
    #     slots=set(slots)
    #     return min(len(slots), self.cap)

    def valuation(self,bundle):   
        '''
        Compute the utility the agent gets from a particular bundle of items 

        @param bundle: list of items (from class Item)
        @return: utility given to the agent by that bundle (int)
        '''
        # T=bundle.copy()
        # # x=[*range(len(bundle))]
        # # x.reverse()
        # for g in bundle:
        #     if items[g].item_id not in self.desired_items:
        #         T.remove(g)
        slots=set()
        for item in bundle:
            if item.item_id in self.desired_items:
                slots.add(item.timeslot)
        return min(len(slots), self.cap)

    def marginal_contribution(self,bundle,item):
        '''
        Compute the marginal utility the agent gets form adding a particular item to a particular bundle of items

        @param bundle: list of items (from class Item)
        @param item: marginal item (from class Item)
        @return: marginal utility obtained by adding item to bundle (either 0 or 1).
        '''
        
        T=bundle.copy()
        current_val=self.valuation(T)
        T.append(item)
        new_val=self.valuation(T)
        return new_val-current_val
    


    def exchange_contribution(self,bundle,og_item, new_item):
        '''
        Determine whether the agent can exchange original_item for new_item and keep the same utility

        @param bundle: list of items (from class Item)
        @param og_item: original item in the bundle (from class Item)
        @param new_item: item we might exchange the og item for (from class Item)
        @return: True if utility obtained by exchanging item is the same or more, False otherwise.
        '''
        og_val=self.valuation(bundle)

        for i in range(len(bundle)):
            if bundle[i].item_id == new_item.item_id:
                return False

        T0=bundle.copy()
        index=[]
        for i in range(len(T0)):
            if T0[i].item_id == og_item.item_id:
                index.append(i)
        if len(index)==0:
            return False
        
        T0.pop(index[0])
        T0.append(new_item)

        new_val=self.valuation(T0)
        if og_item.item_id==new_item.item_id:
            return False
        if og_val==new_val:
            return True
        else:
            return False
    
def gen_random_agents(num_agents,items,p=10):
    agents=[]
    for i in range(num_agents):
        agent_id='Student'+str(i)
        agent_cap=random.randrange(4,11,1)
        agent_desired_items=[]
        for item in items:
            random_num=random.randrange(1, p+1, 1)
            if random_num==1:
                agent_desired_items.append(item.item_id)
        agent=Agent(agent_id,agent_desired_items, agent_cap)
        agents.append(agent)
    return agents

