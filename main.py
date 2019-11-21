import numpy as np
from vispy import app
from vispy import gloo
from vispy import io, plot

SIZE = (600, 600)
TITLE = 'Physarum Polycephalum'
SIZE = 0.1

fname1 = 'teapot.obj'
fname2 = 'sphere.obj'
fig = plot.Fig(title=TITLE)
fig[0, 0].mesh(*io.read_mesh(fname1)[:2])
    
arr = io.read_mesh(fname2)[:2]
for elem in arr[0]:
    elem[0] = elem[0] * SIZE
    elem[1] = elem[1] * SIZE
    elem[2] = elem[2] * SIZE
    
fig[0, 0].mesh(*arr, color=(1, 1, 0.1))
app.run()

if __name__ == "__main__":
    drawOutput([[0, 0, 0], [0.5, 0, 0.5], [0.5, 0, 0], [0, 0, 0.5], [1, 0, 0]])
