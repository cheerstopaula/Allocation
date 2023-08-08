from data_utils import Schedule

class Item:
    def __init__(self,item_id, copies,timeslot):
        self.item_id=item_id
        self.copies=copies
        self.timeslot=timeslot

def generate_items_from_schedule(filename):
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

    