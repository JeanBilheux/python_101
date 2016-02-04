import dask
import dask.array as da

x = da.random.normal(10, 0.1, size=(2000, 2000), chunks=(100, 100))
result = x.mean()

from dask.dot import dot_graph


dot_graph(result.dask)
