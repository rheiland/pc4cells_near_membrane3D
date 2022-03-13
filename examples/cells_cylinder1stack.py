# python cells_cylinder.py 100 8 >cyl1.csv
import sys
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



cyl_radius = float(sys.argv[1])
# height_scale = float(sys.argv[2])

# cell_radius = 1.  # ~2 micron spacing
cell_radius = 8.4127  # PhysiCell_phenotype.cpp
cell_diam = cell_radius*2

theta_half = np.arcsin(cell_radius/cyl_radius)
# print("theta_half = ",theta_half)
theta = theta_half * 2
theta = theta_half * 1.6 # make a bit less to have overlap
# print("theta= ",theta)

cell_diam = cell_radius*2

ncells_per_ring = int(2*np.pi / theta)

zv = 0
#for t0 in [0., theta_half, 2*theta_half]:
theta_del = theta/2.0
for t0 in [0., theta_del, 2*theta_del, 3*theta_del, 4*theta_del]:
    # for t in np.arange(t0, 2*np.pi, theta):
    t = t0
    for idx in range(ncells_per_ring):
        xv = cyl_radius * np.cos(t) 
        yv = cyl_radius * np.sin(t)
        print(xv,',',yv,',',zv,', 0,0')
        t += theta 
    zv += cell_diam - 2.5

fig = plt.figure()
ax = plt.axes(projection='3d')
# set_axes_equal(ax)
# ax.set_aspect('equal')

#ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
# ax.scatter3D(cells_x, cells_y, cells_z)

# plt.show()
