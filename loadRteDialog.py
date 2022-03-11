#from . import fields_dialog

from qgis.gui import QgsFileWidget
from qgis.utils import iface

from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox
from qgis.gui import QgsFileWidget,QgsFieldComboBox,QgsMapLayerComboBox


class loadRteDialog(QDialog):    

#parent must have attribute sections
    def __init__(self,parent=None):

        self.clear = None#true if want to clear existing sections from model
        super().__init__(parent=parent)
        
        self.setLayout(QFormLayout(self))

        self.fileWidget = QgsFileWidget(self)
        self.fileWidget.setFilter('*.rte;;*')
        self.layout().insertRow(0,'File',self.fileWidget)
        
        self.directionFieldWidget = fieldWidget(self,'direc_code')
        self.directionFieldWidget.setToolTip('Field of layer with direction. Values need to be one of NB,EB,SB,WB,CW,AC')
        self.layout().addRow('Field of layer with direction.',self.directionFieldWidget)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,parent=self)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        
        self.layout().addRow(self.buttonBox)
        self.setClear(False)
        
        
    def setClear(self,clear):
    
        if clear:
            self.setWindowTitle('load rte')
        else:
            self.setWindowTitle('insert rte')
        
        self.clear = clear
        
        
    def setLayer(self,layer):
        self.directionFieldWidget.setLayer(layer)
        

    def load(self):

        layer=self.parent().getLayer()

        p=self.fileWidget.filePath()
        if not p:
            iface.messageBar().pushMessage("manual secbuilder:no file selected",duration=4)
            return     

        
        labelField=self.parent().getLabelField()
        

        with open(p,'r') as f:
            self.parent().model.loadRTE(f=f,layer=layer,labelField=labelField,directionField=directionField,row=self.parent().rowBox.value(),clear=self.clearMode)



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