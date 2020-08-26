import pygame
BLACK = (0,0,0)
WHITE = (255,255,255)
rad = 15
class Unit:
    def __init__(self,amt,pos):
        self.amt = amt
        self.pos = pos

        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.text = self.font.render(str(self.amt), True, WHITE)
        self.textpos = self.update()
        self.update()
    def update(self):

        textRect = self.text.get_rect()

        oldpos = self.pos
        newpos = (oldpos[0]-textRect[2]//2-rad//3.14,oldpos[1]-textRect[3]//2-rad//3.14) #
        # moves to the centre of the circle (minus offset)
        return newpos
    def draw(self,scr):
        pygame.draw.circle(scr,BLACK,self.pos,rad)
        self.text = self.font.render(str(self.amt), True, WHITE)
        scr.blit(self.text,self.textpos)
    def changeUnits(self,amt):
        self.amt = self.amt + amt
