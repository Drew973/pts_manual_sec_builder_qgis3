

from PyQt5.QtCore import QDate
from .rte import R2_1,R3_1,R4_1,opposite_direction

#one of these for each section in rte

#direction in ['N','E','S','W','CW','AC']
#start_node,end_node,direction can be used to get if in reverse direction

#'label', 'direction', 'length', 'startNode', 'endNode', 'startDate', 'endDate', 'function'

class rteItem:
    def __init__(self,label,survey_direction,section_direction,length,start_node,end_node,start_date,end_date,function,lane_name='Lane 1',start_chainage=0,end_chainage=None,start_x=None,start_y=None,end_x=None,end_y=None):
        #cast to correct types here?
        self.section_label = label
        self.survey_direction = survey_direction
        self.section_direction = section_direction
        self.lane_name = lane_name
        
        self.start_chainage = start_chainage
        
        if end_chainage is None:
            self.end_chainage = length
        else:
            self.end_chainage = end_chainage

        self.section_len = length
        self.start_node = start_node
  
        self.end_node = end_node
            
        self.start_x = start_x
        
        self.start_y = start_y
        
        self.end_x = end_x
        
        self.end_y = end_y
        
        
        if isinstance(start_date,QDate):
            self.start_date = start_date.toString('dd-MMM-yyyy')
        else:
            self.start_date = start_date
        
        
        if isinstance(end_date,QDate):
            self.end_date = end_date.toString('dd-MMM-yyyy')
        else:
            self.end_date = end_date
            
        self.function = function
        

    def R2_1(self):
        return R2_1(self.section_label,self.survey_direction,self.lane_name,self.start_chainage,self.end_chainage,self.start_node,self.start_x,self.start_y)


    def R3_1(self):
        return R3_1(self.end_node,self.end_x,self.end_y)


    def R4_1(self):
        return R4_1(self.section_label,self.start_date,self.end_date,self.section_len,self.section_direction,self.function)


    def flip_direction(self):
        self.start_node,self.end_node = self.end_node,self.start_node #swap values
        self.start_x,self.end_x = self.end_x,self.start_x
        self.start_y,self.end_y = self.end_y,self.start_y

        self.survey_direction = opposite_direction(self.survey_direction)
        #self.start_chainage,self.end_chainage = self.end_chainage,self.start_chainage     #start and end chainage were not swapped in previous. Mistake?


    def is_dummy(self):
        return False


#make dummy using start_node,start_x,start_y of this item
#start node of dummy = end node of last. 
    def make_dummy(self):
        return dummy(start_node=self.end_node,start_x=self.end_x,start_y=self.end_y)


#behaves like rte_item. Not actually subclass because don't want some methods.
    
class dummy:

    def __init__(self,start_node,start_x=None,start_y=None):
        self.start_node = start_node
        self.start_x = start_x
        self.start_y = start_y

    def R2_1(self):
        return R2_1(None,None,None,0,0,self.start_node,self.start_x,self.start_y)

    def is_dummy(self):
        return True