import os
from os import path

from PyQt5 import QtGui

from PyQt5.Qt import QItemSelectionModel
                      
from  qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal,QSettings,Qt,QUrl
from qgis.utils import iface
from qgis.core import QgsFieldProxyModel
from qgis.PyQt.QtWidgets import QDockWidget,QFileDialog,QMessageBox,QMenuBar,QMenu
from qgis.PyQt.QtGui import QKeySequence

from . import layer_functions
from . makeRteDialog import makeRteDialog
from . loadRteDialog import loadRteDialog

from .msbModel import msbModel


def fixHeaders(path):
    with open(path) as f:
        t = f.read()

    r = {'qgsfieldcombobox.h':'qgis.gui','qgsmaplayercombobox.h':'qgis.gui'}
    for i in r:
        t = t.replace(i,r[i])

    with open(path, "w") as f:
        f.write(t)


uiPath = os.path.join(os.path.dirname(__file__), 'manual_sec_builder_dockwidget_base.ui')
fixHeaders(uiPath)
FORM_CLASS, _ = uic.loadUiType(uiPath)


class manual_sec_builderDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent = None):
        super(manual_sec_builderDockWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.model = msbModel(self)
        
        self.rteDialog = makeRteDialog(parent = self,model = self.model)#persistant.

        self.loadRteDialog = loadRteDialog(model = self.model,parent = self)
        self.loadRteDialog.accepted.connect(self.loadRte)
        
        self.sectionBox.setFilters(QgsFieldProxyModel.String)
        self.sectionBox.activated.connect(self.labelFieldSet)
        
        self.layerBox.activated.connect(self.layerSet)
        self.layerBox.layerChanged.connect(self.layerChange)
        
        layer = QSettings('pts', 'msb').value('layer','',str)
        self.layerBox.setCurrentIndex(self.layerBox.findText(layer))#try to set to last value 
        self.layerChange(self.layerBox.currentLayer())
        
        self.initTopMenu()
        self.initTableMenu()
        
       # self.rteDialog.buttonBox.accepted.connect(self.saveAsRte)
        #self.rteDialog.buttonBox.accepted.connect(self.rteDialog.hide)

        self.tableView.setModel(self.model)
        initDragAndDrop(self.tableView)

        self.model.countChanged.connect(self.rowCountChanged)


    def layerChange(self,layer):
        self.sectionBox.setLayer(layer)
        sf = QSettings('pts', 'msb').value('sectionField','',str)
        self.sectionBox.setCurrentIndex(self.sectionBox.findText(sf))
       # sd = QSettings('pts', 'msb').value('directionField','',str)
        self.rteDialog.setLayer(layer)
        self.loadRteDialog.setLayer(layer)


    #saves settings for layer when user activates box.
    def layerSet(self):
        layer = self.layerBox.currentLayer().name()
        QSettings('pts', 'msb').setValue('layer',layer)
    
    
    #saves setting for label field when user activates box.
    #i:int
    def labelFieldSet(self,i):
        sf = self.sectionBox.currentField()
        if sf:
            QSettings('pts', 'msb').setValue('sectionField',sf)


    def labelFieldChange(self,field):
        self.loadRteDialog.setLabelField(field)
        
        
    #row = row number
    def addRow(self,label,isReversed = None,rowNumber = None):
        self.model.addRow(label,isReversed,rowNumber)


    def rowCountChanged(self,change):
        newCount = self.model.rowCount() 
        v = self.rowBox.value()+change
        self.rowBox.setMaximum(newCount+1)
        self.rowBox.setValue(v)


    #for requested view
    def initTableMenu(self):
        self.tableMenu = QMenu()
        from_layer_act = self.tableMenu.addAction('set selected from layer')
        from_layer_act.triggered.connect(self.selectedFromFeatures)

        zoomAct = self.tableMenu.addAction('select on layer')
        zoomAct.triggered.connect(self.selectOnLayer)

        delAct = self.tableMenu.addAction('delete selected rows')
        delAct.triggered.connect(lambda:dropSelectedRows(self.tableView))

        delAllAct = self.tableMenu.addAction('delete all rows')
        delAllAct.triggered.connect(self.removeAll)        
        
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu);
        self.tableView.customContextMenuRequested.connect(lambda pt:self.tableMenu.exec_(self.tableView.mapToGlobal(pt)))


    def addDummy(self):
        self.model.addDummy(row = self.rowBox.value())


    #add selected feature of layer
    def addFeature(self):

        layer = self.getLayer()
        field = self.getLabelField()
        
        if layer and field:
            
            sf = layer.selectedFeatures()
            
            if len(sf)>1:
                iface.messageBar().pushMessage("manual sec builder: >1 feature selected",duration = 4)
                return

            if len(sf)<1:
                iface.messageBar().pushMessage("manual secbuilder: no features selected.",duration = 4)
                return

            sec = sf[0][field]
            self.addRow(label = sec,isReversed = self.rev(),rowNumber = self.rowBox.value()-1)



    def loadSec(self,clear = False):
        p = QFileDialog.getOpenFileName(caption = 'load .rte',filter = '*.sec;;*',directory = self.lastFolder())[0]
        
        if p:
            self.setFolder(p)
            
            row = self.rowBox.value()
            
            with open(p,'r') as f:
                self.model.loadSec(f = f,rev = self.rev(),row = row,clear = clear)
                
            iface.messageBar().pushMessage("manual secbuilder:loaded "+p,duration = 4)


    def loadRte(self):
        self.loadRteDialog.prepare(self.getLabelField(),row = None)
        self.loadRteDialog.show()
        
        
    def insertRte(self):
        self.loadRteDialog.prepare(self.getLabelField(),self.rowBox.value())
        self.loadRteDialog.show()       



#reversed selected?
    def rev(self):
        return self.model.revToBool(self.reversedBox.currentText())
                
                
    def lastFolder(self):
        folder = QSettings('pts', 'msb').value('folder','',str)
        if folder:
            return folder
        else:
            return path.expanduser('~\\Documents')


    def setFolder(self,p):
        f = path.dirname(p)
        QSettings('pts', 'msb').setValue('folder',f)


        
    def loadSr(self,row = None,clear = False):
        p = QFileDialog.getOpenFileName(caption = 'load .rte',filter = '*.sr;;*',directory = self.lastFolder())[0]
        if p:
            self.setFolder(p)

            if clear:
                self.model.clear()
                
            with open(p,'r') as f:
                self.model.loadSr(f,row)
                
            iface.messageBar().pushMessage("manual secbuilder:loaded "+p,duration = 4)
        


    def removeAll(self):
        response = QMessageBox.question(self,'remove all','remove all sections from table?',QMessageBox.Yes | QMessageBox.No)
        if response ==  QMessageBox.Yes:
            self.model.clear()


    def saveAsSec(self):
        p = QFileDialog.getSaveFileName(self, 'Save File',filter = '*.sec;;*',directory = self.lastFolder())[0]
        if p:

            if self.model.rowCount() == 0:
                iface.messageBar().pushMessage("manual secbuilder:no sections to save:",duration = 4)
                return
            
            self.setFolder(p)

            with open(p,'w') as f:
                self.model.saveSec(f = f)

            iface.messageBar().pushMessage("manual secbuilder:saved sec:"+p,duration = 4)


    #list of features   
    def features(self):
        layer = self.getLayer()
        labelField = self.getLabelField()
        if layer and labelField:
            return[layer_functions.getFeature(layer,labelField,val) for val in self.model.sectionLabels()]



   # def saveAsRte(self):
        
     #   to = self.rteDialog.fileWidget.filePath()
    #    layer = self.getLayer()

     #   if not to:
     #       iface.messageBar().pushMessage("manual secbuilder:no file selected",duration = 4)
     #       return
            
  #      fields = self.rteDialog.fields()
    #    fields.update({'label':self.getLabelField()})

  #      self.model.saveRte(to = to,layer = layer,fields = fields)
  #      iface.messageBar().pushMessage("manual secbuilder:saved to rte:"+to,duration = 4)
        


    def saveAsSr(self):
        p = QFileDialog.getSaveFileName(self, 'Save File',filter = '*.sr;;*',directory = self.lastFolder())[0]
        if p:
            if self.model.rowCount() == 0:
                iface.messageBar().pushMessage("manual secbuilder:no sections to save:",duration = 4)
                return
            
            self.setFolder(p)

            with open(p,'w') as f:
                self.model.saveSr(f,header = True)
                                      
            iface.messageBar().pushMessage("manual secbuilder:saved .sr:"+p,duration = 4)
                

        
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()


    def getLayer(self):
        layer = self.layerBox.currentLayer()
        if layer:
            return layer
        else:
            iface.messageBar().pushMessage("manual secbuilder: no layer selected",duration = 4)


    def getLabelField(self):
        field = self.sectionBox.currentField()
        if field:
            return field
        else:
            iface.messageBar().pushMessage("manual secbuilder: section field not set.",duration = 4)

    
    def selectOnLayer(self):
        layer = self.getLayer()
        field = self.getLabelField()       
        sections = [self.model.item(row,0).data(Qt.EditRole) for row in selectedRows(self.tableView)]#selected sections

        if layer and field:
            layer_functions.selectValues(layer,field,sections)


    def initTopMenu(self):
        topMenu = QMenuBar()       


        ######################load
        loadMenu = topMenu.addMenu("Load")
        loadSecAct = loadMenu.addAction('Load .sec...')
        loadSecAct.triggered.connect(lambda:self.loadSec(clear = True))

        loadRteAct = loadMenu.addAction('Load .rte...')
        #loadRteAct.triggered.connect(lambda:self.loadRteDialog.show(clearMode = True))
        #loadRteAct.triggered.connect(lambda:self.loadRte(clear = True))
        loadRteAct.triggered.connect(self.loadRte)
        
        
        loadSrAct = loadMenu.addAction('Load .sr...')
        loadSrAct.triggered.connect(lambda:self.loadSr(clear = True))


        ##################insert
        insertMenu = topMenu.addMenu("Insert")
        insertMenu.setToolTipsVisible(True)


        insertSecAct = insertMenu.addAction('Insert .sec...')
        insertSecAct.triggered.connect(lambda:self.loadSec(clear = False))
        insertSecAct.setToolTip('insert .sec file using selected row and direction')

    
        insertRteAct = insertMenu.addAction('Insert .rte...')
        #insertRteAct.triggered.connect(lambda:self.loadRteDialog.show(clearMode = False))
        #insertRteAct.triggered.connect(lambda:self.loadRte(clear = False))
        insertRteAct.triggered.connect(self.insertRte)

        insertRteAct.setToolTip('insert .rte file at row')


        insertSrAct = insertMenu.addAction('Insert .sr...')
        insertSrAct.triggered.connect(lambda:self.loadSr(row = self.rowBox.value(),clear = False))
        insertSrAct.setToolTip('insert .sr file at row')
        

        self.addFeatureAct = insertMenu.addAction('Add Selected Feature')
        self.addFeatureAct.setShortcut(QKeySequence('Alt+1'))#focus policy of dockwidget probably important here
        self.addFeatureAct.triggered.connect(self.addFeature)
        self.addFeatureAct.setToolTip('Insert selected feature of layer using selected row and direction')

        self.addDummyAct = insertMenu.addAction('Add Dummy')
        self.addDummyAct.setShortcut(QKeySequence('Alt+2'))#focus policy of dockwidget probably important here
        self.addDummyAct.triggered.connect(self.addDummy)
        self.addDummyAct.setToolTip('Insert dummy at row')

        ############################################save
        saveMenu = topMenu.addMenu("Save")
        
        saveSrAct = saveMenu.addAction('Save as .sr...')
        saveSrAct.triggered.connect(self.saveAsSr)

        saveSecAct = saveMenu.addAction('Save as .sec...')
        saveSecAct.triggered.connect(self.saveAsSec)

        saveRteAct = saveMenu.addAction('Save as .rte...')
        saveRteAct.triggered.connect(self.rteDialog.show)
        
        
        #######################help

        helpMenu = topMenu.addMenu('Help')  
        openHelpAct = helpMenu.addAction('Open help (in your default web browser)')
        openHelpAct.triggered.connect(self.openHelp)

        
        self.main_widget.layout().setMenuBar(topMenu)



#opens help/index.html in default browser
    def openHelp(self):
        helpPath = os.path.join(os.path.dirname(__file__),'help','overview.html')
        helpPath = 'file:///'+os.path.abspath(helpPath)
        QtGui.QDesktopServices.openUrl(QUrl(helpPath))

        

#select rows matching selected features of layer
    def selectedFromFeatures(self):
        layer = self.getLayer()
        field = self.getLabelField()
        
        if layer and field:
            sections = [f[field] for f in layer.selectedFeatures()]
            selectRowsFromValues(tableView = self.tableView,column = 0,values = sections)
            


def dropSelectedRows(tableView):
    model = tableView.model()
    rows = [r.row() for r in tableView.selectionModel().selectedRows()]#selectedRows() returns list of indexes
    for r in sorted(rows,reverse = True):
        model.takeRow(r)


def selectedRows(tableView):
    return [r.row() for r in tableView.selectionModel().selectedRows()]


#select rows where column matches values
def selectRowsFromValues(tableView,column,values,clearSelection = True):
    model = tableView.model()
    
    items = []
    for v in values:
        items += model.findItems(v,column = column)
    
    indexes = [i.index() for i in items]

    for c in range(model.columnCount()):
        indexes +=  [i.siblingAtColumn(c) for i in indexes]#add indexes for second column
    
    
    tableView.selectionModel().clearSelection()
    for i in indexes:
        tableView.selectionModel().select(i,QItemSelectionModel.Select)



def initDragAndDrop(tableView):
    tableView.setSelectionBehavior(tableView.SelectRows)
    tableView.setDragDropMode(tableView.InternalMove)
    tableView.setDragDropOverwriteMode(False)


#unused
#select row where column = value
#def selectRowFromValue(tableView,column,value):
    #rows = [i.index().row() for i in tableView.model().findItems(value,column = column)]
