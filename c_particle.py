from additional import *
from time import sleep
import random, math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
    
class Polyhedron():
    def __init__(self, verteces, faces):
        self.verteces = verteces
        self.faces = faces

class Particle():   
    def __init__(self, x, y, z, surface, polyhedron):
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
        self.SO = 2
        self.SS = 2
        self.depT = 5
        self.food = 255
        self.foodTrH = 20
        self.coord = np.array([x, y, z])
        self.surface = surface
        self.polyhedron = polyhedron
        self.trail = np.zeros((5, 2))
        self.trans_matrix = np.array(transmission_matrix(surface, polyhedron))
        vert = np.asarray(polyhedron.verteces[surface[0]])
        self.csens = self.coord + (vert - self.coord)/get_distance(vert, self.coord)*self.SO
        
    
    def count_step_size(self):
        self.SS = 1
        
    def space_to_face(self, p):
        """
        returns coordinates of P relative to self.coord in self.surface
        """
        delta_p = p - self.coord
        return self.trans_matrix @ delta_p

    def face_to_space(self, p):
        """
        returns coordinates of P relative to base space
        """
        C = np.linalg.inv(self.trans_matrix)
        return C @ p + self.coord
    
    def rotate_point_angle(self, n, p, angle):
        """
        rotates point p (vector from point A) relative to point A on angle
        param n:
        param p:
        param angle:
        """
        return (1 - np.cos(np.radians(angle)))*np.dot(n, p)*n + \
                      np.cos(np.radians(angle))*p + \
                      np.sin(np.radians(angle))*np.cross(n, p) + self.coord
                      
    
    def init_sensors_from_center(self):
        """
        Initializing lsens and rsens after full init using csens
        """
        n = np.cross(self.polyhedron.verteces[surface[1]] - self.polyhedron.verteces[surface[0]], \
                     self.polyhedron.verteces[surface[2]] - self.polyhedron.verteces[surface[0]])
        n = n/get_distance(n, np.zeros((1, 3)))         
        p = self.csens - self.coord
        self.lsens = self.rotate_point_angle(n, p, self.SA)
        self.rsens = self.rotate_point_angle(n, p, -self.SA)
                      
        if np.dot(n, np.cross(self.rsens, self.lsens)) > 0:
            self.lsens, self.rsens = self.rsens, self.lsens
                      
    
    def sense_trail(self, TrailMap, FoodMap):
        """
        get TrailMap and FoodMap
        return Trail and Food on the rigth and left sensors
        """        
        return np.array([[TrailMap[round(self.lsens[0]), round(self.lsens[1]), round(self.lsens[2])], \
               TrailMap[round(self.csens[0]), round(self.csens[1]), round(self.csens[2])], \
               TrailMap[round(self.rsens[0]), round(self.rsens[1]), round(self.rsens[2])]], 
               [FoodMap[round(self.lsens[0]), round(self.lsens[1]), round(self.lsens[2])], \
               FoodMap[round(self.csens[0]), round(self.csens[1]), round(self.csens[2])], \
               FoodMap[round(self.rsens[0]), round(self.rsens[1]), round(self.rsens[2])]]])
               
    def rotate_all_sensors(self, sense):
        heading = 0
        #turn according to food
        if sense[0, 1] > 0 or sense[2, 1] > 0:
            if sense[0, 1] > sense[2, 1]:
                # turn left
                heading += 5
            else:
                # turn right
                heading -= 5

        rand = random.randint(0, 15)
        if rand == 1:
            # turn randomly
            r = random.randint(0, 1)
            if r == 0:
                heading += self.RA
            else:
                heading -= self.RA
        else:
            if sense[1, 0] >= sense[0, 0] and sense[1, 0] >= sense[2, 0]:
                pass
            elif sense[1, 0] < sense[0, 0] and sense[1, 0] < sense[2, 0]:
                # turn randomly
                r = random.randint(0, 1)
                if r == 0:
                    heading += self.RA
                else:
                    heading -= self.RA
            elif sense[0, 0] >= sense[1, 0] and sense[0, 0] >= sense[2, 0]:
                # turn left
                heading += self.RA
            elif sense[2, 0] >= sense[1][0] and sense[2, 0] >= sense[0, 0]:
                # turn right
                heading -= self.RA
                
        n = np.cross(self.lsens - self.coord, self.rsens - self.coord)
        n = n/get_distance(n, np.zeros((1, 3)))         
        p = self.lsens - self.coord
        self.lsens = self.rotate_point_angle(n, p, heading)
        p = self.csens - self.coord
        self.csens = self.rotate_point_angle(n, p, heading)
        p = self.rsens - self.coord
        self.rsens = self.rotate_point_angle(n, p, heading)
               
    def move_all_agent_coordinates(self):
        """
        change all agent coordinates(coord, csens, lsens, rsens)
        """
        vector_move = (self.csens - self.coord) / self.SO * self.SS
        self.coord += vector_move
        self.csens += vector_move
        self.lsens += vector_move
        self.rsens += vector_move
        
    def simple_visualizing(self, ax):
        ax.scatter3D(xs=part.coord[0], ys=part.coord[1], zs=part.coord[2], color = 'black')
        ax.scatter3D(xs=part.csens[0], ys=part.csens[1], zs=part.csens[2], color = 'black')
        ax.scatter3D(xs=part.lsens[0], ys=part.lsens[1], zs=part.lsens[2], color = 'red')
        ax.scatter3D(xs=part.rsens[0], ys=part.rsens[1], zs=part.rsens[2], color = 'green')
        ax.plot3D([part.coord[0], part.csens[0]], [part.coord[1], part.csens[1]], [part.coord[2], part.csens[2]], color = 'black')
        ax.plot3D([part.coord[0], part.lsens[0]], [part.coord[1], part.lsens[1]], [part.coord[2], part.lsens[2]], color = 'red')
        ax.plot3D([part.coord[0], part.rsens[0]], [part.coord[1], part.rsens[1]], [part.coord[2], part.rsens[2]], color = 'green')
        self.move_all_agent_coordinates()
        #sleep(0.1)
       
    

    
if __name__ == "__main__":
    TrailMap = np.zeros((100, 100, 100))
    FoodMap = np.zeros((100, 100, 100))
    triangle = Polyhedron(verteces = np.array([[0, 0, 0], [0, 2., 0], [2., 0, 0]]), faces = [0, 1, 2])
    surface = [0, 1, 2]
    part = Particle(1.0, 1.0, 0, surface, triangle)
    part.init_sensors_from_center()
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    for i in range(0, 5):
        part.simple_visualizing(ax)
        part.rotate_all_sensors(part.sense_trail(TrailMap, FoodMap))
    plt.show()
