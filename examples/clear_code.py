import numpy as np
from vispy import app, scene
from vispy import gloo
from vispy import io, plot

SIZE = (600, 600)
TITLE = 'Physarum Polycephalum'

c = app.Canvas(keys='interactive', title=TITLE, size=SIZE)
vertex = """
attribute vec2 a_position;
void main (void) {
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""
fragment = """
void main() {
    gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

program = gloo.Program(vertex, fragment)

program['a_position'] = np.c_[
        np.random.uniform(-0.5, +0.5, 1000).astype(np.float32),
        np.random.uniform(-0.5, +0.5, 1000).astype(np.float32)]

''''''
fname1 = 'teapot.obj'
fname2 = 'sphere.obj'
fig = plot.Fig()
fig[0, 0].mesh(*io.read_mesh(fname1)[:2])
fig[0, 0].mesh(*io.read_mesh(fname2)[:2])
''''''
                                 
@c.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)
    
@c.connect
def on_draw(event):
    gloo.clear((0,0,0,1))
    program.draw('points')

if __name__ == "__main__":
    c.show()
    app.run()
