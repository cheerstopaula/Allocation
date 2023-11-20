from item_functions import generate_items_from_schedule
from itertools import combinations
import numpy as np
from collections import defaultdict
from itertools import product


class Student:

    def __init__(self, items, max_courses=6, cat_max=4):

        self.items = items

        def def_value(): 
            return 0
        
        self.cat_vals = defaultdict(def_value)
        cats = []
        for item in items:
            if item.category not in cats:
                cats.append(item.category)
        num_cats = np.random.randint(1, cat_max+1)
        cat_idx = np.arange(num_cats)
        np.random.shuffle(cat_idx)
        self.cat_prefs = []
        for i in range(num_cats):
            self.cat_prefs.append(cats[cat_idx[i]])
            self.cat_vals[cats[cat_idx[i]]] = []
        self.course_value_map = self.init_cat_value_map(items, max_courses, cat_max, self.cat_prefs)



    def init_cat_value_map(self, items, max_courses, cat_max, cat_prefs):

        course_list = []
        cat_courses = {}
        for cat in cat_prefs:       # init lists for each category in dictionary
            cat_courses[cat] = []

        for i in range(len(items)):
            if items[i].course not in course_list:      # only adds non-duplicates (removes sections)
                course_list.append(items[i].course)
                if items[i].category in cat_prefs:      # only adds from interested preferences
                    cat_courses[items[i].category].append(items[i].course)

        cat_combs = {}
        for cat in cat_prefs:       # init lists for each category in combination dictionary
            cat_combs[cat] = []
            self.cat_vals[cat] = []
            for i in range(min(cat_max, len(cat_courses[cat]))+1):  # all combinations over possible groupings
                combs = list(combinations(cat_courses[cat], i))
                combs.sort()
                for i in range(len(combs)):
                    combs[i] = tuple(sorted(combs[i]))
                cat_combs[cat].append(combs)
                self.cat_vals[cat].append([])

        for key in cat_combs.keys():
            idx = 0
            for loc in cat_combs[key]:
                for tup in loc:
                    val = np.random.randint(0, max(1, len(tup)+1))
                    self.cat_vals[key][idx].append(val)
                idx += 1

        return cat_combs
    

    #def init_sect_time_val_map(self, items, )


    def resolve_conflicts(self, bundle, dup_courses=None, conflict_times=None):
        conflicts = []
        non_conflicts = []
        max_val = 0

        if dup_courses is not None:
            for i in range(len(dup_courses)):
                conflicts.append([])
                for item in bundle:
                    if item.course == dup_courses[i]:
                        conflicts[i].append(item)

        if conflict_times is not None:
            for i in range(len(conflict_times)):
                conflicts.append([])
                for item in bundle:
                    if item.days == conflict_times[i][0] and item.time == conflict_times[i][1]:
                        conflicts[i].append(item)
        
        conflict_combs = list(product(*tuple(tuple(i) for i in conflicts)))
    
        for item in bundle:
            if item not in conflicts:
                non_conflicts.append(item)
        for comb in conflict_combs:
            new_bundle = non_conflicts + list(comb)
            val = self.valuation(new_bundle, True)
            if val > max_val:
                max_val = val
        return max_val


    def valuation(self, bundle, conflict=False):
        value = 0
        cats_dict = {}
        cats = []
        courses = []
        times = {}
        seen_days = []
        dup_courses = []
        conflict_times = []
        for item in bundle:
            if item.category not in cats:
                cats.append(item.category)
                cats_dict[item.category] = []
            if item.course not in courses:
                courses.append(item.course)
                cats_dict[item.category].append(item.course)
            else:
                if item.course not in dup_courses:
                    dup_courses.append(item.course)
            days = [day for day in item.days.split(' ')]
            for day in days:
                if day not in seen_days:
                    seen_days.append(day)
                    times[day] = []
                if item.time not in times[day]:
                    #times.append(item.time)
                    times[day].append(item.time)
                else:
                    if item.time not in conflict_times:
                        conflict_times.append((item.days, item.time))
        if (len(dup_courses) > 0 or len(conflict_times) > 0) and not conflict:
            if len(dup_courses) > 0 and len(conflict_times) == 0:
                val = self.resolve_conflicts(bundle, dup_courses)
                return val
            elif len(dup_courses) == 0 and len(conflict_times) > 0:
                val = self.resolve_conflicts(bundle, conflict_times=conflict_times)
                return val
            else:
                val = self.resolve_conflicts(bundle, dup_courses, conflict_times)
                return val
        for key in cats_dict.keys():
            if key in self.course_value_map.keys():
                cats_dict[key].sort()
                length = len(cats_dict[key])
                idx = self.course_value_map[key][length].index(tuple(cats_dict[key]))
                value += self.cat_vals[key][length][idx]
        return value
    


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

"""
    NOTES:
            -Would suggest making combinations compatible with selection of 'req'/'core'/'elec'
"""
