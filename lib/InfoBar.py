import pygame
import pygame.font

WHITE = (255,255,255)
class InfoBar:
    def __init__(self,players):
        self.boxSize = 10
        self.players = players
        self.font = pygame.font.Font('Marons-Regular.ttf', 25)
        self.createLabs()
    def createLabs(self):
        self.Labs = []
        for x in range(0,len(self.players)):
            newString = self.players[x].name+":"
            lab = self.font.render(newString,True,WHITE)
            x1,y1,x2,y2=lab.get_rect()
            pos1 = ((x*25)+50)
            pos2 = ((x2+10)//13)*13
            pos3 = (x*25)+60
            aLabel = PlayerLabel(pos1,pos2,pos3,lab,self.players[x].colour)
            self.Labs.append(aLabel)
    def draw(self,scr):
        for lab in self.Labs:
            lab.draw(scr)

class PlayerLabel:
    def __init__(self,pos1,pos2,pos3,text,colour):
       self.pos1 = pos1
       self.pos2 = pos2
       self.pos3 = pos3
       self.lab = text
       self.colour = colour
       self.boxSize = 10

    def draw(self,scr):
        scr.blit(self.lab,(0,self.pos1))
        pygame.draw.rect(scr,self.colour,(self.pos2,self.pos3,self.boxSize,self.boxSize))