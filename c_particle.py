#class Particle():
    def __init__(self, x, y, z, heading = random.randint(0, 360)):
        """Constructor"""
        self.SA = 45
        self.RA = 20
        self.SO = 9
        self.SS = 0.5
        self.depT = 5
        self.pCD = 0
        self.sMin = 0
        self.food = 255
        self.foodTrH = 20
        self.x = x
        self.y = y
        self.z = z
        self.heading = heading
        
if __name__ == "__main__":
