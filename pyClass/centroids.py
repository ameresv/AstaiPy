#%%
import numpy as np

# %%
def centroid(vertexes):
    x_list = [vertex[0] for vertex in vertexes]
    y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(x_list) / _len
    _y = sum(y_list) / _len
    return(_x, _y)

# %%
polygon_data = [(0, 0), (1, 0), (1, 1), (0, 1)]

# %%
centroid(polygon_data)

# %% Minina Distancia
import math

def dot(v,w):
    x,y,z = v
    X,Y,Z = w
    return x*X + y*Y + z*Z

def length(v):
    x,y,z = v
    return math.sqrt(x*x + y*y + z*z)

def vector(b,e):
    x,y,z = b
    X,Y,Z = e
    return (X-x, Y-y, Z-z)

def unit(v):
    x,y,z = v
    mag = length(v)
    return (x/mag, y/mag, z/mag)

def distance(p0,p1):
    return length(vector(p0,p1))

def scale(v,sc):
    x,y,z = v
    return (x * sc, y * sc, z * sc)

def add(v,w):
    x,y,z = v
    X,Y,Z = w
    return (x+X, y+Y, z+Z)

#%% Explicación del algoritmo (Fuente: http://www.fundza.com/vectors/point2line/index.html)
# Given a line with coordinates 'start' and 'end' and the
# coordinates of a point 'pnt' the proc returns the shortest 
# distance from pnt to the line and the coordinates of the 
# nearest point on the line.
#
# 1  Convert the line segment to a vector ('line_vec').
# 2  Create a vector connecting start to pnt ('pnt_vec').
# 3  Find the length of the line vector ('line_len').
# 4  Convert line_vec to a unit vector ('line_unitvec').
# 5  Scale pnt_vec by line_len ('pnt_vec_scaled').
# 6  Get the dot product of line_unitvec and pnt_vec_scaled ('t').
# 7  Ensure t is in the range 0 to 1.
# 8  Use t to get the nearest location on the line to the end
#    of vector pnt_vec_scaled ('nearest').
# 9  Calculate the distance from nearest to pnt_vec_scaled.
# 10 Translate nearest back to the start/end line. 
# Malcolm Kesson 16 Dec 2012

def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist, nearest)


# %%
pnt = (2,0,0.5)
start = (1,0,2)
end = (4.5,0,0.5)

# %%
pnt2line(pnt = pnt, start = start, end = end)

# %%
from shapely.geometry import LinearRing, LineString, Polygon

# %%
r0 = [(0, 0), (1, 1), (1, 2)]
r1 = LineString([(0, 0), (1, 1), (1, 2), (0, 0)])
r2 = LinearRing([(0, 0), (1, 1), (1, 2)])
r3 = LineString(r0)

# %%
s0 = Polygon(r0)
s1 = Polygon(r1)
s2 = Polygon(r2)
s3 = Polygon(r3)

# %%
s.area

# %%
test = [(803676.680268817, 9120464.63376052),
(803707.19531476, 9120486.99913016),
(803738.291596794, 9120486.99913016),
(803759.797439182,9120457.37227766),
(803756.019384524,9120435.00690802),
(803723.17938619, 9120428.32634332),
(803676.680268817, 9120464.63376052)]

test2 = [
(803629.285522461, 9120502.73858642),
(803634.688476563, 9120529.8371582),
(803671.435546875, 9120568.63781739),
(803692.326782226, 9120575.3706665),
(803701.778808594, 9120560.84515381),
(803711.146362305, 9120546.0045166),
(803721.675903321, 9120527.30529785),
(803694.442138672, 9120498.79296875),
(803659.670166016, 9120485.64465332),
(803646.283447266, 9120496.83270264)
]

test3 = [
(803598.575683594, 9120572.07415772),
(803571.802001953, 9120583.25982666),
(803547.443237305, 9120614.49029541),
(803550.797973633, 9120640.40637207),
(803578.855834961, 9120670.26025391),
(803601.83581543, 9120683.52783203),
(803634.936157227, 9120689.6496582),
(803640.645385742, 9120684.95275879),
(803654.780883789, 9120651.81652832),
(803674.735961914, 9120629.36706543)
]

test4 = [(803676.680268817, 9120464.63376052),
(803707.19531476, 9120486.99913016),
(803738.291596794, 9120486.99913016),
(803759.797439182, 9120457.37227766),
(803756.019384524, 9120435.00690802),
(803723.17938619, 9120428.32634332),
(803676.680268817, 9120464.63376052)]
# %%
t1 = LineString(test)
t2 = LineString(test2)
t3 = LineString(test3)
t4 = LineString(test4)

# %%
t1_1 = Polygon(t1)
t2_1 = Polygon(t2)
t3_1 = Polygon(t3)

# %%
