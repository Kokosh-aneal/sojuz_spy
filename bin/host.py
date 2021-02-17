#! /usr/bin/python3

class Host():
#Host class constructor
    def __init__(self,ID,name,log):
        self.name = name
        self.ID = ID
        self.log = log
        self.item_list = []
