from numpy import array,concatenate
from math import sqrt, sin
from Quad import Quad,Wall
from time import perf_counter
import pygame


class Grid:
    def __init__(self, center, size, frequency,  perspective, color = (255,0,0)):
        self.size = array(size)
        self.frequency = array(frequency)
        self.center = array(center)
        self.color = color

        self.player = [0, 0]
        self.highlight = (255,255,255)

        self.slot_size = self.size / self.frequency

        def f(x, y, t):
            dx = (x - self.center[0])/self.slot_size[0]
            dy = (y - self.center[1])/self.slot_size[1]

            return 64*sin(-0.5*sqrt(dx*dx + dy*dy) + 2*t)
        self.function = f

        self.start = perf_counter()

        D_frequency = concatenate((self.frequency, (0,)))
        D_slot_size = concatenate((self.slot_size, (0,)))


        self.tiles = [[Quad(((-D_frequency/2 + [i,j,0]) * D_slot_size + self.center), self.slot_size, self.color, perspective) for i in range(self.frequency[0])] for j in range(self.frequency[1])]
        
        self.walls = []
        for r,row in enumerate(self.tiles):
            for c,tile in enumerate(row):
                if r + 1 < self.frequency[0]:
                    tile.walls.append(Wall(quad1 = self.tiles[r+1][c], quad2 = self.tiles[r][c]))
                """if row + 1 < self.frequency[0]:
                    self.walls.append(Wall(quad1=self.tiles[row][c], quad2=self.tiles[row + 1][c]))"""
                if c + 1 < self.frequency[1]:
                    tile.walls.append(Wall(quad1 = self.tiles[r][c], quad2 = self.tiles[r][c+1]))
                """if c + 1 < self.frequency[0]:
                    self.walls.append(Wall(quad1=self.tiles[row][c], quad2=self.tiles[row][c+1]))"""




    def render(self, screen):
        for r,row  in enumerate(self.tiles):
            for c,quad in enumerate(row):

                for wall in quad.walls:
                    wall.render(screen)

                if self.player == [r,c]:
                    quad.render(screen,color = self.highlight)

                else:
                    quad.render(screen)
                

    def map(self):
        for row in self.tiles:
            for quad in row:
                quad.center[2] = self.function(quad.center[0], quad.center[1], perf_counter() - self.start)
                quad.update()

        for row in self.tiles:
            for quad in row:
                for wall in quad.walls:
                    wall.update()



    def entry(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.player[1] = self.player[1] + 1
                #self.player[0] = self.player[0] - 1
            if event.key == pygame.K_LEFT:
                self.player[1] = self.player[1] - 1
                #self.player[0] = self.player[0] + 1
            if event.key == pygame.K_DOWN:
                self.player[0] = self.player[0] + 1
            if event.key == pygame.K_UP:
                self.player[0] = self.player[0] - 1

            self.player[0] = max(0, min(self.frequency[0]-1, self.player[0]))
            self.player[1] = max(0, min(self.frequency[1]-1, self.player[1]))

    def update(self, screen):
        self.map()
        self.render(screen)
