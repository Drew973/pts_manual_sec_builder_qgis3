# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 11:54:29 2026

@author: Drew.Bennett


mypy scanner_rte.py --follow-imports=silent

"""


from dataclasses import dataclass , fields



    
    
@dataclass
class R1_1:
    route_id:str
    number_of_lanes:int
    
    @staticmethod
    def from_line(line:str) -> 'R1_1':
        line = line.strip('\n').ljust(63, ' ') # remove \n and add training spaces to make 63 charactors long
        
        return R1_1(
            route_id = line[8:57].strip(),
            number_of_lanes = int(line[57:63]),
        )
        
    

    def to_line(self) -> str:
        #template ='SCNROUTE{route_id:>50}{number_of_lanes:5g}'
        #route_str = '{route_id:>49}'.format(route_id = self.route_id)
        #print('route_str' , len(route_str))
        
        
        # “An”-means a string of n characters without leading spaces, or a string of n spaces.
        template ='SCNROUTE{route_id:>49}{number_of_lanes:5g}'#matches example but spec says A50
        return template.format(route_id = self.route_id ,
                               number_of_lanes = self.number_of_lanes
                               )





@dataclass
class R2_1:
    section_label:str
    section_length:float
    start_node:str
    xsp:str
    start_x:float
    start_y:float
    section_description:str
    
    
    #cast values to correct type
    def __post_init__(self):
        for field in fields(self):
            setattr(self, field.name, field.type(getattr(self, field.name)))
        
        
        
        
    @staticmethod
    def from_line(line:str) -> 'R2_1':
        line = line.strip('\n').ljust(186, ' ') # remove \n and add training spaces to make 186 charactors long
        
        return R2_1(
            section_label = line[0:30].strip(),
            section_length = float(line[30:41]),
            start_node = line[41:61].strip(),
            xsp = line[61:64],
            start_x = float(line[64:75]),
            start_y = float(line[75:86]),
            section_description = line [86:186].strip()
        )
        
    
    
    

    def to_line(self) -> str:
        template ='{section_label:<30}{section_length:11.3f}{start_node:<20}{xsp:<3}{start_x:11.3f}{start_y:11.3f}{section_description:<100}'
        return template.format(section_label = self.section_label ,
                               section_length = self.section_length,
                               start_node = self.start_node,
                               xsp = self.xsp,
                               start_x = self.start_x,
                               start_y = self.start_y,
                               section_description = self.section_description)

    @staticmethod
    def try_from_line(line:str) -> 'R2_1':
        try:
            return R2_1.from_line(line)
        except Exception:
            return None
        
        
        

#end of route reference
@dataclass
class R3_1:
    end_node: str
    end_x :float
    end_y: float
    
    @staticmethod
    def from_line(line:str) -> 'R3_1':
        line = line.strip('\n').ljust(42, ' ') # remove \n and add training spaces to make 63 charactors long
        
        return R3_1(
            end_node = line[0:20].strip(),
            end_x = float(line[21:31]),
            end_y = float(line[32:42])
        )
        
    

    def to_line(self) -> str:
        template ='{end_node:20}{end_x:11.3f}{end_y:11.3f}'
        return template.format(end_node = self.end_node ,
                               end_x = self.end_x,
                               end_y = self.end_y
                               )




def test_R1_1():
    input_line = 'SCNROUTE                                      20260523_06   33'
                 #SCNROUTE                                      20260523_06    33
    record = R1_1.from_line(input_line)
  #  print('route_id' , len(record.route_id))
    print(record)
    output_line = record.to_line()
    print(input_line)
    print(output_line)
    assert input_line.strip() == output_line.strip()



# test R2_1 to_line and from_line.
def test_R2_1():
    input_line = 'SRR1_01                           895.000SRR1_01             CL1 485272.000 168888.000                                                                                           '
    input_line = input_line.strip()
    r = R2_1.from_line(input_line)
   # print(r)
    output_line = r.to_line().strip()
    #line out should be same as line in. allowing spaces.
    #assert input_line[0:len(output_line)] == output_line
    assert input_line == output_line
    
    
    
# test R2_1 to_line and from_line.
def test_R3_1():
    input_line = 'Run-out              485263.000 168920.000'
    input_line = input_line.strip()
    r = R3_1.from_line(input_line)
    output_line = r.to_line().strip()
    print(input_line)
    print(output_line)
    #line out should be same as line in. allowing spaces.
    #assert input_line[0:len(output_line)] == output_line
    assert input_line == output_line    
    
    
    
    
if __name__ in ('__main__' , '__console__'):
    test_R2_1()
    #test_R1_1()
    #test_R3_1()
    
    
    
    