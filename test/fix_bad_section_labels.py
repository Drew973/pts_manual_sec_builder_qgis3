# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:02:39 2026

@author: Drew.Bennett



use section labels from 20260523_06.rte to set "label" field of layer.
layer has "Section Id" field that partially matches rte section label

"""

from qgis.core import QgsFeatureRequest,QgsVectorLayer , QgsFeature , QgsProject


from manual_sec_builder.scanner_rte import scanner_rte

rteFile = r'C:\Users\drew.bennett\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\manual_sec_builder\test\greece\20260523_06.rte'

layer = QgsProject.instance().mapLayersByName('TRR1_incDescriptions')[0]

col = layer.fields().indexOf('label')


with open(rteFile,'r') as f:
    for line in f.readlines():
        
        r = scanner_rte.R2_1.try_from_line(line)
        if r is not None:
            print(r.section_label)

            #filt = '("2021Length" - {sl})*("2021Length" - {sl}) < 100'.format(sl = r.section_length)
            
            lab = r.section_label[1:]
            filt = '"Section Id" like \'%{lab}%\''.format(lab = lab)
            print(filt)
            request = QgsFeatureRequest().setFilterExpression(filt)
            feats = [f for f in layer.getFeatures(request)]
            
            print(feats)
            
            if len(feats) == 1:
                feat = feats[0]
                layer.changeAttributeValue(feat.id(), col, r.section_label)