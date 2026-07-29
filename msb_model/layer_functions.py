from qgis.core import QgsFeatureRequest,QgsVectorLayer , QgsFeature
from qgis.utils import iface
from typing import Iterator


#def selectSections(sections,layer,secField):
 #   a=','.join([singleQuote(s) for s in sections])
  #  #Field names in double quotes, string in single quotes
   # e="%s IN (%s)" %(doubleQuote(secField),a)#expression looks like "Column_Name" IN ('Value_1', 'Value_2', 'Value_N')
    
    #layer.selectByExpression(e)
   # iface.actionZoomToSelected().trigger()#zoom to selected

def single_quote(s:str) -> str:
    return "'%s'"%(s)


def double_quote(s:str) -> str:
    return '"%s"'%(s) 

def singleQuote(s:str):
    return "'%s'"%(s)


def doubleQuote(s:str):
    return '"%s"'%(s)



#sects is list of sections.
def selectSections(sects:list[str],layer:QgsVectorLayer ,field:str , zoom:bool = False):
    if field: 
        e="%s IN (%s)" %(double_quote(field),','.join([single_quote(s) for s in sects]))#expression looks like "Column_Name" IN ('Value_1', 'Value_2', 'Value_N')
        #Field names in double quotes, string in single quotes
        layer.selectByExpression(e)
        if zoom:
            zoomToSelected(layer)   
    else:
        iface.messageBar().pushMessage('fitting tool: Field not set.')       


#select features where feature[field]=value
def selectValues(layer:QgsVectorLayer , field:str , vals:list[str] , zoom: bool = False):
    e="%s IN (%s)" %(double_quote(field),','.join([single_quote(val) for val in vals]))#expression looks like "Column_Name" IN ('Value_1', 'Value_2', 'Value_N')
    #Field names in double quotes, string in single quotes
    layer.selectByExpression(e)
    if zoom:
        zoomToSelected(layer)   


        
#zoom to selected features of layer. Works with any crs
def zoomToSelected(layer:QgsVectorLayer):
    a = iface.activeLayer()
    iface.setActiveLayer(layer)
    iface.actionZoomToSelected().trigger()
    iface.setActiveLayer(a)
    #iface.mapCanvas().setExtent(layer.boundingBoxOfSelected())
    #iface.mapCanvas().refresh()



#get features where feature[field] in vals.
#no particular order
def getFeatures(layer:QgsVectorLayer , field:str , vals:list[str]) -> Iterator[QgsFeature]:
    e = "%s IN (%s)" %(doubleQuote(field),','.join([singleQuote(val) for val in vals]))#expression looks like "Column_Name" IN ('Value_1', 'Value_2', 'Value_N')
    #Field names in double quotes, string in single quotes
    return layer.getFeatures(e)
    


#return features of layer where field=val
#def getFeatures(layer,field,val):
  #  e='%s=%s '%(double_quote(field),single_quote(val))
 #   request = QgsFeatureRequest().setFilterExpression(e)
 #   return layer.getFeatures(request)



#return feature of layer where field=val
def getFeature(layer,field,value) -> QgsFeature:
    feats=[f for f in getFeatures(layer,field,value)]
    
    if len(feats) == 1:
        return feats[0]

    if not feats:
        raise KeyError('feature with %s = %s not found on layer %s'%(field,value,layer))

    if len(feats) > 1:
        raise KeyError('multiple features with %s = %s on layer %s'%(field,value,layer))


  


#find single feature in layer where field = section.
def findSection(section: str ,layer: QgsVectorLayer , field:str) -> QgsFeature:
    e = doubleQuote(field)+'='+singleQuote(section)
    r = QgsFeatureRequest().setFilterExpression( e)
    feats = []
        
    for f in layer.getFeatures(r):
        feats.append(f)

    if len(feats) == 1:
        return feats[0]

    if len(feats) == 0:
        raise KeyError('no feature with {f} = {v}'.format(f = field , v = section))
    
    if len(feats) > 1 :
        raise KeyError('more than 1 feature with {f} = {v}'.format(f = field , v = section))
        
    
    
def forward_dir(section: str , layer: QgsVectorLayer ,lab_field: str , dir_field: str) -> str:
    f = findSection(layer=layer,lab_field=lab_field,section=section)
    return f[dir_field]

