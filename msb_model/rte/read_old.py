# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 08:48:17 2022

@author: Drew.Bennett
"""


class RTEReadError(Exception):
    
    def __init__(self,line,tp,error):
        self.message = 'Error parsing line "{line}" as {tp}: {err}'.format(line=line,tp=tp,err=error)
        super().__init__(self.message)
    

def readR4_1(line):
    try:
        r = {}
        r['section_label'] = line[0:30].strip()
        r['start_date'] = line[30:41].strip()
        r['end_date'] = line[41:52].strip()
        r['section_length'] = line[52:63].strip()
        r['section_direction'] = line[63:65].strip()
        r['function'] = line[65:69].strip()
        return r
    
    except Exception as e:
        raise RTEReadError(line,'R4.1',e)


#line = '0600M62/416                   01-Jan-200901-Jan-3000   1323.000EBMain'
#print(readR4_1(line))


def readR2_1(line):
    try:
        r = {}
        r['section_label'] = line[0:30].strip()
        r['direction'] = line[30:32].strip()
        r['lane_name'] = line[32:52].strip()
        r['start_chainage'] = line[53:63].strip()
        r['end_chainage'] = line[64:74].strip()
        r['start_reference_label'] = line[74:94].strip()
        r['start_x'] = line[94:105].strip()
        r['start_y'] = line[105:116].strip()
        return r

    except Exception as e:
        raise RTEReadError(line,'R2.1',e)

#line = '0600M62/416                   EBLane 1                    0.000   1323.000900000               346067.001 389229.381'
#print(readR2_1(line))


# 1 indexed and inclusive
def getCharactors(line,start,end):
    
    if start <1:
        raise ValueError('trying to read before 1st charactor')
        
        
    if end>len(line):
        line += ' ' * end
        
    return line[start-1:end]
    
#line = '123456789'
#line = ''

#print(getCharactors(line,1,4))


#raise exception if start_x and start_y included and not floats. 
def readR3_1(line):
    try:
        r = {}
        r['end_ref'] = line[0:20].strip()
        if not r['end_ref']:
            raise ValueError('No end reference')
        
        start_x = getCharactors(line,21,31).strip()
        if start_x:
            r['start_x'] = float(start_x)
        else:
            r['start_x'] = None
   
        start_y = getCharactors(line,32,42).strip()
        if start_y:
            r['start_y'] = float(start_y)
        else:
            r['start_y'] = None            
   
        return r    

    except Exception as e:
        raise RTEReadError(line,'R3.1',e)

#line = '71661                350531.000 389891.246 '
#line = '0600M62/416                   EBLane 1                    0.000   1323.000900000               346067.001 389229.381'
#print(readR3_1(line))



def isR3_1(line):
    try:
        readR3_1(line)
        return True
    
    except:
        return False
    
    
def isR2_1(line):
    try:
        readR2_1(line)
        return True
    except:
        return False
    
    
    
def isR4_1(line):
    try:
        readR4_1(line)
        return True
    except:
        return False
    
    
#line = '71661                350531.000 389891.246 '
#line = '71661 '
#line = '                                                         '
#line = '0600M62/416                   EBLane 1                    0.000   1323.000900000               346067.001 389229.381'
#print(isR3_1(line))    
    
    
    