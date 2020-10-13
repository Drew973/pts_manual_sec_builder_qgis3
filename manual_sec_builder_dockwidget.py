import os
from os import path

from  qgis.PyQt import uic

from qgis.PyQt.QtCore import pyqtSignal,QSettings,Qt

from qgis.utils import iface
#from qgis.gui import QgsFieldProxyModel
from qgis.core import QgsFieldProxyModel

#from reading import RTESections,secSections
from .write_rte import database_to_rte

from qgis.PyQt.QtWidgets import QDockWidget,QFileDialog,QMessageBox,QShortcut,QMenuBar,QMenu,QToolBar
from qgis.PyQt.QtGui import QKeySequence

from .sections import sections
from .section import section
from .read_rte import rte_to_sections
from .read_sec import sec_to_sections

from .layer_functions import selectSections,forward_dir
from .secs_to_sr import secsToSR
from .sr_to_secs import SRToSecs

#from .database_dialog.database_dialog import database_dialog



def fixHeaders(path):
    with open(path) as f:
        t=f.read()

    r={'qgsfieldcombobox.h':'qgis.gui','qgsmaplayercombobox.h':'qgis.gui'}
    for i in r:
        t=t.replace(i,r[i])

    with open(path, "w") as f:
        f.write(t)


uiPath=os.path.join(os.path.dirname(__file__), 'manual_sec_builder_dockwidget_base.ui')
fixHeaders(uiPath)
FORM_CLASS, _ = uic.loadUiType(uiPath)


class manual_sec_builderDockWidget(QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super(manual_sec_builderDockWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.addButton.released.connect(self.add)
        
        self.addDummyButton.released.connect(self.addDummy)
        self.sectionBox.setFilters(QgsFieldProxyModel.String)
        self.sectionBox.activated.connect(self.secFieldSet)

        self.directionBox.setFilters(QgsFieldProxyModel.String)
        self.directionBox.activated.connect(self.dirFieldSet)
        
        self.s=QShortcut(QKeySequence('Ctrl+1'), self)
        self.s.activated.connect(self.add)

        self.sections=sections(table=self.secTable,spinbox=self.rowBox)

        self.layerBox.layerChanged.connect(self.layerChange)
        layer=QSettings('pts', 'msb').value('layer','',str)
        self.layerBox.setCurrentIndex(self.layerBox.findText(layer))#try to set to last value 
        self.layerBox.activated.connect(self.layerSet)
        self.layerChange(self.layerBox.currentLayer())
        self.dd=database_to_rte(self)
        self.dd.set(host='192.168.5.157',database='pts1944-01_he',user='stuart')
        
        self.initSecMenu()
        self.initTopMenu()

   
                        
    def layerChange(self,layer):
        self.sectionBox.setLayer(layer)
        sf=QSettings('pts', 'msb').value('sectionField','',str)
        self.sectionBox.setCurrentIndex(self.sectionBox.findText(sf))

        self.directionBox.setLayer(layer)
        sd=QSettings('pts', 'msb').value('directionField','',str)
        self.directionBox.setCurrentIndex(self.directionBox.findText(sd))



    def secFieldSet(self):
        sf=self.sectionBox.currentField()
        if sf!='':
            QSettings('pts', 'msb').setValue('sectionField',sf)


    def dirFieldSet(self):
        sf=self.directionBox.currentField()
        if sf!='':
            QSettings('pts', 'msb').setValue('directionField',sf)        

        
    def layerSet(self):
        layer=self.layerBox.currentLayer().name()
        QSettings('pts', 'msb').setValue('layer',layer)
    
    
    def add(self):
        if self.checkLayerSet() and self.checkSectionFieldSet():
        
            sl=self.layerBox.currentLayer()
            secField=self.sectionBox.currentField()
          
            sf=sl.selectedFeatures()
            
            if len(sf)>1:
                iface.messageBar().pushMessage("manual sec builder: >1 feature selected",duration=4)
                return

            if len(sf)<1:
                iface.messageBar().pushMessage("manual secbuilder: no features selected.",duration=4)
                return

            sec=sf[0][secField]
            s=section(label=sec,reverse=self.rev())
            
            self.sections.add_section(s)
        
#reversed selected?
    def rev(self):
        if self.reversedBox.currentText()=='Yes':
            return True
        
        if self.reversedBox.currentText()=='No':
            return False
        
        if self.reversedBox.currentText()=='Leave Blank':
            return None

        raise KeyError('unknown reverse option')

        
    def addDummy(self):
        self.sections.add_section(section(dummy=True,reverse=False))


    def loadRTE(self):
        if self.checkLayerSet() and self.checkSectionFieldSet() and self.checkDirectionFieldSet():
            p=QFileDialog.getOpenFileName(caption='load .rte',filter='*.rte;;*',directory=self.lastFolder())[0]

            if p!='':
                self.setFolder(p)
                secs=rte_to_sections(p)#list of section objects

                for sec in secs:
                    if not sec.dummy:
                        try:
                            fd=forward_dir(sec.label,self.layerBox.currentLayer(),self.sectionBox.currentField(),self.directionBox.currentField())
                           
                            if fd==sec.direction:
                                sec.reverse=False

                            if fd==sec.opposite_direction():
                                sec.reverse=True

                        except:
                            iface.messageBar().pushMessage("manual secbuilder: could not find section %s in layer. reversed? not set. "%(sec.label),duration=4)
                                                    
                    self.sections.add_section(sec)  
                
                
    def lastFolder(self):
        folder=QSettings('pts', 'msb').value('folder','',str)
        if folder!='':
            return folder
        else:
            return path.expanduser('~\\Documents')


    def setFolder(self,p):
        f=path.dirname(p)
        QSettings('pts', 'msb').setValue('folder',f)

        
    def loadSec(self):
        p=QFileDialog.getOpenFileName(caption='load .rte',filter='*.sec;;*',directory=self.lastFolder())[0]
        if p!='':
            self.setFolder(p)
            for s in sec_to_sections(p,self.rev()):
                self.sections.add_section(s)

        
    def loadSr(self):
        p=QFileDialog.getOpenFileName(caption='load .rte',filter='*.sr;;*',directory=self.lastFolder())[0]
        if p!='':
            self.setFolder(p)
            for s in SRToSecs(p):
                self.sections.add_section(s)


    def remove(self):
        self.sections.remove_selected()
        


    def removeAll(self):
        response = QMessageBox.question(self,'remove all','remove all sections from table?',QMessageBox.Yes | QMessageBox.No)
        if response== QMessageBox.Yes:
            self.sections.clear()


    
    def saveAsSec(self):
        p=QFileDialog.getSaveFileName(self, 'Save File',filter='*.sec;;*',directory=self.lastFolder())[0]
        if p!='':
            if len(self.sections.secs)>0:
                self.setFolder(p)
                self.sections.to_sec(p)
                iface.messageBar().pushMessage("manual secbuilder:saved sec:"+p,duration=4)
            else:
                iface.messageBar().pushMessage("manual secbuilder:no sections to save:",duration=4)



    def saveAsRte(self):
        self.dd.connect()
        
        p=QFileDialog.getSaveFileName(self, 'Save File',filter='*.rte;;*',directory=self.lastFolder())[0]
        if p!='':
            if len(self.sections.secs)>0:
                self.setFolder(p)
                f,route_id = os.path.split(p)
                
                m=self.dd.make(self.sections.secs,route_id = route_id)
                if m==True:
                    self.dd.save(p)
                    iface.messageBar().pushMessage("manual secbuilder:saved rte:"+p,duration=4)
                else:
                    iface.messageBar().pushMessage("manual secbuilder error:error in making .rte "+m,duration=4)
            else:
                    iface.messageBar().pushMessage("manual secbuilder:no sections to save.",duration=4)
 

    def saveAsSr(self):
        p=QFileDialog.getSaveFileName(self, 'Save File',filter='*.sr;;*',directory=self.lastFolder())[0]
        if p!='':
            if len(self.sections.secs)>0:
                self.setFolder(p)
                secsToSR(self.sections.secs,p)
                iface.messageBar().pushMessage("manual secbuilder:saved .sr:"+p,duration=4)
            else:
                iface.messageBar().pushMessage("manual secbuilder:no sections to save:",duration=4)

        
    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()


    #checks layer is set
    def checkLayerSet(self):
        layer = self.layerBox.currentLayer()
        if not layer is None:
            return True
        else:
            iface.messageBar().pushMessage("manual secbuilder error: no layer selected",duration=4)
            return False


    #checks section field is set
    def checkSectionFieldSet(self):
        if self.sectionBox.currentField()=='':
            iface.messageBar().pushMessage("manual secbuilder: section field not set.",duration=4)
            return False        
        else:
            return True


    #checks direction field is set
    def checkDirectionFieldSet(self):
        if self.directionBox.currentField()=='':
            iface.messageBar().pushMessage("manual secbuilder: direction field not set.",duration=4)
            return False
        else:
            return True
        
    
    def select(self):
        if self.checkLayerSet() and self.checkSectionFieldSet():
            selected=self.sections.list_selected()
            if len(selected)==0:
                selected=self.sections.list_sections()
            selectSections(selected,self.layerBox.currentLayer(),self.sectionBox.currentField(),True)
            
    
    def setSelected(self):
        if self.checkLayerSet() and self.checkSectionFieldSet():
            feats=self.layerBox.currentLayer().selectedFeatures()
            secs=[f[self.sectionBox.currentField()] for f in feats]
            self.sections.set_selected(secs)


    def initTopMenu(self):
#adding
        #topMenu=self.titleBarWidget()
        #topMenu=self.layout().menuBar() 
        topMenu=QMenuBar()
        #self.layout().setMenuBar(self.topMenu)
        #topMenu=QMenuBar(self)#works but need to click '>>' button
       
        addMenu=topMenu.addMenu("add")
        loadSecAct=addMenu.addAction('load .sec...')
        loadSecAct.triggered.connect(self.loadSec)
        loadRteAct=addMenu.addAction('load .rte...')
        loadRteAct.triggered.connect(self.loadRTE)
        loadSrAct=addMenu.addAction('load .sr...')
        loadSrAct.triggered.connect(self.loadSr)
    

#save
        saveMenu=topMenu.addMenu("save")
        
        saveSrAct=saveMenu.addAction('save as .sr...')
        saveSrAct.triggered.connect(self.saveAsSr)        

        saveSecAct=saveMenu.addAction('save as .sec...')
        saveSecAct.triggered.connect(self.saveAsSec)

        saveSecAct=saveMenu.addAction('save as .rte...')
        saveSecAct.triggered.connect(self.saveAsRte)

        setingsMenu=topMenu.addMenu("settings")
        setDatabaseAct=setingsMenu.addAction('set database...')
        setDatabaseAct.triggered.connect(self.dd.show)
        
        #self.toolBar=QToolBar(self) 
        #toolbar=self.addToolBar()
        #topMenu = QMenuBar(self)
        #topMenu.setDefaultUp(False)
        #addMenu=topMenu.addMenu("add")
        #saveMenu=topMenu.addMenu("save")
        #self.layout().addWidget(topMenu)
        self.main_widget.layout().setMenuBar(topMenu)
        

#for requested view
    def initSecMenu(self):
        self.sec_menu = QMenu()
        from_layer_act=self.sec_menu.addAction('set selected from layer')
        from_layer_act.triggered.connect(self.setSelected)

        zoomAct=self.sec_menu.addAction('zoom to selected')
        zoomAct.triggered.connect(self.select)

        delAct=self.sec_menu.addAction('delete selected rows')
        delAct.triggered.connect(self.sections.remove_selected)

        delAllAct=self.sec_menu.addAction('delete all rows')
        delAllAct.triggered.connect(self.removeAll)        
        
        self.secTable.setContextMenuPolicy(Qt.CustomContextMenu);
        self.secTable.customContextMenuRequested.connect(self.showSecMenu)


    def showSecMenu(self,pt):
        self.sec_menu.exec_(self.mapToGlobal(pt))








            
