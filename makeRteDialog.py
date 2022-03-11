from PyQt5.QtWidgets import QDialog
from  qgis.PyQt import uic
import os
from qgis.utils import iface

from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox
from qgis.gui import QgsFileWidget,QgsFieldComboBox,QgsMapLayerComboBox
from qgis.core import QgsFieldProxyModel



class makeRteDialog(QDialog):    


    def __init__(self,parent=None):

        fields = ['section_label','direction','section_len','start_node','end_node','start_date','end_date','function']

        super().__init__(parent)
        
        self.setWindowTitle('save as rte')

        self.setLayout(QFormLayout(self))
        
        self.fileWidget = QgsFileWidget(self)
        self.fileWidget.setStorageMode(QgsFileWidget.SaveFile)        
        self.layout().insertRow(0,'File',self.fileWidget)
        
        self.fw = {}#field widgets. dict of name:QgsFieldComboBox
        
        
   #     self.addField('label',makeFieldWidget(self,filters=QgsFieldProxyModel.String,default='sect_label'),'Section label')#have this in main widget
        self.addField('section_direction',makeFieldWidget(self,filters=QgsFieldProxyModel.String,default='direc_code'),'Direction')
        self.addField('length',makeFieldWidget(self,filters=QgsFieldProxyModel.Numeric,default='sec_length'),'Length')
        self.addField('start_node',makeFieldWidget(self,allowEmpty=True,default='start_node'),'Start node')
        self.addField('end_node',makeFieldWidget(self,allowEmpty=True,default='end_node'),'End node')
        self.addField('start_date',makeFieldWidget(self,filters=QgsFieldProxyModel.Date|QgsFieldProxyModel.String|QgsFieldProxyModel.DateTime,default='start_date'),'Start date')
        self.addField('end_date',makeFieldWidget(self,filters=QgsFieldProxyModel.Date|QgsFieldProxyModel.String|QgsFieldProxyModel.DateTime,default='end_date'),'End date')
        self.addField('function',makeFieldWidget(self,filters=QgsFieldProxyModel.String,default='funct_name'),'Function')

        #self.setTooltips({'direction':'Field with direction. Values need to be one of NB,EB,SB,WB,CW,AC'})


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,parent=self)
        self.buttonBox.rejected.connect(self.hide)
        self.layout().addRow(self.buttonBox)
        

    def addField(self,key,widget,displayName=None):
    
        if displayName is None:
            displayName = key
            
        self.fw[key] = widget     
        self.layout().addRow(displayName,self.fw[key])


    def setLayer(self,layer):
        for w in self.fw.values():
            w.setLayer(layer)
        
        
    def fields(self):
        return {k:self.fw[k].currentField() for k in self.fw}
        


class fieldWidget(QgsFieldComboBox):

    def __init__(self,parent=None,default=''):
        super().__init__(parent)
        
        self.default = default
        
        if isinstance(parent,QgsMapLayerComboBox):
            self.setLayer(parent.currentLayer())
            parent.layerChanged.connect(self.setLayer)

    def setLayer(self,layer):
        super().setLayer(layer)
        
        if self.default in layer.fields().names():
            self.setField(self.default)
            
            
            
def makeFieldWidget(parent=None,filters=None,allowEmpty=False,default=''):
  
    w = fieldWidget(parent,default=default)
        
    if not filters is None:
        w.setFilters(filters)
            
    w.setAllowEmptyFieldName(allowEmpty)
    
    return w

