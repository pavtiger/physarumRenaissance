from additional import transmission_matrix, Point
import random
import numpy as np
    
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
        self.trans_matrix = np.array(transmission_matrix(surface, polyhedron))
    
    def count_step_size(self):
        self.SS = 1
        
    def space_to_face(self, p):
        print(self.trans_matrix)
        new_p = Point(0, 0, 0)
        delta_p = np.array([p.x, p.y, p.z]) - np.array([self.coord.x, self.coord.y, self.coord.z])
        new_p.x, new_p.y, new_p.z = self.trans_matrix @ delta_p
        return new_p

    def face_to_space(self, p):
        C = np.linalg.inv(self.trans_matrix)
        new_p = Point(0, 0, 0)
        new_p.x, new_p.y, new_p.z = C@np.array([p.x, p.y, p.z]) + \
                            np.array([self.coord.x, self.coord.y, self.coord.z])
        return new_p

    
    def sense_trail(self, polyhedron, TrailMap):
        '''
        get polyhedron and TrailMap
        return Trail on the rigth and left sensors
        '''
        # get coords of right sensor on (x,y,0) plain
        rcoord = space_to_face()   # project point to (x,y,0) plain 
        rcoord.x = rcoord.x + SO * np.sin(np.radians(heading + SA))
        rcoord.y = rcoord.y + SO * np.cos(np.radians(heading + SA))
        
        # get coords of left sensor on (x,y,0) plain
        сcoord = space_to_face()
        сcoord.x = сcoord.x + SO * np.sin(np.radians(heading - SA))
        сcoord.y = сcoord.y + SO * np.cos(np.radians(heading - SA))
        
        # get coords of left sensor on (x,y,0) plain
        lcoord = space_to_face()
        lcoord.x = lcoord.x + SO * np.sin(np.radians(heading - SA))
        lcoord.y = lcoord.y + SO * np.cos(np.radians(heading - SA))

        # get 3D coord of sensors
        rsens = face_to_space(Points(rcoord.x, rcoord.y, 0))
        сsens = face_to_space(Points(сcoord.x, сcoord.y, 0))
        lsens = face_to_space(Points(lcoord.x, lcoord.y, 0))
        
        return TrailMap[lsens.x, lsens.y, lsens.z], \
               TrailMap[csens.x, csens.y, csens.z], \
               TrailMap[rsens.x, rsens.y, rsens.z]
        
    
    
    
'''triangle = Polyhedron(verteces = [[0, 0, 1], [0, 1, 1], [1, 0, 2]], faces = [0, 1, 2])
surface = [0, 1, 2]
tanya = Point(1/3, 1/3, 4/3)
part = Particle(0, 0, 1, surface, triangle)
print(part.space_to_face(tanya).x, part.space_to_face(tanya).y, part.space_to_face(tanya).z)'''