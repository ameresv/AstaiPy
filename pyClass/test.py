value = 48
x = 'par' if value % 2 == 0 else 'impar'
print(x)

#%%
data = [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0, 0, 0], 
[0, 1, 1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
[0, 0, 1, 1, 0, 0, 0, 0, 0,1], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], 
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0]]   


# %%
for d in range(1,68):
    exec 'x%s = data[:,%s]' %(d,d-1)

# %%
x = []

for d in xrange(0,66):
    x.append(data[:,d])

# %%
import Calcs as calc

# %%
polygon_data = [(0, 0), (1, 0), (0.5,1)]

# %%
a = calc.centroid(polygon_data)

# %%
a = calc.Calculations()


# %%
import numpy as np

A = np.array([[14,  7, 30],
              [44, 76, 65],
              [42, 87, 11]])

print (A[:,range(1,3)])
print (A[[0, 1, 1], range(len(A))])

# %%
        #unique, counts = np.unique(data[:,3], return_counts=True)
        #b = zip(unique, counts)
        #test = calc.Calculations(polygon_data)

        #data_1 = np.array(data[:,[0,1,2]], copy=True, dtype=np.float64)
        #data_2 = np.unique(data[:,[3,4]], axis = 0)