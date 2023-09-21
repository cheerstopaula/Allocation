from data_utils import Schedule

class Item:
    def __init__(self,item_id, capacity,timeslot):
        '''
        Object Item has three parameters:
        - @param item_id: course identification subject+catalog+'-"+section (Ex: CICS110-3)
        - @param copies: course capacity (seats)
        - @param timeslot: course schedule day+'-'+slot (Ex: Tue Thu -01:00 PM - 02:15 PM)
        '''
        self.item_id=item_id
        self.capacity=capacity
        self.timeslot=timeslot

def generate_items_from_schedule(filename):
    '''
    Generate list of items from object Schedule (its atributes are list with course information):
    @param filename: name of the excel file containing all course information
    @returns items: list of item objects.
    '''
    items=[]
    schedule = Schedule(filename)
    subject=schedule.subjects
    catalog=schedule.catalog
    capacity=schedule.capacity
    section=schedule.section
    days=schedule.days
    slot=schedule.slot
    for i in range(0, len(catalog)):
        item_id=subject[i]+catalog[i]+'-'+str(section[i])
        copies=int(capacity[i])
        timeslot=days[i]+'-'+slot[i]
        item=Item(item_id, copies, timeslot)
        items.append(item)
    return items

def get_bundle_from_allocation_matrix(X, items, agent_index):
    bundle=[]
    items_list=X[:,agent_index]
    for i in range(len(items_list)):
        if int(items_list[i])==1:
            bundle.append(items[i])
    return bundle



def get_bundle_indexes_from_allocation_matrix(X, items, agent_index):
    bundle_indexes=[]
    items_list=X[:,agent_index]
    for i in range(len(items_list)):
        if int(items_list[i])==1:
            bundle_indexes.append(i)
    return bundle_indexes

