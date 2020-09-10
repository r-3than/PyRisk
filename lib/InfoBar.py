import pygame
import pygame.font

WHITE = (255,255,255)
class InfoBar:
    def __init__(self,players):
        self.boxSize = 10
        self.players = players
        self.font = pygame.font.Font('Marons-Regular.ttf', 25)
    def draw(self,scr):
        for x in range(0,len(self.players)):
            newString = self.players[x].name+":"
            lab = self.font.render(newString,True,WHITE)
            x1,y1,x2,y2=lab.get_rect()
            scr.blit(lab,(0,(x*25)+50))
            XDraw = ((x2+10)//13)*13
            pygame.draw.rect(scr,self.players[x].colour,(XDraw,(x*25)+60,self.boxSize,self.boxSize))

