from matplotlib import pyplot as pl
from matplotlib.widgets import MultiCursor
from matplotlib import gridspec
import numpy as np

if __name__ == "__main__":

    fig = pl.gcf()
    gs = gridspec.GridSpec(2,2)

    ax = None
    for g in gs:
        ax = pl.subplot(g, sharex=ax)

    multi = MultiCursor(fig.canvas, tuple(fig.axes),
                        useblit=False, horizOn=True, color='k', lw=1)

    x = np.arange(50,55,0.01)
    y1 = np.sin(x)
    y2 = np.cos(x) + 4
    y3 = 0.2*np.cos(x) - 4
    y4 = np.cos(2*x) - 1

    for ax,y in zip(fig.axes, [y1,y2,y3,y4]):
        ax.plot(x,y)

    for ax in fig.axes:
        ax.grid()

    multi = MultiCursor(fig.canvas, tuple(fig.axes),
                        useblit=False, horizOn=True, color='k', lw=1)
    
    pl.draw()
    pl.show()
