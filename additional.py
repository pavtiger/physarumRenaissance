import numpy as np

class Points():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
def transmission_matrix(surface, polyhedron):
    C = np.zeros((3, 3))
    verA = np.array(polyhedron.verteces[surface[0]])
    verB = np.array(polyhedron.verteces[surface[1]])
    verC = np.array(polyhedron.verteces[surface[2]])
    C[:, 0] = verB - verA
    C[:, 1] = verC - verA
    C[0, 2] = C[1, 0]*C[2, 1] - C[2, 0]*C[1, 1]
    C[1, 2] = C[2, 0]*C[0, 1] - C[0, 0]*C[2, 1]
    C[2, 2] = C[0, 0]*C[1, 1] - C[1, 0]*C[0, 1]
    return C

def get_distance(a, b):
	return np.sqrt(np.sum((a - b)*(a - b)))
