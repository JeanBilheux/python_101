import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from tutorial import track_loader

tracks = track_loader('data/polygons.shp')
# Filter out non-tracks (unassociated polygons given trackID of -9)
tracks = {tid: t for tid, t in tracks.items() if tid != -9}

fig, ax = plt.subplots(1, 1)
lc = LineCollection(tracks.values(), color='b', lw=[1]*len(tracks), picker=True)
ax.add_collection(lc)
ax.autoscale(True)

selected = None
def onpick(event):
    global selected
    if event.artist is not lc:
        return
    lws = lc.get_linewidths()

    ind = event.ind[0]
    if ind != selected:
        # "Select" this track
        # But first, we need to de-select the previous selection
        if selected is not None:
            lws[selected] = 1
        lws[ind] = 4
        selected = ind
    else:
        # "Deselect this track
        lws[ind] = 1
        selected = None
    lc.set_linewidths(lws)
    fig.canvas.draw_idle()

def keypress(event):
    global selected
    if event.key == 'd' and selected is not None:
        segs = lc.get_segments()
        segs.pop(selected)
        selected = None
        lc.set_segments(segs)
        # Also need to reset the linewidths list
        lc.set_linewidths([1] * len(segs))
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('key_press_event', keypress)

plt.show()
