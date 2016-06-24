# -*- coding: utf-8 -*-
import geojson
from pyspatialite import dbapi2 as db
import os
import json
import glob
import matplotlib.pyplot as plt
import shutil
import datetime
import subprocess
import sys
import qgis
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *

qgisPath = r"/usr"
raiz = os.path.join(os.path.dirname(__file__),"capas")
copiarA = os.path.join(os.path.dirname(__file__),"..","web_src")
nombreBD = "dbMonitoreo.sqlite"
bDatosPath = os.path.join(os.path.dirname(__file__),"..","bd",nombreBD)

def buscarMaximoMinimo(cadena):
    max = 0
    min = 0
    for r in cadena.split("\n"):
        if "STATISTICS_MINIMUM" in r:
            min = float(r.split("=")[-1].strip())        
        elif "STATISTICS_MAXIMUM" in r:
            max = float(r.split("=")[-1].strip())
    return max,min


def buscarNumeroDePuntos(cadena):                                      
    for r in cadena.split("\n"):
        if "Feature Count:" in r:
            return int(r.split(":")[-1].strip())
if __name__ == '__main__':
    print "inicio"
    
    ogr2ogrInstruccion = [
                "ogr2ogr",
                "-f",
                "'ESRI Shapefile'",
                "-t_srs",
                "EPSG:32615",
                "-overwrite",
                os.path.join(raiz,"procesos/estaciones_24hr.shp"),
                os.path.join(raiz,"procesos/estaciones_24hr.geojson")]
 
    stdout, stderr = subprocess.Popen(
                                      " ".join(ogr2ogrInstruccion),
                                      shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()
                                                
    ogrinfoInstruccion = [
                          "ogrinfo",
                          "-so",
                          os.path.join(raiz,"procesos/estaciones_24hr.shp"),
                          "estaciones_24hr"]
    stdout, stderr = subprocess.Popen(
                                      " ".join(ogrinfoInstruccion),
                                      shell=True,stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE).communicate()
      
    numeroDePuntos = buscarNumeroDePuntos(stdout)
    print "Numero de puntos en la capa:",numeroDePuntos
     
    # app = QgsApplication([],True)
    app = QgsApplication([],True)
    app.setPrefixPath(qgisPath, True)
    app.initQgis()
    
    sys.path.append("/usr/share/qgis/python/plugins")
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing

    processing.runalg("grass:v.surf.idw",os.path.join(raiz,"procesos/estaciones_24hr.shp"),numeroDePuntos,2,"precipitac",False,"358437.822632,800904.643622,1586906.09172,2082253.19389",2000,-1.000000,0.000100,os.path.join(raiz,"procesos/interpolacion_24hr.tif"))        
    app.exitQgis()
    app.exit()

    print "fin..........."