from shapely.geometry import LinearRing, LineString, Polygon

class Testing_Close:
    def __init__(self):
        pass
    
    def EvalPolygon(self):
        a = LineString(self).is_closed
        return a

r0 = [(0, 0), (1, 1), (1, 2)]
r0_1 = [(0, 0), (1, 1), (1, 2),(0, 0)]

print('xd' if Testing_Close.EvalPolygon(r0_1) else 'tmr oe')