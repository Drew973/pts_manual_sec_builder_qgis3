# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:25:51 2022

@author: Drew.Bennett
"""

from . import rte_item
from qgis.core import QgsCoordinateTransform,QgsCoordinateReferenceSystem,QgsProject,QgsGeometry



#fields:dict of key:field with key per field of rte item
#crs:QgsCoordinateReferenceSystem. get with layer.crs()
def featureToRteItem(feature,fields,crs,rev=False):
    
    v = featureToDict(feature,fields)    
    t = QgsCoordinateTransform(crs,QgsCoordinateReferenceSystem('ESPG27700'),QgsProject.instance())#transform to espg 27700
    geom = QgsGeometry(feature.geometry())
    geom.transform(t)
       
    s = startPoint(geom)
    e = endPoint(geom)
    
    v.update({'start_x':s.x(),'start_y':s.y(),'end_x':e.x(),'end_y':e.y()})

    v.update({'survey_direction':v['section_direction']})        
        
    i = rte_item.rteItem(**v)

    if rev:
        i.flip_direction()#this swaps start and end coordinates

    return i



#fields is dict of key:fieldName
#returns dict of key:attribute
def featureToDict(feature,fields):
    featureFields = feature.fields().names()
    r = {}
    for k in fields:
        if fields[k] in featureFields:
            r[k] = feature[fields[k]]
        else:
            r[k] = None
    return r
    

def startPoint(geom):    
    for v in geom.vertices():
        return v
 
      
      
def endPoint(geom):  
    # p = geom.interpolate(geom.length())#Null for MultilineString with multiple parts
    #if not p.isNull():
     #   return p.asPoint() 
    
    for v in geom.vertices():
        pass
    
    return v
    