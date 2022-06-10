# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 11:21:16 2022

@author: Drew.Bennett



functions to read line of rte. returns dict or RTEReadError.
' 'charactors are important here.

ignores trailing '/n' charactors


"""


class RTEReadError(Exception):
    
    def __init__(self,line,tp,error):
        self.message = 'Error parsing line "{line}" as {tp}: {err}'.format(line=line,tp=tp,err=error)
        super().__init__(self.message)
        
        
        

# 1 indexed and inclusive
def getCharactors(line,start,end):
    
    if start <1:
        raise ValueError('trying to read before 1st charactor')
        
        
    if end>len(line):
        line += ' ' * end
        
    return line[start-1:end]




def readR2_1(line):
    try:
        line = line.strip('\n')
        
        
        if len(line)<116:
            return RTEReadError(line,'R2_1','R3_1 has <116 charactors')
            
         
        if len(line)>116:
            return RTEReadError(line,'R2_1','R3_1 has >116 charactors')
        
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
        
        
        
        

def readR3_1(line):
    try:
        line = line.strip('\n')

        if len(line)<42:
            return RTEReadError(line,'R3_1','R3_1 has <42 charactors')
            
         
        if len(line)>42:
            return RTEReadError(line,'R3_1','R3_1 has >42 charactors')
        
            
        r = {}
        
        r['end_ref'] = line[0:20].strip()
        if not r['end_ref']:
            return RTEReadError(line,'R3_1','No end reference')

        
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
        return RTEReadError(line,'R3.1',e)
    
    
    
def readR4_1(line):
    try:
        line = line.strip('\n')

        if len(line)<69:
            return RTEReadError(line,'R4_1','R3_1 has <69 charactors')
         
        if len(line)>69:
            return RTEReadError(line,'R4_1','R3_1 has >69 charactors')
        
        r = {}
        r['section_label'] = line[0:30].strip()
        r['start_date'] = line[30:41].strip()
        r['end_date'] = line[41:52].strip()
        r['section_length'] = line[52:63].strip()
        r['section_direction'] = line[63:65].strip()
        r['function'] = line[65:69].strip()
        return r
    
    except Exception as e:
        return RTEReadError(line,'R4.1',e)    
    
    
    
    
#v = readR2_1('2200M25/928                   ACLane 1                    0.000   1785.0001239                 547275.632 156148.177')
v = readR4_1('2275M25/382                   01-Jan-300001-Jan-3000   2460.000ACMAIN')


    