
from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsFieldProxyModel
from . field_widget import makeFieldWidget

from qgis.utils import iface


class makeRteDialog(QDialog):    


    def __init__(self,parent,model):

        super().__init__(parent)
        
        self.setWindowTitle('save as rte')

        self.setLayout(QFormLayout(self))
        
        self.fileWidget = QgsFileWidget(self)
        self.fileWidget.setStorageMode(QgsFileWidget.SaveFile)
        self.fileWidget.setFilter('*.rte;;*')
        self.layout().insertRow(0,'File',self.fileWidget)
        
        self.fw = {}#field widgets. dict of name:QgsFieldComboBox
        
   #     self.addField('label',makeFieldWidget(self,filters=QgsFieldProxyModel.String,default='sect_label'),'Section label')#have this in main widget
        self.addField('section_direction',makeFieldWidget(self,filters=QgsFieldProxyModel.String,default='direc_code'),'Direction')
        self.addField('length',makeFieldWidget(self,filters=QgsFieldProxyModel.Numeric,default='sec_length'),'Length')
        self.addField('start_node',makeFieldWidget(self,default='start_node',allowEmpty=True),'Start node')
        self.addField('end_node',makeFieldWidget(self,default='end_node',allowEmpty=True),'End node')
        self.addField('start_date',makeFieldWidget(self,QgsFieldProxyModel.Date|QgsFieldProxyModel.String|QgsFieldProxyModel.DateTime,True,'start_date'),'Start date')
        self.addField('end_date',makeFieldWidget(self,QgsFieldProxyModel.Date|QgsFieldProxyModel.String|QgsFieldProxyModel.DateTime,True,'end_date'),'End date')
        self.addField('function',makeFieldWidget(self,QgsFieldProxyModel.String,True,'funct_name'),'Function')

        #self.setTooltips({'direction':'Field with direction. Values need to be one of NB,EB,SB,WB,CW,AC'})

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel,parent=self)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.hide)

        self.layout().addRow(self.buttonBox)

        self.accepted.connect(self.save)


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
        
  
            
    def save(self):
        
        to = self.fileWidget.filePath()

        if not to:
            iface.messageBar().pushMessage("manual secbuilder:no file selected",duration = 4)
            return
            
        fields = self.fields()
        fields.update({'label':self.parent().getLabelField()})

        layer = self.parent().getLayer()
        
        if not layer is None:
            self.parent().model.saveRte(to = to,layer = layer,fields = fields)
            iface.messageBar().pushMessage("manual secbuilder:saved to rte:"+to,duration = 4)

