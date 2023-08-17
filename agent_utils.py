
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

    def marginalContribution(self,bundle,item):
        '''
        Compute the marginal utility the agent gets form adding a particular item to a particular bundle of items

        @param bundle: list of items (from class Item)
        @param item: marginal item (from class Item)
        @return: marginal utility obtained by adding item to bundle (either 0 or 1).
        '''
        if item.item_id not in self.desired_items:
            print('if 1')
            return 0
        T=bundle.copy()
        x=[*range(len(bundle))]
        x.reverse()
        for i in x:
            g=bundle[i]
            if g.item_id not in self.desired_items:
                T.pop(i)
        slots=[]
        for i in range(0,len(T)):
            slot=T[i].timeslot
            slots.append(slot)
            if slot==item.timeslot:
                print('if 2')
                return 0
        slots=set(slots)
        if len(slots)>=self.cap:
            print('if 3')
            return 0
        return 1