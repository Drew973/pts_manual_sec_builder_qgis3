#from . import fields_dialog

from qgis.utils import iface

from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox
from qgis.gui import QgsFileWidget
from . field_widget import fieldWidget



class loadRteDialog(QDialog):    

#parent must have attribute sections
    def __init__(self,model,parent=None):

        super().__init__(parent=parent)
        
        self.layer = None
        self.clear = None#true if want to clear existing sections from model
        self.row = 0# row to insert at. clear if row is None
        
        self.labelField = None
        self.model = model
        
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
         
        self.accepted.connect(self.load)
        
        
    #QgsMapLayer
    def setLayer(self,layer):
        self.directionFieldWidget.setLayer(layer)
        
  

    #set parameters for loading rte. Call before showing.
    def prepare(self,labelField,row):
     
        self.labelField = labelField
        self.row = row
    
        if self.row is None:
            self.setWindowTitle('load rte')
        else:
            self.setWindowTitle('insert rte')
        
        

#labelField,row,clear

    def load(self):
            
        p = self.fileWidget.filePath()
        if not p:
            iface.messageBar().pushMessage("manual secbuilder:no file selected",duration=4)
            return     


        with open(p,'r') as f:
            self.model.loadRTE(f=f,layer=self.directionFieldWidget.layer(),labelField=self.labelField,directionField=self.directionFieldWidget.currentField(),row=self.row)
            #iface.messageBar().pushMessage("manual secbuilder:loaded rte",duration=4)