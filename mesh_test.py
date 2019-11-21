import numpy as np
from vispy import app, io
import vispy

SIZE = (600, 600)
TITLE = 'Physarum Polycephalum'

def mesh_viewer(fname, camera="arcball"):

    canvas = app.Canvas(keys="interactive", show=True, title=TITLE, size=SIZE)
    view = canvas.central_widget.add_view()

    view.camera = camera

    verts, faces, normals, nothin = io.read_mesh(fname)
    vc = np.zeros((len(verts), 4))
    fc = np.zeros((len(faces), 4))

    vc[:, 3] = 1
    vc[:, 0] = 1

    fc[:, 3] = 1
    fc[:, 1] = 1
    mesh = app.visuals.Mesh(
        vertices=verts, faces=faces, face_colors=fc, vertex_colors=vc, mode="triangles"
    )
    view.add(mesh)
    app.run()


fname = "teapot.obj"
mesh_viewer(fname)
