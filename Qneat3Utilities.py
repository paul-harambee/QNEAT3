"""
***************************************************************************
    Qneat3Utilities.py
    ---------------------
    Date                 : November 2017
    Copyright            : (C) 2017 by Clemens Raffler
    Email                : clemens dot raffler at gmail dot com
***************************************************************************
"""
from qgis.core import *
from qgis.analysis import *

from PyQt5.QtCore import QVariant

def AssignAnalysisCrs(vlayer):
    logPanel("Setting analysis CRS")
    AnalysisCrs = vlayer.crs()
    return AnalysisCrs

def logPanel(message):
    QgsMessageLog.logMessage(message, "QNEAT3")
    
def isGeometryType(vlayer, type_obj):
    geom_type = vlayer.geometryType()
    if geom_type == type_obj:
        return True
    else:
        return False

def buildQgsVectorLayer(string_geomtype, string_layername, crs, list_geometry, list_qgsfield):
    
    #create new vector layer from self.crs
    vector_layer = QgsVectorLayer(string_geomtype, string_layername, "memory")
    
    #set crs from class
    vector_layer.setCrs(crs)
    
    #set fields
    provider = vector_layer.dataProvider()
    provider.addAttributes(list_qgsfield) #[QgsField('fid',QVariant.Int),QgsField("origin_point_id", QVariant.Double),QgsField("iso", QVariant.Int)]
    vector_layer.updateFields()
    
    #fill layer with geom and attrs
    vector_layer.startEditing()
    for i, geometry in enumerate(list_geometry):
        feat = QgsFeature()
        feat.setGeometry(geometry)#geometry from point
        feat.setAttributes(list_qgsfield[i])
        vector_layer.addFeature(feat, True)
    vector_layer.commitChanges()

    return vector_layer


def getFeaturesFromQgsIterable(qgs_feature_storage):#qgs_feature_storage can be any vectorLayer/QgsProcessingParameterFeatureSource/etc
    fRequest = QgsFeatureRequest().setFilterFids(qgs_feature_storage.allFeatureIds())
    return qgs_feature_storage.getFeatures(fRequest)

def getFieldIndexFromQgsProcessingFeatureSource(feature_source, field_name):
    if field_name != "":
        return feature_source.fields().lookupField(field_name)
    else:
        return -1

def getListOfPoints(qgs_feature_storage): #qgs_feature_storage can be any vectorLayer/QgsProcessingParameterFeatureSource/etc
    given_geom_type = QgsWkbTypes().displayString(qgs_feature_storage.wkbType()) #GetStringRepresentation of WKB Type
    expected_geom_type = QgsWkbTypes.displayString(1) #Point
    
    if given_geom_type == expected_geom_type: 
        qgsfeatureiterator = getFeaturesFromQgsIterable(qgs_feature_storage)
        return [f.geometry().asPoint() for f in qgsfeatureiterator]
    else:
        raise Qneat3GeometryException(given_geom_type, expected_geom_type)
        
