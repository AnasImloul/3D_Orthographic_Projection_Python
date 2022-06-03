import pygame
from numpy import array, sqrt
from Grid import Grid
from matrix import rotMat
from time import perf_counter_ns,sleep
from FPS import Fps
from Control import Control

SIZE = 800

BG_COLOR = (255,255,255)

perspective = array([[1,0,0],[0,0.5,1]]) @ rotMat(0,0,45) / sqrt(2)

grid = Grid((0,0,0),(800,800),(16,)*2,perspective, color = (200,100,100))

pygame.init()

screen = pygame.display.set_mode((SIZE,SIZE))

fps = Fps(1)

control = Control(fps,grid)


dt = 1/60

is_closed = False
while not is_closed:
    start = perf_counter_ns()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_closed = True

    screen.fill(BG_COLOR)

    grid.update(screen)
    control.update(dt)
    fps.update(screen,dt)

    pygame.display.flip()

    dt = (perf_counter_ns() - start)/1_000_000_000
