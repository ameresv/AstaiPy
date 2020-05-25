import os
import ezdxf as DXF
import pandas as pd
from numpy import array as ar
import numpy as np
from shapely.geometry import LinearRing, LineString
#import time
#import matplotlib.pyplot as plt
# Mis librerias
import ReadXmlSetup as Rxml
import Sqlite.Consult as Conq
# Libreia supports Autocad R12 to Autocad R2018

# Pasamos el archivo del plan


class OrigenDXF:
    def __init__(self):
        """Iniciamos la clase OrigenDXF haciendo que consulte la clase de XML, donde le manda el archivo de origen.
        Trabajaremos con dos modulos el de lectura de polylineas(readPolyline) y el solo puntos (readPoint)"""
        # Solo corro para un archivo, posteriormente se debera de incrementar los paths
        FileWork = Rxml.readxml()[0]
        # Obtengo el Nombre del archivo separando las barras.
        self.fileDxf = FileWork
        self.NameFile = (FileWork.split("\\")[-1])[:-4]
        file = DXF.readfile(FileWork)
        self.Sheet = file.modelspace()
        UnitCreate = file.header['$MEASUREMENT']
        UnitPrecition = file.header['$LUNITS']
        VersionFile = file.dxfversion
        # print("    Version de DXF: {0} \n    Unidades del archivo: {1} \n    Presicion guardadas: {2} \n".format(
        #    VersionFile, UnitCreate, UnitPrecition))

    def readPolyline(self):
        """Lee solo dos tipos de linea LWPOLYLINE (2D) y POLYLINE (3D), y devuelve un array con el siguiente formato: \n
        -->  X, Y, Z, File, Layer, Atrib, IDx """
        count = 0
        s = 0
        t = 0
        tt = []
        File = self.NameFile
        PointResult = []
        Project = "Test_1"
        Period = 1
        for idx, Gpline in enumerate(self.Sheet.query('LWPOLYLINE')):
            Elev = Gpline.dxf.elevation
            Index = idx
            Layer = Gpline.dxf.layer
            Atrib1 = 'Cut' if Layer[:3] in {'Cut',"Abi", "POL"} else 'Road' # Por lo pronto depende del nombre
            Element_type = 'Road' if Atrib1 == 'Road' else 'Cut' if Gpline.dxf.flags == 1 else 'aa'  # Por lo pronto depende del nombre
            Atrib = [Elev, File, Layer, Atrib1,Index, Element_type, Project, Period]
            with Gpline.points() as Lines:
                for pp, point in enumerate(Lines):
                    count += 1
                    if Atrib[5] == 'aa':
                        tt.append(Atrib[2])
                        continue
                    else:
                        PointIter = list(point[:2]) + list(Atrib)
                        PointResult.append(PointIter)
            s = idx
        s += 1
        for idx, GGpoly in enumerate(self.Sheet.query('POLYLINE')):
            Index = idx+s
            Layer = GGpoly.dxf.layer
            Atrib1 = 'Cut' if Layer[:3] in {'Cut',"Abi", "POL"} else 'Road' # Por lo pronto depende del nombre
            Element_type = 'Road' if Atrib1 == 'Road' else 'Cut' if Gpline.dxf.flags == 1 else 'bb'  # Por lo pronto depende del nombre
            Atrib = [File, Layer, Atrib1, Index, Element_type, Project, Period]
            for i, locations in enumerate(GGpoly.points()):
                count += 1
                if Atrib[5] == 'bb':
                    tt.append(Atrib[2])
                    continue
                else:
                    PointIter = next if Element_type == None else list(locations) + Atrib
                    PointResult.append(PointIter)
        g = Conq.LoadData(File, Project)
        g.LoadRoads(PointResult)
        VecPoly = ar(PointResult)
        tt1 = list(np.unique(tt, return_counts=True)[0])
        print("Corte {} se encuentra abierto, por favor revisar".format(tt1))
        # TableResult = pd.DataFrame(data=VecPoly, columns=[
        #    "X", "Y", "Z", "File", "Layer", "Atrib", "IDx", "Element_type", "Project", "Period"])
        # TableResult.to_csv("Poly.csv")
        return VecPoly

    def readPoint(self):
        # ID para poder identificar cual es posible origen o destino
        count = 0
        SetID = ["Stk", "Wst", "Ch", "Lp", "Bk"]
        Operation = ["Minado", "Rehandle", "Rehandle LP", "Construccion"]
        File = self.NameFile
        PointsResul = []
        Atrib1 = ""
        Element_type = "Point"
        Project = "Test_1"
        Period = 1
        for Point in (self.Sheet.query('POINT')):
            Layer = Point.dxf.layer
            Index = "LPW{0}".format(count)
            Atrib = [File, Layer, Atrib1, Index, Element_type, Project, Period]
            PoinIter = next if Element_type == None else list(Point.dxf.location) + Atrib
            PointsResul.append(PoinIter)
            count += 1
        VecPoint = ar(PointsResul)
        g = Conq.LoadData(File, Project)
        g.LoadOrgDest(PointsResul)
        # TPointResult = pd.DataFrame(data=VecPoint,
                                    # columns=["X", "Y", "Z", "File", "Layer", "Atrib", "IDx", "Element_type", "Project", "Period"])
        # TPointResult.to_csv("List_Point.csv")
        return VecPoint


# def plot2D(table):
#    fig = table.plot.scatter(
#        x='X', y='Y', color='blue')
#    plt.Axes.set_aspect(fig, 'equal')
#    plt.Axes.ticklabel_format(fig, axis='x', style='sci')
#    plt.show()


class OrigenASCII:
    def __init__(self):
        print("No implentado")


class OrigenDB:
    def __init__(self):
        print("No implentado")


class OrigSQLite:
    def __init__(self):
        super().__init__()
