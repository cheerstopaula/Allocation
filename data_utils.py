import pandas as pd

class Schedule:
    def __init__(self,filename):
        attributes=self.build_atributes(filename)
        self.subjects=attributes[0]
        self.catalog=attributes[1]
        self.capacity=attributes[2]
        self.section=attributes[3]
        self.days=attributes[4]
        self.slot=attributes[5]
    def build_atributes(self, filename):
        classes = pd.read_excel(filename)
        subjects=classes['Subject'].to_list()
        catalog=classes['Catalog'].to_list()
        capacity=classes['CICScapacity'].to_list()
        section=classes['Section'].to_list()
        days=classes['zc.days'].to_list()
        slot=classes['Mtg Time'].to_list()
        return subjects, catalog, capacity, section, days, slot

    
