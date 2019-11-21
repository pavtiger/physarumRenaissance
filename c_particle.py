class Point():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Particle():
    def __init__(self, x, y, z, heading = random.randint(0, 360), surface):
        """
            Initializing the particle(agent)
            param SA: sensor angle
            param RA: rotation angle of angle
            param SO: sensor distance 
            param SS: agent's step size
            param depT: trail distance
            param x, y, z: agent's coordinates
            param heading: agent's angle relative to its surface
            param surface: 3 vertexes of polyhedron
            param trails: array with trail's coordinates
        """
        self.SA = 45
        self.RA = 20
        self.SO = 9
        self.SS = 0.5
        self.depT = 5
        self.food = 255
        self.foodTrH = 20
        self.coord = Point(x, y, z)
        self.heading = heading
        self.surface = surface
        self.trail = np.zeros((5, 2))
    
    def count_step_size(self):
        self.SS = 1
		
	def transmission_matrix(self, polyhedron):
		C = np.zeros((3, 3))
		verA = polyhedron.vertex[self.surface[0]]
		verB = polyhedron.vertex[self.surface[1]]
		verC = polyhedron.vertex[self.surface[2]]
		C[:, 0] = verB - verA
		C[:, 1] = verC - verA
		C[0, 2] = C[1, 0]*C[2, 1] - C[2, 0]*C[1, 1]
		C[1, 2] = C[2, 0]*C[0, 1] - C[0, 0]*C[2, 1]
		C[2, 2] = C[0, 0]*C[1, 1] - C[1, 0]*C[0, 1]
		return C
		
	
		
		
	
	
	
	
	