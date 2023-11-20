from data_utils import Schedule

class Item:
    def __init__(self, course, item_id, capacity, days, slot, timeslot, category, prof):
        '''
        Object Item has four parameters:
        - @param item_id: course identification subject+catalog+'-"+section (Ex: CICS110-3)
        - @param copies: course capacity (seats)
        - @param timeslot: course schedule day+'-'+slot (Ex: Tue Thu -01:00 PM - 02:15 PM)
        - @param category: course category (Ex: Data Science, Programming, Systems, etc.)

        '''
        self.course=course
        self.item_id=item_id
        self.capacity=capacity
        self.days=days
        self.time=slot
        self.timeslot=timeslot
        self.category=category
        self.prof=prof


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
    categories=schedule.categories
    prof=schedule.prof
    for i in range(0, len(catalog)):
        course=subject[i]+catalog[i]
        item_id=subject[i]+catalog[i]+'-'+str(section[i])
        copies=int(capacity[i])
        timeslot=days[i]+slot[i]
        item=Item(course, item_id, copies, days[i], slot[i], timeslot, categories[i], prof[i])
        items.append(item)
    return items

