
class Agent:
    def __init__(self,id, desired_classes, cap):
        self.id=id
        self.desired_classes=desired_classes
        self.cap=cap

    def valuation(self,bundle):
        T=bundle.copy()
        x=[*range(len(bundle))]
        x.reverse()
        for i in x:
            g=bundle[i]
            if g.item_id not in self.desired_classes:
                T.pop(i)
        slots=[]
        for i in range(0,len(T)):
            slots.append(T[i].timeslot)
        slots=set(slots)
        return min(len(slots), self.cap)

    def marginalContribution(self,bundle,item):
        if item.item_id not in self.desired_classes:
            print('if 1')
            return 0
        T=bundle.copy()
        x=[*range(len(bundle))]
        x.reverse()
        for i in x:
            g=bundle[i]
            if g.item_id not in self.desired_classes:
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