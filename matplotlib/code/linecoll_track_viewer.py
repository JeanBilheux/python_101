import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from tutorial import track_loader

tracks = track_loader('polygons.shp')
# Filter out non-tracks (unassociated polygons given trackID of -9)
tracks = {tid: t for tid, t in tracks.items() if tid != -9}

fig, ax = plt.subplots(1, 1)
lc = LineCollection(tracks.values(), color='b')
ax.add_collection(lc)
ax.autoscale(True)
plt.show()
