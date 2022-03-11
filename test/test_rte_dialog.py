import sys
import imp

p = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder'

if __name__=='__console__':
    if not p in sys.path:
        sys.path.append(p)
        
    from qgis.core import QgsProject

    import makeRteDialog
    imp.reload(makeRteDialog)
    
    d = makeRteDialog.makeRteDialog()
    
    layer = QgsProject.instance().mapLayersByName('network')[0]
    d.setLayer(layer)
    d.show()
    