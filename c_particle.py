class Point():
    def __init__(self, x, y, z):
        self.x = x
	self.y = y
	self.z = z

def transmission_matrix(surface, polyhedron):
    C = np.zeros((3, 3))
    verA = polyhedron.vertex[surface[0]]
    verB = polyhedron.vertex[surface[1]]
    verC = polyhedron.vertex[surface[2]]
    C[:, 0] = verB - verA
    C[:, 1] = verC - verA
    C[0, 2] = C[1, 0]*C[2, 1] - C[2, 0]*C[1, 1]
    C[1, 2] = C[2, 0]*C[0, 1] - C[0, 0]*C[2, 1]
    C[2, 2] = C[0, 0]*C[1, 1] - C[1, 0]*C[0, 1]
    return C

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
        self.trans_matrix = transmission_matrix(surface, polyhedron)
    
    def count_step_size(self):
        self.SS = 1
		
    def space_to_face(self)
    

    
    def sense_trail(self, polyhedron, TrailMap):
        '''
        get polyhedron and TrailMap
        return Trail on the rigth and left sensors
        '''
        # get coords of right sensor on (x,y,0) plain
        rcoord = space_to_face(self.coord)# project point to (x,y,0) plain 
        rcoord.x = fcoord.x + SO * np.sin(np.radians(RA + SA))
        rcoord.y = fcoord.y + SO * np.cos(np.radians(RA + SA))
        

        # get coords of left sensor on (x,y,0) plain
        lcoord = space_to_face(self.coord)
        lcoord.x = lcoord.x + SO * np.sin(np.radians(RA - SA))
        lcoord.y = lcoord.y + SO * np.cos(np.radians(RA - SA))

        # get 3D coord of sensors
        rsens = face_to_space(Points(rcoord.x, rcoord.y, 0)
	lsens = face_to_space(Points(lcoord.x, lcoord.y, 0)

	return TrailMap[lsens.x, lsens.y, lsens.z], \
               TrailMap[rsens.x, rsens.y, rsens.z]

		
		
	
	
	
	
	
