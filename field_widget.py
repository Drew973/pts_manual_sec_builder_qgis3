from qgis.gui import QgsFieldComboBox,QgsMapLayerComboBox



class fieldWidget(QgsFieldComboBox):

    def __init__(self,parent=None,default=''):
        super().__init__(parent)
        
        self.default = default
        
        if isinstance(parent,QgsMapLayerComboBox):
            self.setLayer(parent.currentLayer())
            parent.layerChanged.connect(self.setLayer)

    def setLayer(self,layer):
        super().setLayer(layer)
        
        if not layer is None:
            if self.default in layer.fields().names():
                self.setField(self.default)
                
                
                
def makeFieldWidget(parent=None,filters=None,allowEmpty=False,default=''):
  
    w = fieldWidget(parent,default=default)
        
    if not filters is None:
        w.setFilters(filters)
            
    w.setAllowEmptyFieldName(allowEmpty)
    
    return w                