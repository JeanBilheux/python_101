import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# A contour plot example:
delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)
#

# first drawing
fig = plt.figure()
ax = fig.add_subplot(111)  # drawing axes
c = ax.contourf(Z)   # contour fill c
cb = fig.colorbar(c)  # colorbar for contour c

# clear first drawimg
ax.clear()  # clear drawing axes
cb.ax.clear()  # clear colorbar axes

# replace with new drawing
# 1. drawing new contour at drawing axes
c_new = ax.contour(Z)  
# 2. create new colorbar for new contour at colorbar axes
cb_new = ax.get_figure().colorbar(c_new, cax=cb.ax) 

plt.show()
