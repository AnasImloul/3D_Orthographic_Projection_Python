from numpy import array,cross,dot
from numpy.linalg import norm
from matrix import rotMat
import pygame

class Quad:
    def __init__(self, center, size, color, perspective, orientation = (0,0,0)):
        self.center = center

        self.perspective = perspective

        self.size = size
        self.border_size = int(min(self.size)//12) + 1

        self.orientation = rotMat(orientation[0], orientation[1], orientation[2])


        unit_x = self.orientation@[self.size[0]/2, 0,0]
        unit_y = self.orientation@[0, self.size[1]/2,0]

        self.normal = cross(unit_x, unit_y)
        self.normal /= norm(self.normal)

        self.light = array((0, 0, 1))

        self.light = self.light / norm(self.light)

        self.brightness = (dot(self.normal, self.light) + 1) / 2

        self.color = array(color) * self.brightness


        x1, y1, z1 =  unit_x[0] + unit_y[0],  unit_x[1] + unit_y[1],  unit_x[2] + unit_y[2]
        x2, y2, z2 =  unit_x[0] - unit_y[0],  unit_x[1] - unit_y[1],  unit_x[2] - unit_y[2]
        x3, y3, z3 = -unit_x[0] - unit_y[0], -unit_x[1] - unit_y[1], -unit_x[2] - unit_y[2]
        x4, y4, z4 = -unit_x[0] + unit_y[0], -unit_x[1] + unit_y[1], -unit_x[2] + unit_y[2]


        self.p1 = (self.perspective[0][0] * x1 + self.perspective[0][1] * y1 + self.perspective[0][2] * z1,
                   self.perspective[1][0] * x1 + self.perspective[1][1] * y1 + self.perspective[1][2] * z1)

        self.p2 = (self.perspective[0][0] * x2 + self.perspective[0][1] * y2 + self.perspective[0][2] * z2,
                   self.perspective[1][0] * x2 + self.perspective[1][1] * y2 + self.perspective[1][2] * z2)

        self.p3 = (self.perspective[0][0] * x3 + self.perspective[0][1] * y3 + self.perspective[0][2] * z3,
                   self.perspective[1][0] * x3 + self.perspective[1][1] * y3 + self.perspective[1][2] * z3)

        self.p4 = (self.perspective[0][0] * x4 + self.perspective[0][1] * y4 + self.perspective[0][2] * z4,
                   self.perspective[1][0] * x4 + self.perspective[1][1] * y4 + self.perspective[1][2] * z4)

        self.walls = []

        self.update()


    def update(self):

        center = (self.perspective[0][0] * self.center[0] + self.perspective[0][1] * self.center[1] + self.perspective[0][2] * self.center[2],
                  self.perspective[1][0] * self.center[0] + self.perspective[1][1] * self.center[1] + self.perspective[1][2] * self.center[2])

        self.d_center = center

        self.rect = ((self.p1[0] + center[0], self.p1[1] + center[1]), (self.p2[0] + center[0], self.p2[1] + center[1]),
                     (self.p3[0] + center[0], self.p3[1] + center[1]), (self.p4[0] + center[0], self.p4[1] + center[1]))






    def render(self,screen, color = None):
        w, h = pygame.display.get_surface().get_size()

        rect = [(point[0] + w/2, point[1] + h/2) for point in self.rect]

        if color is None:
            color = self.color

        pygame.draw.polygon(screen, color, rect)
        pygame.draw.polygon(screen, (0,0,0), rect, width = self.border_size)



    def moveTo(self, pos):
        if isinstance(pos, (tuple, list)):
            self.center = pos
            self.update()
        else:
            raise ValueError


    def translate(self,other):
        if isinstance(other, (tuple, list)):
            self.center = self.center + other
            self.update()
        else:
            raise ValueError

    def scale(self,other):
        if isinstance(other, (int, float)):
            self.size *= other
            self.update()
        else:
            raise ValueError

    def __str__(self):
        return f"Center : {self.center}, Size : {self.size}"


class Wall:
    def __init__(self, quad1, quad2):
        self.quad1 = quad1
        self.quad2 = quad2

        self.border_size = (int(min(min(self.quad1.size), min(self.quad2.size)) // 12) + 1)

        self.color = (quad1.color + quad2.color)/2

        self.update()

        self.normal = dot(array(self.p1) - self.p3,array(self.p2) - self.p4)
        self.normal /= norm(self.normal)

        self.light = array((0, 0, 1))

        self.light = self.light / norm(self.light)

        self.brightness = (dot(self.normal, self.light) + 1) / 2


        self.color *= self.brightness


    def update(self):
        self.p1 = self.quad1.p1[0] + self.quad1.d_center[0], self.quad1.p1[1] + self.quad1.d_center[1]
        self.p2 = self.quad1.p2[0] + self.quad1.d_center[0] ,self.quad1.p2[1] + self.quad1.d_center[1]
        self.p3 = self.quad2.p3[0] + self.quad2.d_center[0] ,self.quad2.p3[1] + self.quad2.d_center[1]
        self.p4 = self.quad2.p4[0] + self.quad2.d_center[0] ,self.quad2.p4[1] + self.quad2.d_center[1]

        self.rect = (self.p1, self.p2, self.p3, self.p4)


    def render(self,screen, color = None):
        w, h = pygame.display.get_surface().get_size()

        rect = [(point[0] + w/2, point[1] + h/2) for point in self.rect]

        if color is None:
            color = self.color

        pygame.draw.polygon(screen, color, rect)
        pygame.draw.polygon(screen, (0,0,0), rect, width = self.border_size)
