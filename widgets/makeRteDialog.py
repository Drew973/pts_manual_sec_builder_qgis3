
from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsFieldProxyModel
from qgis.utils import iface
from .field_box import fieldBox


class makeRteDialog(QDialog):    


    def __init__(self,parent,model,layerBox):

        super().__init__(parent)
        
        
        self.model = model
        self.setWindowTitle('save as rte')

        self.setLayout(QFormLayout(self))
        
        self.fileWidget = QgsFileWidget(self)
        self.fileWidget.setStorageMode(QgsFileWidget.SaveFile)
        self.fileWidget.setFilter('*.rte;;*')
        self.layout().insertRow(0,'File',self.fileWidget)
        
        self.fw = {}#field widgets. dict of name:QgsFieldComboBox
        
        self.fw['section_direction'] = fieldBox(layerBox,'direc_code',QgsFieldProxyModel.String)
        self.fw['section_direction'].setAllowEmptyFieldName(False)
        self.layout().addRow('Direction',self.fw['section_direction'])
        
        self.fw['length'] = fieldBox(layerBox,'sec_length',QgsFieldProxyModel.Numeric)
        self.layout().addRow('Length',self.fw['length'])    
        
        self.fw['start_node'] = fieldBox(layerBox,default = 'start_lrp_')
        self.layout().addRow('Start node',self.fw['start_node'])
        
        self.fw['end_node'] = fieldBox(layerBox,default = 'end_lrp_co')
        self.layout().addRow('End node',self.fw['end_node'])       
        
        
        self.fw['start_date'] = fieldBox(layerBox,'start_date',
                                         QgsFieldProxyModel.Date|QgsFieldProxyModel.String|QgsFieldProxyModel.DateTime)
        self.layout().addRow('Start date',self.fw['start_date'])       
        
        
        self.fw['end_date'] = fieldBox(layerBox,'s_end_date',
                                         QgsFieldProxyModel.Date|QgsFieldProxyModel.String|QgsFieldProxyModel.DateTime)
        self.layout().addRow('End date',self.fw['end_date'])    
        
        
        self.fw['function'] = fieldBox(layerBox,'funct_name', QgsFieldProxyModel.String)
        self.layout().addRow('Function',self.fw['function'])    
        
        

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,parent=self)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.hide)

        self.layout().addRow(self.buttonBox)

        self.accepted.connect(self.save)


    #{name:field}
    def fields(self):
        return {k:self.fw[k].currentField() for k in self.fw}
        
  
            
    def save(self):
        to = self.fileWidget.filePath()
        if not to:
            iface.messageBar().pushMessage("manual secbuilder:no file selected",duration = 4)
            return
        fields = self.fields()
        fields.update({'label':self.parent().getLabelField()})
        layer = self.parent().getLayer()
        if not layer is None:
            with open(self.fileWidget.filePath(),'w') as f:
                r = self.model.saveRte(f,layer = layer,fields = fields)
                if r:
                    iface.messageBar().pushMessage(str(r),duration = 4)

