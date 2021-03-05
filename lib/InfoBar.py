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
            x2=lab.get_rect()[2]
            pos1 = ((x*25)+50) #doing maths to find good position to place
            pos2 = ((x2+10)//13)*13
            pos3 = (x*25)+60
            aLabel = PlayerLabel(pos1,pos2,pos3,lab,self.players[x].colour) # create lab
            self.Labs.append(aLabel) #add label
    def draw(self,scr):
        for lab in self.Labs: # draw all labels
            lab.draw(scr)

class PlayerLabel: #player name and colour
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