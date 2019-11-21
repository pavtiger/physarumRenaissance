from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, translate, rotate

import random
import numpy as np
import time
import math
#from PIL import Image
import matplotlib.pyplot as plt

START_POINT = [[0, 0, 0]]
QUALITY = 'LOW'

if QUALITY == 'LOW':
    TRAIL = False
    LENGH = 5
elif QUALITY == 'HIGH':
    TRAIL = False
    LENGH = 20

SENSORS = False
FOOD_EAT = 40
FOOD = True
SIZE = (600, 600)
CL = (33, 33, 33)
ANGLE = 360
K = 0


class Modeling():
    def __init__(self, trsCount=1):
        self.trsCount = trsCount
        for item in START_POINT:
            self.arrOrganism = [Particle(item[0], item[1], item[2]) for i in range(trsCount)]

    def locationUpdate(self, Count):
        delete = []
        for a in range(len(self.arrOrganism)):
            #####
            elem = self.arrOrganism[a]
            elem.move()
            elem.share()
            ans = elem.sence()
            elem.rotate(ans)
            if elem.food >= 0:
                elem.food -= 0
            else:
                delete.append(a)
            #####
            # pygame.display.set_caption(f'{str(int(ans[0][1]))} - {str(int(ans[1][1]))} - {str(int(ans[2][1]))}')
            if elem.x >= 0 and elem.x <= SIZE[0] and elem.y >= 0 and elem.y <= SIZE[1]:
                TrailMap[int(elem.y), int(elem.x)] += 255
                if FoodMap[int(elem.y), int(elem.x)] <= 10:
                    FoodMap[int(elem.y), int(elem.x)] = 0
            else:
                delete.append(a)

        for ind in range(len(delete)):
            del model.arrOrganism[delete[ind]]
            Count -= 1
            for i in range(len(delete)):
                delete[i] -= 1



vert = """
#version 120
// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_linewidth;
uniform float u_antialias;
uniform float u_size;
// Attributes
// ------------------------------------
attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_size;
// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
void main (void) {
    v_size = a_size * u_size;
    v_linewidth = u_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    gl_PointSize = v_size + 2.*(v_linewidth + 1.5*v_antialias);
}
"""

frag = """
#version 120
// Constants
// ------------------------------------
// Varyings
// ------------------------------------
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;
// Functions
// ------------------------------------
// ----------------
float disc(vec2 P, float size) {
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2.;
    return r;
}
// ----------------
float arrow_right(vec2 P, float size) {
    float r1 = abs(P.x -.50)*size + abs(P.y -.5)*size - v_size/2.;
    float r2 = abs(P.x -.25)*size + abs(P.y -.5)*size - v_size/2.;
    float r = max(r1,-r2);
    return r;
}
// ----------------
float ring(vec2 P, float size) {
    float r1 = length((P.xy - vec2(0.5,0.5))*size) - v_size/2.;
    float r2 = length((P.xy - vec2(0.5,0.5))*size) - v_size/4.;
    float r = max(r1,-r2);
    return r;
}
// ----------------
float clober(vec2 P, float size) {
    const float PI = 3.14159265358979323846264;
    const float t1 = -PI/2.;
    const vec2  c1 = 0.2*vec2(cos(t1),sin(t1));
    const float t2 = t1+2.*PI/3.;
    const vec2  c2 = 0.2*vec2(cos(t2),sin(t2));
    const float t3 = t2+2.*PI/3.;
    const vec2  c3 = 0.2*vec2(cos(t3),sin(t3));
    float r1 = length((P.xy- vec2(0.5,0.5) - c1)*size);
    r1 -= v_size/3;
    float r2 = length((P.xy- vec2(0.5,0.5) - c2)*size);
    r2 -= v_size/3;
    float r3 = length((P.xy- vec2(0.5,0.5) - c3)*size);
    r3 -= v_size/3;
    float r = min(min(r1,r2),r3);
    return r;
}
// ----------------
float square(vec2 P, float size) {
    float r = max(abs(P.x -.5)*size,
                  abs(P.y -.5)*size);
    r -= v_size/2.;
    return r;
}
// ----------------
float diamond(vec2 P, float size) {
    float r = abs(P.x -.5)*size + abs(P.y -.5)*size;
    r -= v_size/2.;
    return r;
}
// ----------------
float vbar(vec2 P, float size) {
    float r1 = max(abs(P.x -.75)*size,
                   abs(P.x -.25)*size);
    float r3 = max(abs(P.x -.5)*size,
                   abs(P.y -.5)*size);
    float r = max(r1,r3);
    r -= v_size/2.;
    return r;
}
// ----------------
float hbar(vec2 P, float size) {
    float r2 = max(abs(P.y -.75)*size,
                   abs(P.y -.25)*size);
    float r3 = max(abs(P.x -.5)*size,
                   abs(P.y -.5)*size);
    float r = max(r2,r3);
    r -= v_size/2.;
    return r;
}
// ----------------
float cross(vec2 P, float size) {
    float r1 = max(abs(P.x -.75)*size,
                   abs(P.x -.25)*size);
    float r2 = max(abs(P.y -.75)*size,
                   abs(P.y -.25)*size);
    float r3 = max(abs(P.x -.5)*size,
                   abs(P.y -.5)*size);
    float r = max(min(r1,r2),r3);
    r -= v_size/2.;
    return r;
}
// Main
// ------------------------------------
void main() {
    float size = v_size +2.0*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;
    float r = disc(gl_PointCoord, size);
    // float r = square(gl_PointCoord, size);
    // float r = ring(gl_PointCoord, size);
    // float r = arrow_right(gl_PointCoord, size);
    // float r = diamond(gl_PointCoord, size);
    // float r = cross(gl_PointCoord, size);
    // float r = clober(gl_PointCoord, size);
    // float r = hbar(gl_PointCoord, size);
    // float r = vbar(gl_PointCoord, size);
    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias)) {
        discard;
    }
    else if( d < 0.0 ) {
       gl_FragColor = v_fg_color;
    } else {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0.)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}
"""



class Canvas(app.Canvas):

    def __init__(self):
        app.Canvas.__init__(self, keys='interactive', title='test', size=(800, 600))
        ps = self.pixel_scale
        ar = []
        for elem in model.arrOrganism:
            ar.append([elem.x, elem.y, 0])

        # Create vertices
        #n = 1000
        '''self.data = np.zeros(n, [('a_position', np.float32, 3),
                            ('a_bg_color', np.float32, 4),
                            ('a_fg_color', np.float32, 4),
                            ('a_size', np.float32)])'''
        #data['a_position'] = elem[]
        '''self.data['a_bg_color'] = np.random.uniform(0.85, 1.00, (n, 4))
        data['a_fg_color'] = 0, 0, 0, 1
        data['a_size'] = np.random.uniform(5*ps, 10*ps, n)
        u_linewidth = 1.0
        u_antialias = 1.0'''

        self.translate = 5
        self.program = gloo.Program(vert, frag)
        self.program['a_position'] = ar
        self.view = translate((0, 0, -self.translate))
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)

        self.apply_zoom()
        self.theta = 0
        self.phi = 0

        gloo.set_state('translucent', clear_color='white')

        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.show()

    def drawOutput(self):
        ar = []
        print(len(model.arrOrganism))
        for elem in model.arrOrganism:
            ar.append([elem.x, elem.y, 0])
        #data['a_position'] = ar
        self.program['a_position'] = ar
        print(ar)


    def on_key_press(self, event):
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()

    def on_timer(self, event):
        self.theta += .5
        self.phi += .5
        self.model = np.dot(rotate(self.theta, (0, 0, 1)),
                            rotate(self.phi, (0, 1, 0)))
        self.program['u_model'] = self.model
        self.update()

    def on_resize(self, event):
        self.apply_zoom()

    def on_mouse_wheel(self, event):
        self.translate -= event.delta[1]
        self.translate = max(2, self.translate)
        self.view = translate((0, 0, -self.translate))

        self.program['u_view'] = self.view
        self.program['u_size'] = 5 / self.translate
        self.update()

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('points')

    def apply_zoom(self):
        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
        self.projection = perspective(45.0, self.size[0] /
                                      float(self.size[1]), 1.0, 1000.0)
        self.program['u_projection'] = self.projection



class Particle():
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

    def share(self):
        for elem in model.arrOrganism:
            if elem.x != self.x or elem.y != self.y:
                if self.food > elem.food:
                    dx = math.fabs(elem.x - self.x)
                    dy = math.fabs(elem.y - self.y)
                    if QUALITY == 'LOW': n = 3
                    elif QUALITY == 'HIGH': n = 6
                    if math.sqrt(dx*dx + dy*dy) <= n:
                        if elem.food <= 255 - FOOD_EAT and self.food > FOOD_EAT:
                            elem.food += FOOD_EAT
                            self.food -= FOOD_EAT

    def test(self, y, x, var):
        var = [FoodMap[y, x], 20] [FoodMap[y, x] > 20]
        FoodMap[y, x] -= var # Transaction

    def move(self):
        var = [FoodMap[int(self.y), int(self.x)], 20] [FoodMap[int(self.y), int(self.x)] > 20]
        if self.food <= 255 - 20:
            self.food += var # Transaction
        self.test(int(self.y), int(self.x), var)
        self.test(int(self.y+1), int(self.x), var)
        self.test(int(self.y-1), int(self.x), var)
        self.test(int(self.y), int(self.x+1), var)
        self.test(int(self.y), int(self.x-1), var)
        dx = math.sin(math.radians(self.heading)) * (self.SS + FoodMap[int(self.y), int(self.x)]/255 * K)
        dy = math.cos(math.radians(self.heading)) * (self.SS + FoodMap[int(self.y), int(self.x)]/255 * K)
        if Skip == False and FoodMap[int(self.y + dy), int(self.x + dx)] >= 0:
            self.x += dx
            self.y += dy

    def rotate(self, ans):
        if ans[0][1] > 0 or ans[2][1] > 0:
            if ans[0][1] > ans[2][1]:
                # turn left
                self.heading += 5
            else:
                # turn right
                self.heading -= 5

        rand = random.randint(0, 15)
        if rand == 1:
            # turn randomly
            r = random.randint(0, 1)
            if r == 0:
                self.heading += self.RA
            else:
                self.heading -= self.RA
        else:
            if ans[1][0] >= ans[0][0] and ans[1][0] >= ans[2][0]:
                pass
            elif ans[1][0] < ans[0][0] and ans[1][0] < ans[2][0]:
                # turn randomly
                r = random.randint(0, 1)
                if r == 0:
                    self.heading += self.RA
                else:
                    self.heading -= self.RA
            elif ans[0][0] >= ans[1][0] and ans[0][0] >= ans[2][0]:
                # turn left
                self.heading += self.RA
            elif ans[2][0] >= ans[1][0] and ans[2][0] >= ans[0][0]:
                # turn right
                self.heading -= self.RA


    def sence(self):
        """LEFT"""
        dx1 = int(math.sin(math.radians(self.heading + self.SA)) * self.SO)
        dy1 = int(math.cos(math.radians(self.heading + self.SA)) * self.SO)
        if SENSORS:
            # pygame.draw.circle(screen, (0, 0, 0), (int(self.x + dx1), int(self.y + dy1)), 0, 0)
            pass
        """SENTER"""
        dx2 = int(math.sin(math.radians(self.heading)) * self.SO)
        dy2 = int(math.cos(math.radians(self.heading)) * self.SO)
        if SENSORS:
            # pygame.draw.circle(screen, (0, 0, 0), (int(self.x + dx2), int(self.y + dy2)), 0, 0)
            pass
        """RIGHT"""
        dx3 = int(math.sin(math.radians(self.heading - self.SA)) * self.SO)
        dy3 = int(math.cos(math.radians(self.heading - self.SA)) * self.SO)
        if SENSORS:
            # pygame.draw.circle(screen, (0, 0, 0), (int(self.x + dx3), int(self.y + dy3)), 0, 0)
            pass
        try:
            element0 = [TrailMap[int(self.y + dy1), int(self.x + dx1)], FoodMap[int(self.y + dy1), int(self.x + dx1)]]
            element1 = [TrailMap[int(self.y + dy2), int(self.x + dx2)], FoodMap[int(self.y + dy2), int(self.x + dx2)]]
            element2 = [TrailMap[int(self.y + dy3), int(self.x + dx3)], FoodMap[int(self.y + dy3), int(self.x + dx3)]]
            return [element0, element1, element2]
        except:
            return [0, 0, 0]



if __name__ == "__main__":
    model = Modeling(1)
    c = Canvas()
    app.run()

    N = 0
    Skip = False
    TrailMap = np.zeros((SIZE[1], SIZE[0]))
    FoodMap = np.zeros((SIZE[1], SIZE[0]))
    Count = 1

    '''def makeCircle(p, type, s = 20):
        for i in range(s):
            for angl in range(360):
                dx = math.sin(math.radians(angl)) * i
                dy = math.cos(math.radians(angl)) * i
                if type == 'FOOD':
                    FoodMap[int(p[1] + dy), int(p[0] + dx)] = 255 - (i * 255/s)
                else:
                    FoodMap[int(p[1] + dy), int(p[0] + dx)] = 255 - (9-1 * i * 255/s)'''


    done = False
    while not done:
        for y in range(TrailMap.shape[0]):
            for x in range(TrailMap.shape[1]):
                if FoodMap[y, x] > 0:
                    value = FoodMap[y, x]
                    # pygame.draw.circle(screen, (255 - value, 255, 255 - value), (x, y), 0, 0)
                elif FoodMap[y, x] < 0:
                    value = math.fabs(FoodMap[y, x])
                    # pygame.draw.circle(screen, (255-value, 255-value, 255-value), (x, y), 1, 0)

                if TrailMap[y, x] >= 8:
                    TrailMap[y, x] -= 8
                    if TRAIL:
                        value = TrailMap[y, x]
                        if value > 255:
                            value = 255
                        # pygame.draw.circle(screen, (255 - value, 255 - value, 255 - value), (x, y), 0, 0)


        model.locationUpdate(Count)
        c.drawOutput()
        #for elem in START_POINT:
        #    pygame.draw.circle(screen, (200, 0, 0), (elem[0], elem[1]), 6, 3) # Start Point


        for i in range(LENGH):
            for point in START_POINT:
                model.arrOrganism.append(Particle(x=point[0], y=point[1], z=point[2], heading=random.randint(0, ANGLE)))
                Count += 1
                print(f'--{Count}--')

        # pygame.image.save(screen, 'screens/file-' + str(N) + '.png')
        N += 1   
        pygame.display.update()
        screen.fill(CL)

    print(f'--{Count}--')
    pygame.quit()
