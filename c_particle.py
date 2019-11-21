from additional import transmission_matrix, Point
    
class Polyhedron():
    def __init__(self, verteces, faces):
        self.verteces = verteces
        self.faces = faces

class Particle():
    def __init__(self, x, y, z, surface, polyhedron, heading = random.randint(0, 360)):
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
        
    def space_to_face(self, p):
        new_p = Point(0, 0, 0)
        new_p.x = p.x*self.trans_matrix[0, 0] + \
                  p.y*self.trans_matrix[0, 1] + \
                  p.z*self.trans_matrix[0, 2]
        new_p.y = p.x*self.trans_matrix[1, 0] + \
                  p.y*self.trans_matrix[1, 1] + \
                  p.z*self.trans_matrix[1, 2]
        new_p.z = p.x*self.trans_matrix[2, 0] + \
                  p.y*self.trans_matrix[2, 1] + \
                  p.z*self.trans_matrix[2, 2]
        return new_p

    def face_to_space(self, p):
        C = np.linalg.inv(self.trans_matrix)
        new_p = Point(0, 0, 0)
        new_p.x = p.x*C[0, 0] + p.y*C[0, 1] + p.z*C[0, 2]
        new_p.y = p.x*C[1, 0] + p.y*C[1, 1] + p.z*C[1, 2]
        new_p.z = p.x*C[2, 0] + p.y*C[2, 1] + p.z*C[2, 2]
        return new_p

    
    def sense_trail(self, polyhedron, TrailMap):
        '''
        get polyhedron and TrailMap
        return Trail on the rigth and left sensors
        '''
       # get coords of right sensor on (x,y,0) plain
        rcoord = space_to_face(self.coord)# project point to (x,y,0) plain 
        rcoord.x = rcoord.x + SO * np.sin(np.radians(heading + SA))
        rcoord.y = rcoord.y + SO * np.cos(np.radians(heading + SA))
        

        # get coords of left sensor on (x,y,0) plain
        lcoord = space_to_face(self.coord)
        lcoord.x = lcoord.x + SO * np.sin(np.radians(heading - SA))
        lcoord.y = lcoord.y + SO * np.cos(np.radians(heading - SA))

        # get 3D coord of sensors
        rsens = face_to_space(Points(rcoord.x, rcoord.y, 0))
        lsens = face_to_space(Points(lcoord.x, lcoord.y, 0))
        
        return TrailMap[lsens.x, lsens.y, lsens.z], \
               TrailMap[rsens.x, rsens.y, rsens.z]
        pass

        
        
    
    
    