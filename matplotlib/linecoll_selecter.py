import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from tutorial import track_loader

tracks = track_loader('data/polygons.shp')
# Filter out non-tracks (unassociated polygons given trackID of -9)
tracks = {tid: t for tid, t in tracks.items() if tid != -9}

fig, ax = plt.subplots(1, 1)
lc = LineCollection(tracks.values(), color='b', 
                    lw=[1]*len(tracks), 
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
