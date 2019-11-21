import numpy as np
from vispy import scene
from vispy import app, io
import vispy


def mesh_viewer(fname, camera="arcball", bgcolor="black"):

    canvas = scene.SceneCanvas(keys="interactive", show=True, bgcolor=bgcolor)
    view = canvas.central_widget.add_view()

    view.camera = camera

    verts, faces, normals, nothin = io.read_mesh(fname)
    vc = np.zeros((len(verts), 4))
    fc = np.zeros((len(faces), 4))

    vc[:, 3] = 1
    vc[:, 0] = 1

    fc[:, 3] = 1
    fc[:, 1] = 1
    mesh = scene.visuals.Mesh(
        vertices=verts, faces=faces, face_colors=fc, vertex_colors=vc, mode="triangles"
    )
    view.add(mesh)
    app.run()


fname = "teapot.obj"
mesh_viewer(fname)
