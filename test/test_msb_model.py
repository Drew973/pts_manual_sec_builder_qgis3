# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:38:25 2026

@author: Drew.Bennett
"""


from manual_sec_builder.msb_model.msb_model import msbModel
from qgis.core import QgsProject



def testLoadScannerRte():
    rteFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\greece\20260523_06.rte'
    m = msbModel()
    m.loadScannerRte(rteFile)
    
    
    rc = m.rowCount()
    
    print(rc)
    assert rc == 33
    return m
    
    
    
    
    
def testSaveScannerRte(m:msbModel):
    f = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\greece\20260523_06_output.rte'
    
    layer = QgsProject.instance().mapLayersByName('TRR1_incDescriptions')[0]
    m.saveScannerRte(file = f,
                     layer = layer ,
                     labelField = 'label',
                     lengthField = '2021Length',
                     startNodeField = 'start_node',
                     endNodeField = 'end_node')
    #    def saveScannerRte(self , file:str , layer:QgsVectorLayer , lengthField:str , startNodeField:str , endNodeField:str ):
#
    
    
def testLoadRte():
    m = msbModel()
    p = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\Run005.rte'
    with open(p,'r') as f:
        m.loadRte(f)
    
    
    

def testLoadSec():
    m = msbModel()
    s = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\D0720.sec'
    with open(s,'r') as f:
        m.loadSec(f,rev=False)
    
    
    
def testSaveRte():
    
    m = msbModel()
    m.addRow(r'0800A30/127',False)
    m.addRow(r'0800A30/138',False)
    
    layer = QgsProject.instance().mapLayersByName('network_with_nodes')[0]
    #fields = {'label': 'sect_label', 'direction': 'direc_code', 'length': 'sec_length', 'startNode': 'start_node', 'endNode': 'end_node', 'startDate': 'start_date', 'endDate': 'sect_label', 'function': 'funct_name'}
    fields = {'label': 'sect_label', 'section_direction': 'direc_code', 'length': 'sec_length',
    'start_node': 'start_node', 'end_node': 'end_node', 'start_date': 'start_date', 'end_date': '',
    'function': 'funct_name'}    
    
    to = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\test.rte'

    with open(to,'w') as f:
        m.saveRte(f,layer,fields)
    
    
    
if __name__=='__console__':
  
    #imp.reload(manual_sec_builder)
    
    m = testLoadScannerRte()
    testSaveScannerRte(m)
    
    