# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:23:55 2026

@author: Drew.Bennett
"""

from PyQt5.QtWidgets import QDialog,QFormLayout,QDialogButtonBox
from qgis.gui import QgsFileWidget
from qgis.core import QgsFieldProxyModel
from qgis.utils import iface
from manual_sec_builder.widgets.field_box import fieldBox
from qgis.gui import QgsMapLayerComboBox
from qgis.core import QgsMapLayerProxyModel



class saveScannerRteDialog(QDialog):    


    def __init__(self , parent , model):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle('save as SCANNER rte')
        self.setLayout(QFormLayout(self))
        
        self.fileWidget = QgsFileWidget(self)
        self.fileWidget.setStorageMode(QgsFileWidget.SaveFile)
        self.fileWidget.setFilter('*.rte;;*')
        self.layout().insertRow(0,'File',self.fileWidget)
        
        self.layerBox = QgsMapLayerComboBox()
        self.layerBox.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.layerBox.setAllowEmptyLayer(True)
        self.layout().addRow('Layer to lookup details from',self.layerBox) 
        
        
        
        self.label = fieldBox(self.layerBox , 'sec_label')
        self.layout().addRow('Field with section label',self.label) 
        
        
        self.length = fieldBox(self.layerBox , 'sec_length',QgsFieldProxyModel.Numeric)
        self.layout().addRow('Field with section length',self.length)    
        
        self.start_node = fieldBox(self.layerBox , default = 'start_lrp_')
        self.layout().addRow('Field with start node',self.start_node)
        
        self.end_node = fieldBox(self.layerBox , default = 'end_lrp_co')
        self.layout().addRow('Field with end node',self.end_node)       
        
        self.description = fieldBox(self.layerBox , default = 'description')
        self.layout().addRow('Field with section description',self.description)              

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel , parent=self)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.hide)

        self.layout().addRow(self.buttonBox)

        self.accepted.connect(self.save)




            
    def save(self):
        to = self.fileWidget.filePath()
        if not to:
            iface.messageBar().pushMessage("manual secbuilder:no file selected",duration = 4)
            return
    
        self.model.saveScannerRte(file = to ,
                                      layer = self.layerBox.currentLayer(),
                                      labelField = self.label.currentText(),
                                      lengthField = self.length.currentText(),
                                      startNodeField = self.start_node.currentText(),
                                      endNodeField = self.end_node.currentText(),
                                      descriptionField = self.description.currentText())

  