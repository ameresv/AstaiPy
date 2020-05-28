class Calculations:
    def __init__(self,vertexes):
        self.vertexes = vertexes

    def centroid(self):
        x_list = [vertex[0] for vertex in self.vertexes]
        y_list = [vertex[1] for vertex in self.vertexes]
        z_list = [vertex[2] for vertex in self.vertexes]
        _len = len(self.vertexes)
        _x = sum(x_list) / _len
        _y = sum(y_list) / _len
        _z = sum(z_list) / _len
        return(_x, _y, _z)
