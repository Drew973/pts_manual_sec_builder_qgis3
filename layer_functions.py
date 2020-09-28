from qgis.core import QgsFeatureRequest
from qgis.utils import iface


#def selectSections(sections,layer,secField):
 #   a=','.join([singleQuote(s) for s in sections])
  #  #Field names in double quotes, string in single quotes
   # e="%s IN (%s)" %(doubleQuote(secField),a)#expression looks like "Column_Name" IN ('Value_1', 'Value_2', 'Value_N')
    
    #layer.selectByExpression(e)
   # iface.actionZoomToSelected().trigger()#zoom to selected

def single_quote(s):
    return "'%s'"%(s)


def double_quote(s):
    return '"%s"'%(s) 



#sects is list of sections.
def selectSections(sects,layer,field,zoom=False):
    if field: 
        e="%s IN (%s)" %(double_quote(field),','.join([single_quote(s) for s in sects]))#expression looks like "Column_Name" IN ('Value_1', 'Value_2', 'Value_N')
        #Field names in double quotes, string in single quotes
        layer.selectByExpression(e)
        if zoom:
            zoomToSelected(layer)   
    else:
        iface.messageBar().pushMessage('fitting tool: Field not set.')       

        
#zoom to selected features of layer. Works with any crs
def zoomToSelected(layer):
    a=iface.activeLayer()
    iface.setActiveLayer(layer)
    iface.actionZoomToSelected().trigger()
    iface.setActiveLayer(a)
    #iface.mapCanvas().setExtent(layer.boundingBoxOfSelected())
    #iface.mapCanvas().refresh()








def singleQuote(s):
    return "'%s'"%(s)


def doubleQuote(s):
    return '"%s"'%(s)  



def findSection(section,layer,lab_field):
    e=doubleQuote(lab_field)+'='+singleQuote(section)
    r=QgsFeatureRequest().setFilterExpression( e)
    feats=[]
        
    for f in layer.getFeatures(r):
        feats.append(f)

    if len(feats)==1:
        return feats[0]

    if len(feats)==0:
        raise ValueError('section %s not found'%(section))
    
    
def forward_dir(section,layer,lab_field,dir_field):
    f=findSection(layer=layer,lab_field=lab_field,section=section)
    return f[dir_field]

