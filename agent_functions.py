from item_functions import Item

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


    def valuation(self,bundle):   
        '''
        Compute the utility the agent gets from a particular bundle of items 

        @param bundle: list of items (from class Item)
        @return: utility given to the agent by that bundle (int)
        '''
        T=bundle.copy()
        x=[*range(len(bundle))]
        x.reverse()
        for i in x:
            g=bundle[i]
            if g.item_id not in self.desired_items:
                T.pop(i)
        slots=[]
        for i in range(0,len(T)):
            slots.append(T[i].timeslot)
        slots=set(slots)
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

        THIS FUNCTION CAN PROBABLY BE BUILT MORE EFFICIENTLY
        '''
        T=bundle.copy()
        for i in range(len(T)):
            index=0
            if T[i].item_id == og_item.item_id:
                index=i
        T.pop(index)

        val=self.valuation(T)
        og_mg=self.marginal_contribution(T,og_item)
        new_mg=self.marginal_contribution(T, new_item)
        og_val=val+og_mg
        new_val=val+new_mg
        if og_val==new_val:
            return True
        else:
            return False

