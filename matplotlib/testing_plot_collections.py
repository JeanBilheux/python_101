import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

fig, ax = plt.subplots(1, 1)

x = np.arange(10)
y1 = np.cos(x)
y2 = np.sin(x)

track1 = list(zip(x,y1))
track2 = list(zip(x,y2))

lc = LineCollection([track1, track2], color='b', 
                    lw=[1]*2, 
                    picker=True)
ax.add_collection(lc)
ax.autoscale(True)

def onpick(event):
    if not isinstance(event.artist, LineCollection):
        return

    lws = event.artist.get_linewidths()
    for i in event.ind:
        lws[i] = 4 if lws[i] != 4 else 1
    event.artist.set_linewidths(lws)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('pick_event', onpick)
plt.show()
