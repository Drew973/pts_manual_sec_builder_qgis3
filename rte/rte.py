'''
functions for writing rte
'''
from PyQt5.QtCore import QDate

#“An” indicates a text field of n characters, left justified and padded with spaces;
def A(value,n):
    if value is None:
        return ' '*n #n spaces
    else:
        s = '{:<%d}'%(n)#eg '{:<20}'
        return s.format(str(value))
    
    
    
#“In” indicates an integer numeric field of up to n characters, including an optional leading
#sign (+ or -), right justified and padded with spaces;    
def I(value,n,sign=False):

    if value is None:
        return ' '*n  #n spaces

    if isinstance(value,int):
        if sign:
            s = '{:>+%d}'%(n)#eg '{:>+20}'
        else:
            s = '{:>%d}'%(n)#eg '{:>+20}'
        
        return s.format(value)

    raise TypeError('value %s is not integer or None'%(str(value)))



#“Fn.d” indicates a real number field of up to n characters, including the decimal point and an
#optional leading sign (+ or -), with d digits after the decimal point, right justified and padded
#with ''spaces;
def F(value,n,d,sign=False):
    if value is None:
        return ' '*n  #n spaces
    else:
    
        if sign:
            s = '{value:>+%d.%df}'%(n,d)
        else:
            s = '{value:>%d.%df}'%(n,d)
        
        return s.format(value=float(value))
     
     

def check_direction(direction):
    if direction is None:
        return True
        
    directions = ['NB','EB','SB','WB','CW','AC']
    if not direction in directions:
        raise ValueError('direction not in'+','.join(directions))



OPPOSITES = {'NB':'SB','EB':'WB','SB':'NB','WB':'EB','CW':'AC','AC':'CW','':''}#origonal code did CW':'CW','AC':'AC' but specification says CW opposite at AC


def opposite_direction(direction):
    return OPPOSITES[direction]



#1 of these
#route identifier=name. get from filename.
#new sec
#n_lanes=number of survey lanes. was number of items-1 in previous. why -1?      
def R1_1(route_identifier,n_lanes,file_format_version='V1'):
    return A('ROUTE',5)+A(file_format_version,8)+A(route_identifier,50)+I(n_lanes,5)+'\n'



#1 per survey lane. survey lane=section+direction?
#direction like NB
#lane_name='Lane 1'
#start_chainage=0
#end_chainage=section length
#start_reference_label=start node
#start_x,start y = x,y of start node(crs=27700) if known

def R2_1(section_label,direction,lane_name,start_chainage,end_chainage,start_reference_label,start_x=None,start_y=None):
    check_direction(direction)
    #return '{:<30}{:<2}{:<20}{:>11.3f}{:>11.3f}{:<20}{:>10}{:>10}\n'.format(section_label,direction,lane_name,start_chainage,end_chainage,str(start_reference_label),to_format(start_x,'{:>11.3f}'),to_format(start_y,'{:>11.3f}'))
    return A(section_label,30)+A(direction,2)+A(lane_name,20)+F(start_chainage,11,3)+F(end_chainage,11,3)+A(start_reference_label,20)+F(start_x,11,3)+F(start_y,11,3)+'\n'


#start_x and start_y are optional.
def dummy_R2_1(start_reference_label,start_x=None,start_y=None):
    return A(None,30)+A(None,2)+A(None,20)+F(None,11,3)+F(None,11,3)+A(start_reference_label,20)+F(start_x,11,3)+F(start_y,11,3)+'\n'



#end of route record. 1 of these.
#end_ref=end node,x,y (crs=27700) if known        
def R3_1(end_ref,end_x,end_y):
    return A(end_ref,20)+F(end_x,11,3)+F(end_y,11,3)+'\n'


# 1 per non dummy section in r2.1, sorted alphabetically by section label

def R4_1(section_label,start_date,end_date,section_len,direction,function):
    check_direction(direction)
   # return'{:<30}{:<11}{:<11}{:>11.3f}{:<2}{:<4}\n'.format(section_label,start_date,end_date,section_len,direction,function)
    return A(section_label,30)+A(start_date,11)+A(end_date,11)+F(section_len,11,3)+A(direction,2)+A(function,4)+'\n'


#returns space if value is None
def to_format(val,form):
    if val:
        return form.format(val)
    else:
        return ' '



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

        self.direction = opposite_direction(self.direction)
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


#to=something with .write method.

       
def write_rte(rte_items,to,route_identifier):

    n_lanes = len([i for i in rte_items if not i.is_dummy()])
    to.write(R1_1(route_identifier=route_identifier,n_lanes=n_lanes))

    last_non_dummy = None
    
    for i in rte_items:
        to.write(i.R2_1())

        if not i.is_dummy():
            last_non_dummy = i
    
        
    #R3_1 for last last non dummy
    if not last_non_dummy:
        raise ValueError('Error writing rte: All dummys.')


    to.write(last_non_dummy.R3_1())


    for i in sorted(rte_items, key=lambda x: x.section_label):
        if not i.is_dummy():
            to.write(i.R4_1())



#converts value val into format string form

#see rte spec

#to return strings.
# empty where value is None.
#raise error if value should be but can't be converted to int/float