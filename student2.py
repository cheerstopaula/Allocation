import numpy as np


class Student2:

    def __init__(self, items, G_conflicts, G_constraints, max_courses=6, cat_max=4, max_per_cat=4):
        self.items = items
        self.global_conflicts = G_conflicts
        self.global_constraints = G_constraints
        self.alloc_mat = np.zeros((len(items), 1))
        self.pref_mat, self.constraints = self.init_prefs_and_constraints(max_courses, cat_max, max_per_cat)

    def init_prefs_and_constraints(self, max_courses, cat_max, max_per_cat):
        pref_mat = np.zeros((1, len(self.items)))
        constraints = np.zeros((1, 1))
        cats = []
        # courses = []
        pref_cats = []
        # pref_courses = []
        num_cats = np.random.randint(1, cat_max+1)
        for item in self.items:                         # find all categories
            if item.category not in cats:
                cats.append(item.category)
            # if item.course not in courses:
            #     courses.append(item.course)

        """Number of preferred categories"""
        idxs = np.arange(len(cats))
        np.random.shuffle(idxs)
        for i in range(num_cats):                       # pick preferred categories randomly
            idx = idxs[i]
            pref_cats.append(cats[idx])
        print(pref_cats)
        for i in range(len(self.items)):
            if self.items[i].category not in pref_cats:     # set entry to 1 if not preferred category
                pref_mat[0][i] = 1
            # else:
            #     if self.items[i].course not in pref_courses:
            #         pref_courses.append(self.items[i].course)

        """Number of courses in each category"""
        for cat in pref_cats:                           # new row in preference matrix for each category
            cat_row = np.zeros(len(self.items))         # new entry in constraints for each category
            for i in range(len(self.items)):
                if cat == self.items[i].category:
                    cat_row[i] = 1
            pref_mat = np.vstack((pref_mat, cat_row))
            constraints = np.vstack((constraints, [max_per_cat]))

        # """Cannot be in same course, multiple different sections"""
        # seen_courses = []
        # for course in pref_courses:                          # new row in preference matrix for each category
        #     if course not in seen_courses:
        #         seen_courses.append(course)
        #         course_row = np.zeros(len(self.items))         # new entry in constraints for each category
        #         for i in range(len(self.items)):
        #             if (course == self.items[i].course):
        #                 course_row[i] = 1
        #         pref_mat = np.vstack((pref_mat, course_row))
        #         constraints = np.vstack((constraints, [1]))

        """Maximum courses constraint"""
        class_max_row = np.ones(len(self.items))
        pref_mat = np.vstack((pref_mat, class_max_row))
        constraints = np.vstack((constraints, [max_courses]))

        return pref_mat, constraints

    def update_alloc_mat(self, bundle):
        self.alloc_mat = np.zeros((len(self.items), 1))
        for item in bundle:
            idx = self.items.index(item)
            self.alloc_mat[idx] = [1]

    def valuation(self, bundle):
        self.update_alloc_mat(bundle)
        b1 = self.global_conflicts.dot(self.alloc_mat)
        for i in range(len(b1)):
            if b1[i][0] > self.global_constraints[i][0]:
                return len(bundle) - 1
        b2 = self.pref_mat.dot(self.alloc_mat)
        for i in range(len(b2)):
            if b2[i][0] > self.constraints[i][0]:
                return len(bundle) - 1
        return len(bundle)

    def exchange_contribution(self, bundle, og_item, new_item):
        '''
        Determine whether the agent can exchange original_item for new_item and keep the same utility

        @param bundle: list of items (from class Item)
        @param og_item: original item in the bundle (from class Item)
        @param new_item: item we might exchange the og item for (from class Item)
        @return: True if utility obtained by exchanging item is the same or more, False otherwise.
        '''
        og_val = self.valuation(bundle)

        for i in range(len(bundle)):
            if bundle[i].item_id == new_item.item_id:
                return False

        T0 = bundle.copy()
        index = []
        for i in range(len(T0)):
            if T0[i].item_id == og_item.item_id:
                index.append(i)
        if len(index) == 0:
            return False

        T0.pop(index[0])
        T0.append(new_item)

        new_val = self.valuation(T0)
        if og_item.item_id == new_item.item_id:
            return False
        if og_val == new_val:
            return True
        else:
            return False

    def marginal_contribution(self, bundle, item):
        '''
        Compute the marginal utility the agent gets form adding a particular item to a particular bundle of items

        @param bundle: list of items (from class Item)
        @param item: marginal item (from class Item)
        @return: marginal utility obtained by adding item to bundle (either 0 or 1).
        '''

        T = bundle.copy()
        current_val = self.valuation(T)
        T.append(item)
        new_val = self.valuation(T)
        return new_val-current_val
