import numpy as np
from vispy import app
from vispy import gloo
from vispy import io, plot

SIZE = (600, 600)
TITLE = 'Physarum Polycephalum'
SIZE = 0.1

def drawOutput(organism):
    fname1 = 'teapot.obj'
    fname2 = 'sphere.obj'
    fig = plot.Fig(title=TITLE)
    fig[0, 0].mesh(*io.read_mesh(fname1)[:2])
        
    arr = io.read_mesh(fname2)[:2]
    for dot in organism:
        a = arr
        for elem in a[0]:
            elem[0] = elem[0] * 1 + dot[0]
            elem[1] = elem[1] * 1 + dot[1]
            elem[2] = elem[2] * 1 + dot[2]
        #print('workin')
    fig[0, 0].mesh(*arr, color=(1, 1, 0.1))
    
    vispy.
            
    app.run()

if __name__ == "__main__":
    print('hey')
    drawOutput([[0, 0, 0.5], [0, 0, 0.5], [0, 0, 0], [0.5, 0, 0], [0, 0, 0]])
