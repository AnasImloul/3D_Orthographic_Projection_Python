import pygame


class Control:
    def __init__(self,*objects):
        self.objects=objects

    def add(self,object):
        self.objects.append(object)

    def entry(self):
        global running
        events=pygame.event.get()

        for event in events:
            for object in self.objects:
                object.entry(event)
            if event.type == pygame.QUIT:
                running = False

    def update(self,dt):
        self.entry()
