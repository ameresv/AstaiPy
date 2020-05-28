import numpy as np
import pandas as pd
import math as MT
import time as tm
from collections import defaultdict
from shapely.geometry import LinearRing, LineString, Polygon
# Mis modulos
import InputRead_w_cuts as inFile
import Sqlite.Consult as Conq
import Calcs as calc


class CatalogLine:
    """
    Clase para el calculo de la distancia equivalente, esta clase solicita el tipo de dato de origen
    de la informacion, aun se estan implementando 1 de las 3 posibles formar de ingresar la informacion.
    """

    def __init__(self, TypeD, Project):
        """
        Debemos ingresar el oringen de los datos:\n
        \t0 --> ASCII Format Version Srg (Minesight)\n
        \t1 --> DXF file\n
        \t2 --> Database Access (Minesight)
        """
        # Origen de datos
        self.TypeD = TypeD
        self.Project = Project
        if TypeD == 0:
            Data = inFile.OrigenASCII()
        elif TypeD == 1:
            Data = inFile.OrigenDXF()
            self.DataPoly = Data.readPolyline()
            self.DataPoint = Data.readPoint()
        elif TypeD == 2:
            Data = inFile.OrigenDB()
        else:
            print("Metodo buscado no encontrado")

    def RevPoly(self):
        """
        Una vez leido el formato de ingreso de la infomacion (Convencion), se asume un orden en la rutas
        que depende de como se ha diseñado y guardado en su respectivo archivo. El input es un array.
        """
        # Formato de tabla importada
        #          0                    1                 2               3         4       5       6
        # ['803564.8000488281' '9120284.502990725' '4122.947021484375' '2020v2' 'Road_STK' 'road' 'PL1']
        # Declaramos la variable arr que contrendra todo el array pasado
        arr = self.DataPoly
        # Obtenemos el nombre de todos las polilineas y nos aseguramos q no sean repetidos.
        # Los nombres son numeros enteros debido a la propiedad UNIQUE empleado
        NameSegment, countSeg = np.unique(
            np.int_(arr[:, 6]), return_counts=True)  # Esto es una lista

        b = 0  # Contador de polylineas
        c = 0  # Contador para el array, ve la ubicacion de cada valor en el array
        #            Time     -10  -7   -3    3    7    10       EFHc EFHv
        # ____________ 0    1    2    3    4    5    6    7    8    9    10
        catlg = []
        # Iniciamos un artificio, declaramos un array con ceros
        # [0,0,0],[INI],[FIN],[INI],[FIN],[INI],[FIN],[INI],[FIN],[INI],[FIN]
        nodos = np.zeros((1, 3))
        index = []
        for name in NameSegment:  # [0,1,2]
            NodoINI = arr[c][:3].astype(float)
            NodoFIN = arr[c+countSeg[b]-1][:3].astype(float)
            # [INI],[FIN],[INI],[FIN],[INI],[FIN],[INI],[FIN],[INI],[FIN]
            nodos = np.concatenate((nodos, [NodoINI], [NodoFIN]), axis=0)
            c = c + countSeg[b]
            b += 1
        # Terminamos el artificio y borramos el primer elemento
        nodos = np.delete(nodos, 0, axis=0)

        k = 0
        Uqnodos, indices = np.unique(nodos, axis=0, return_inverse=True)
        ####################################################################
        dt = np.dtype([('Id', np.uint32, (1,)), ('PI-PF', np.uint32, (2,)),
                       ('Coo_INI', np.float32, (3,)), ('Coor_FIN', np.float32, (3,))])  # , ('Project_Id', np.unicode_, (5,))
        MatrixIF = np.zeros(1, dt)
        for z in range(0, len(indices)//2):
            a = 2*z
            Dte = (indices[a], indices[a+1])
            TempRsl = np.array(
                [(NameSegment[z], Dte, Uqnodos[indices[a]], Uqnodos[indices[a+1]])], dtype=dt)
            MatrixIF = np.concatenate([MatrixIF, TempRsl])
        MatrixIF = np.delete(MatrixIF, 0, axis=0)
        VectorR = MatrixIF.tolist()
        Array2D = self.LongPend()
        g = Conq.LoadData('2020v2', 'Test_1')
        g.LoadCompactRoad(Array2D)

    def LongPend(self):
        List_Seg = self.DataPoly
        Vector = np.array(
            List_Seg[:, [0, 1, 2]], copy=True, dtype=np.float64)
        ID_Vector = np.array(List_Seg[:, [6, 5, 4, 8]], copy=True)
        # Format Array:
        ArrResult = np.zeros(6)
        a = 0
        while a < (len(ID_Vector)-1):
            if (ID_Vector[a][0] == ID_Vector[a+1][0]):
                Dif_Vector = Vector[a+1] - Vector[a]
                LongVector = MT.sqrt(
                    Dif_Vector[0]**2+Dif_Vector[1]**2+Dif_Vector[2]**2)
                Denomi = MT.sqrt(Dif_Vector[0]**2+Dif_Vector[1]**2)
                if Denomi == 0:
                    print("Error: {0}".format(a))
                    PendVector = 100
                else:
                    PendVector = Dif_Vector[2]*100 / Denomi
                result = np.array([LongVector, PendVector])
                VectResul = np.append(ID_Vector[a+1], result)
                ArrResult = np.vstack((ArrResult, VectResul))
            a += 1
        ArrResult = np.delete(ArrResult, 0, axis=0)
        return ArrResult

    def Cut_Cent(self):
        Cuts = self.DataPoly
        Coord = np.array(Cuts)
        data = Coord[np.where(Coord[:,7] == "Cut")] # Filtro solo los cortes
        filtro = np.unique(data[:,4], axis = 0) # valor = 2. Revisar orden de datos!
        data_i = [data[:,:3][np.where(data[:,4] == filtro[i])] for i in range(0,len(filtro))] # Coordenadas por cortes

        a = 0 #contador de coordenadas
        s = 0
        b = np.zeros(3) #array de resultados

        for a in range(0, len(filtro)):
            s = np.array(data_i[a], dtype=np.float64)
            test = calc.Calculations(s)
            b = np.vstack((b,test.centroid())) 

        b = np.delete(b, 0, axis=0) # Se eliminan los ceros y se convierte en el array con los centroides calculados (x,y,z)

        data_i2 = [data[:,range(3,10,1)][np.where(data[:,4] == filtro[i])] for i in range(0,len(filtro))] # Datos por cortes
        data_i2 = np.array(data_i2) # los convierto en np array
        filtro2 = np.array([1]*len(filtro)) # indice de unos para la extracción de los datos del corte   

        data_i3 = data_i2[np.arange(data_i2.shape[0]),filtro2,:] # datos de los cortes
        data_i3[:,-3] = 'Point' # cambiando el Element_type a 'Point'
        data_i3[:,-5] = 'Centroid' # cambiando el Atrib a 'Centroid'

        c = np.concatenate([b,data_i3], axis = 1)

        g = Conq.LoadData('2020v2', 'Test_1')
        g.LoadRoads(c)


aa = tm.time()
Obj = CatalogLine(1, "Test_1")
Orden = Obj.Cut_Cent()
bb = tm.time()
print(bb-aa)

CatalogLine
