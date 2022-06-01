import pygame

class Fps :
    def __init__(self,refreshTime):
        self.fpsList=[]
        self.refreshTime=refreshTime
        self.time=0
        self.fps=60
        self.hide=False


    def entry(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.hide= not self.hide

    def update(self, screen, dt):
        self.time+=dt
        if self.time<self.refreshTime:
            self.fpsList.append(1/dt)
        else:
            if len(self.fpsList)>0:
                self.fps=round(sum(self.fpsList)/len(self.fpsList))
                self.time=0
                self.fpsList=[]
        self.show(screen)


    def show(self,screen):
        if not self.hide:
            font = pygame.font.Font('freesansbold.ttf', 16)

            Fps= font.render('FPS', True, (50,50,50))
            Rect = Fps.get_rect()
            Rect.center = (20, 10)
            screen.blit(Fps, Rect)

            FpsCount = font.render(str(self.fps), True, (50,50,50))
            FpsRect = FpsCount.get_rect()
            FpsRect.center = (60, 10)
            screen.blit(FpsCount, FpsRect)