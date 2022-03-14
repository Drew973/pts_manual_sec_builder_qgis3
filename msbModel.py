from PyQt5 import QtGui




from qgis.PyQt.QtCore import Qt,pyqtSignal

    #from . import layer_functions
    #from .rte import rte


from . import layer_functions
from . rte import rte,feature_to_rte_item

import os



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


    def loadSec(self,f,rev,row=0,clear=False):
        if clear:
            self.clear()

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
    def loadRTE(self,f,layer,labelField,directionField,row=None):
        
        if row is None:
            self.clear()
            self.setHorizontalHeaderLabels(self.headerLabels)
            row = 0

        lines = [line for line in f.readlines()]

        n = int(lines[0][63:69])#number of lanes is 1st line of file 63:69
        R2_1s = lines[1:n+1]#2.1 type records
                
        for line in R2_1s:
            sec = line[0:30].strip()#section label.

            if sec:
                #if directionField is None:
                direction = line[30:32].strip()
                forwardDirection = str(layer_functions.forward_dir(sec,layer,labelField,directionField))
                self.addRow(rowNumber=row,label=sec,isReversed = direction!=forwardDirection)
                
            else:
                self.addDummy(row)

            if row:
                row+=1



    def loadSr(self,f,row=None):
        for line in f.readlines():
            r=line.strip().split(',')
            if r[0]!='section':#not header
                self.addRow(rowNumber=row,label=r[0],isReversed=self.revToBool(r[1]))
                if row:
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

            

    def rteItem(self,row:int,layer,fields:dict):
        label = self.index(row,0).data()
        rev = self.index(row,1).data()        
        f = layer_functions.getFeature(layer=layer,field=fields['label'],value=label)
        return feature_to_rte_item.featureToRteItem(f,fields,layer.crs(),rev)
        

#labels and directions to list of rte_items and dummys.dummys use last item. dummys at start removed.
   #list of rte items.
    def rteItems(self,layer,fields):
        
        items = []
        lastValid = None
            
        for i in range(0,self.rowCount()):
            label = self.index(i,0).data()
            
            if label=='D':
                if lastValid:
                   items.append(lastValid.make_dummy())
            else:
                item = self.rteItem(i,layer,fields)
                items.append(item)
                lastValid = item
                    
        return items
            
            
    def saveRte(self,to,layer,fields):        
        with open(to,'w') as f:
            if self.rowCount()>0:
                rte.write_rte(self.rteItems(layer,fields),f,os.path.basename(to))
            
            
def isDummy(secLine):
    return secLine.strip()=='D'


def makeItem(data):
    item = QtGui.QStandardItem()
    item.setData(data,role=Qt.EditRole )
    item.setDropEnabled(False)
    #item.setText(str(data))
    return item


