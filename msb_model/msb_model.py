from PyQt5 import QtGui


from qgis.PyQt.QtCore import Qt,pyqtSignal

from . import layer_functions
from . rte import rte,feature_to_rte_item,read

import os

import logging
logger = logging.getLogger(__name__)



class msbModel(QtGui.QStandardItemModel):
    countChanged = pyqtSignal(int)#amount rowCount changed by. Methods that change rowCount should emit this AFTER changing count.


    def __init__(self,parent=None):
        
        super(msbModel, self).__init__(parent)
        self.headerLabels = ['section','reversed']
        self.setHorizontalHeaderLabels(self.headerLabels)



    def dropMimeData(self, data, action, row, col, parent):
        """
        Always move the entire row, and don't allow column "shifting"
        """
        return super().dropMimeData(data, action, row, 0, parent)



    def getRow(self,row:int):
        return [self.data(self.index(row,c)) for c in range(self.columnCount())]



    def takeRow(self,row:int):
        r = super().takeRow(row)
        self.countChanged.emit(-1)             
        return r


    def appendRow(self,items):
        super().appendRow(items)
        self.countChanged.emit(1)


    def insertRow(self,row,items):
        super().insertRow(row,items)
        self.countChanged.emit(1)

    
#returns number of rows added (1)  
    def addRow(self,label,isReversed=None,rowNumber=None):
        
        if not isinstance(rowNumber,int):
            self.appendRow([makeItem(label),makeItem(isReversed)])
        
        else:
            if rowNumber>self.rowCount():
                self.appendRow([makeItem(label),makeItem(isReversed)])
            else:
                self.insertRow(rowNumber,[makeItem(label),makeItem(isReversed)])#does nothing if rowNumber not in model



    def clear(self):
        rc = self.rowCount()
        super(msbModel, self).clear()
        self.setHorizontalHeaderLabels(self.headerLabels)
        self.countChanged.emit(-rc)


    def loadSec(self,f,rev,row=0):
        if row is None:
            self.clear()
            self.setHorizontalHeaderLabels(self.headerLabels)
            row = 0

        for line in f.readlines():

            if isDummy(line):
                self.addDummy(row)

            else:
                r = line.strip().split(',')
                label = r[0]
            
                if label!='section':#not header
                    self.addRow(rowNumber=row,label=label,isReversed=rev)
                     
            row += 1
                


#f is file like object with readlines() method
#returns number of rows added.
#inserts new rows at row. Clears if None.
    def loadRte(self,f,row=None):
        logger.debug('loadRte(%s)',f)

        if row is None:
            self.clear()
            #self.setHorizontalHeaderLabels(self.headerLabels)
            row = 0


        R2_1s = []
        sectionDirections = {}

#R2.1 has forward section direction.
#R4.1 has section direction


#R1.1,R2.1s,R3.1,R4.1s. no R3.1 for dummy.


        for line in f.readlines():
            
            r = read.readR2_1(line)
            if isinstance(r,dict):#valid R2_1 line
                R2_1s.append(r)
            
            
            r = read.readR4_1(line)
            if isinstance(r,dict):#valid R4_1 line
                sectionDirections[r['section_label']] = r['section_direction']
                
                
                
        logger.debug('sectionDirections:%s',sectionDirections)


        for r in R2_1s:#these are in order or route
            sec = r['section_label']
            
            if sec:
                sectionDirection = sectionDirections[sec]
                self.addRow(rowNumber=row,label=r['section_label'],isReversed = sectionDirection!=r['direction'])
        
            else:
                self.addDummy(row)
        
            row +=1
                
        #4.1s are sorted alphabetically
        #2.1s are in order of route


    def loadSr(self,f,row=None):
        
        if row is None:
            self.clear()
            self.setHorizontalHeaderLabels(self.headerLabels)
            row = 0        
        
        for line in f.readlines():
            r = line.strip().split(',')
            if r[0]!='section':#not header
                self.addRow(rowNumber=row,label=r[0],isReversed=self.revToBool(r[1]))
                row+=1        
        


    def addDummy(self,row):
        self.addRow(label='D',isReversed=None,rowNumber=row)



    def saveSec(self,f):
        f.write('\n'.join(self.sectionLabels()))#label\n



    def saveSr(self,f,header=True):
        if header:
            f.write('section,reversed')
                    
        for r in range(self.rowCount()):
            lab=str(self.item(r,0).data(Qt.EditRole))
            rev = self.boolToRev(self.item(r,1).data(Qt.EditRole))
            f.write('\n%s,%s'%(lab,rev))

  

    def sectionLabels(self):
        return [self.item(r,0).data(Qt.EditRole) for r in range(self.rowCount())]
        

    def directions(self):
        return [self.item(r,1).data(Qt.EditRole) for r in range(self.rowCount())]


    def revToBool(self,rev):
        if not rev:
            return None
        
        if rev.lower()=='no':
            return False
        
        if rev.lower()=='yes':
            return True



    def boolToRev(self,b):
       
        if b is None:
            return ''
        
        if b:
            return 'Yes'
        
        if b==False:
            return 'No'


#labels and directions to list of rte_items and dummys.dummys use last item. dummys at start removed.
   #list of rte items.
   #layer.getFeatures() slow and has to set up new conection every time.
   #quicker to call once to get all features
   
   #-> [rteItem]
   
    def rteItems(self,layer,fields):
    #    logger.debug('rteItems(%s,%s)',layer,fields)
        labelField = fields['label']
        
        #label:feature
        features = {f[labelField]:f for f in layer_functions.getFeatures(layer,labelField,self.sectionLabels())}
                
        items = []
        lastValid = None
            
        for i in range(0,self.rowCount()):
            label = self.index(i,0).data()
            rev = self.index(i,1).data()
            
            if label=='D':
                if lastValid:
                   items.append(lastValid.make_dummy())
            else:
                if label in features:                   
                    item = feature_to_rte_item.featureToRteItem(features[label],fields,layer.crs(),rev)
                    items.append(item)
                    lastValid = item
                else:
                    raise KeyError('layer has no feature with {field} = {lab} '.format(field=labelField,lab=label))
                    
                 
        return items
            
            #->str
    def saveRte(self,f,layer,fields):
        
        result = ''
        
        if layer is None:
            return 'Need layer to load rte'
        
        if self.rowCount() == 0:
            return 'No sections in route'
        
        if self.rowCount()>0:
            items = self.rteItems(layer,fields)
            rte.write_rte(items,f,os.path.basename(f.name))
            result = 'manual secbuilder:saved to rte:{name}.'.format(name=f.name)
            if len(items) > 1:
                for i,item in enumerate(items[1:]):
                    last = items[i]
                    if item.start_node != last.end_node:
                        result += '\nWarning End node of {last} != start node of {sec}.'.format(last = last.section_label,sec = item.section_label)
        
        return result
                        
                    
            
    #file is open file like with writeLines() and .name attribute
    #layer and fields only required for rte
    def save(self,f,layer=None,fields=None):
        
        ext = os.path.splitext(f.name)[-1]
                
        if ext == '.sec':
            self.saveSec(f)

        if ext == '.sr':
            self.saveSr(f)
            
        if ext =='.rte':            
            self.saveRte(f,layer,fields)


    #file is open file like with writeLines() and .name attribute
    #layer and fields only required for rte
    #rev only required for sec
    def load(self,f,row=0,layer=None,fields=None,rev=None):
        
        ext = os.path.splitext(f.name)[-1]

        if ext == '.sec':
            self.loadSec(f,rev,row)

        if ext == '.sr':
            self.loadSr(f,row)
            
        if ext =='.rte':                
            self.loadRte(f,row)

            
def isDummy(secLine):
    return secLine.strip()=='D'


def makeItem(data):
    item = QtGui.QStandardItem()
    item.setData(data,role=Qt.EditRole )
    item.setDropEnabled(False)
    #item.setText(str(data))
    return item


