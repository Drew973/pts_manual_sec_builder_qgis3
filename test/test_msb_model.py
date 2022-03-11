import sys
import imp

p = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder'

if __name__=='__console__':
    if not p in sys.path:
        sys.path.append(p)
        
    from qgis.core import QgsProject

    import msbModel
    imp.reload(msbModel)
    
    from rte import rte
    imp.reload(rte)
    
    m = msbModel.msbModel()
    
    layer = QgsProject.instance().mapLayersByName('network_with_nodes')[0]
    #fields = {'label': 'sect_label', 'direction': 'direc_code', 'length': 'sec_length', 'startNode': 'start_node', 'endNode': 'end_node', 'startDate': 'start_date', 'endDate': 'sect_label', 'function': 'funct_name'}
    fields = {'label': 'sect_label', 'section_direction': 'direc_code', 'length': 'sec_length',
    'start_node': 'start_node', 'end_node': 'end_node', 'start_date': 'start_date', 'end_date': '',
    'function': 'funct_name'}

 #   m.addRow(r'0800A30/127',False)
 #   m.addRow(r'0800A30/138',False)
    
 #   print(m.rteItem(0,layer,fields))
#    print(m.rteItems(layer,fields))
    s = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\D0720.sec'
    
    with open(s,'r') as f:
        m.loadSec(f,rev=False)
    
    to = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\test.rte'
    m.saveRte(to,layer,fields)
    print('ok')