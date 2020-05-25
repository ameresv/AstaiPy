import numpy as np
import pandas as pd
import pyClass.InputRead as inFile
import math as MT
import time as tm
from collections import defaultdict


class CatalogLine:
    """
    Clase para el calculo de la distancia equivalente, esta clase solicita el tipo de dato de origen
    de la informacion, aun se estan implementando 1 de las 3 posibles formar de ingresar la informacion.
    """

    def __init__(self, TypeD):
        """
        Debemos ingresar el oringen de los datos:\n
        \t0 --> ASCII Format Version Srg (Minesight)\n
        \t1 --> DXF file\n
        \t2 --> Database Access (Minesight)
        """
        # Origen de datos
        self.TypeD = TypeD
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
        que depende de como se ha dise;ado y guardado en su respectivo archivo. El input es un array.
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
#        nodos2 = np.zeros((1, 3))
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
                       ('Coo_INI', np.float32, (3,)), ('Coor_FIN', np.float32, (3,))])
        MatrixIF = np.zeros(1, dt)
        for z in range(0, len(indices)//2):
            a = 2*z
            Dte = (indices[a], indices[a+1])
            TempRsl = np.array(
                [(NameSegment[z], Dte, Uqnodos[indices[a]], Uqnodos[indices[a+1]])], dtype=dt)
            MatrixIF = np.concatenate([MatrixIF, TempRsl])
        MatrixIF = np.delete(MatrixIF, 0, axis=0)

        VectorR = MatrixIF['PI-PF']
        print(VectorR)
        g = Graph()
        ####################################################################
        for i in range(0, len(indices)//2):
            g.addEdge(indices[i*2], indices[i*2+1])
            g.addEdge(indices[i*2+1], indices[i*2])
        print(g.find_all_paths(3, 1))

        print("-----------")
        ####################################################################

        c = 0
        b = 0
        for name in NameSegment:
            Indx = [str(name)]
            PolIni = arr[c][:3]
            for i in range(c, c+countSeg[b]-1):
                PointINI = arr[i][:3].astype('float')
                PointFIN = arr[i+1][:3].astype('float')
                catlg.append(self.__Distancia(PointINI, PointFIN))
                resulseg = Indx + catlg
            PolFin = arr[c+countSeg[b]-1][:3]
            resul = np.vstack((PolIni, PolFin)).astype(float)
            c = c + countSeg[b]
            b += 1

    def __Distancia(self, INI, FIN):
        # Validamos que INI y FIN no sean iguales por error
        if(INI != FIN).all:
            # La distancia se trabaja en metros (Configuracion por defecto en MS)
            LnLong = MT.sqrt((INI[0]-FIN[0])**2 +
                             (INI[1]-FIN[1])**2+(INI[2]-FIN[2])**2)
            # La pendiente se expresa en porcentaje
            LnPend = (FIN[2]-INI[2])*100 / \
                MT.sqrt((INI[0]-FIN[0])**2 + (INI[1]-FIN[1])**2)
            DistPend = [LnLong, LnPend]
            # print(DistPend)
            self.__Velocidad(LnPend, LnLong)
            # print(self.__Velocidad(LnPend, LnLong))
            # Voy asumir q conozco ya la longitu de las distancias
            return DistPend
        else:
            DistPend = [0, 0]
            print("INI ={0} - FIN = {1}".format(INI, FIN))
            return DistPend

    def __Velocidad(self, pend, LongSg):
        '''
        Se separa en segmentos, manejamos estandar por ahora:\n
        Pend %      -10 -7  -3   3   7  10\n
        VelcLoad   25  35  45  35  25 15 15\n
        VelcEmpty  35  40  45  45  35 25 15\n
        '''
        VelcPend = []
        PendiStand = [-10, -7, -3, 3, 7, 10]  # 7 Campos al final
        VelcEmpty = [35, 40, 45, 45, 35, 25, 10]
        VelcLoad = [25, 35, 45, 35, 25, 15, 15]
        longPend = len(PendiStand)+1
        b = 0
        ZeroPend = 0
        for p in range(0, len(PendiStand)-1):
            if (PendiStand[p] <= 0 and PendiStand[p+1] >= 0):
                ZeroPend = (b+1)
                break
            b += 1
        # Las velocidades deben tener las misma dimension en el array.
        count = 0
        if len(VelcEmpty) == len(VelcLoad):
            VelcPend.append(LongSg)
            for a in range(longPend):
                if a == 0:
                    if pend <= PendiStand[a]:
                        VelcPend.append(LongSg/(VelcEmpty[a]*1000))
                        VelcPend.append(LongSg/(VelcLoad[a]*1000))
                        # Para determinar la distancia equivalente
                        VelcPend.append(
                            VelcEmpty[ZeroPend]*LongSg/VelcEmpty[a])
                        VelcPend.append(VelcEmpty[ZeroPend]*LongSg/VelcLoad[a])
                        count = a
                        VelcPend.append(count)
                        break
                elif (a+1 == longPend):
                    if PendiStand[a-1] <= pend:
                        VelcPend.append(LongSg/(VelcEmpty[a]*1000))
                        VelcPend.append(LongSg/(VelcLoad[a]*1000))
                        # Para determinar la distancia equivalente
                        VelcPend.append(
                            VelcEmpty[ZeroPend]*LongSg/VelcEmpty[a])
                        VelcPend.append(VelcEmpty[ZeroPend]*LongSg/VelcLoad[a])
                        count = a
                        VelcPend.append(count)
                else:
                    if PendiStand[a-1] < pend <= PendiStand[a]:
                        VelcPend.append(LongSg/(VelcEmpty[a]*1000))
                        VelcPend.append(LongSg/(VelcLoad[a]*1000))
                        # Para determinar la distancia equivalente
                        VelcPend.append(
                            VelcEmpty[ZeroPend]*LongSg/VelcEmpty[a])
                        VelcPend.append(VelcEmpty[ZeroPend]*LongSg/VelcLoad[a])
                        count = a
                        VelcPend.append(count)
                        break
        else:
            print("Las velocidades no tienen el formato necesario")
        # Format Export
        # [18.819310535470112, 0.0018819310535470113, 0.0012546207023646741, 84.68689740961551, 56.457931606410334, 6]
        # Longitud          , Time Empty           , Time Load
        return VelcPend


class Graph:
    '''A recursive function to print all paths from 'u' to 'd'.
        visited[] keeps track of vertices in current path.
        path[] stores actual vertices and path_index is current
        index in path[]'''

    def __init__(self):
        # default dictionary to store graph
        self.graph = defaultdict(list)

    # function to add an edge to graph

    def addEdge(self, u, v):
        self.graph[u].append(v)
        # print(self.graph[u])
    # function to generate all possible paths

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not start in self.graph:
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths


aa = tm.time()
Obj = CatalogLine(1)
Orden = Obj.RevPoly()
bb = tm.time()
print(bb-aa)
