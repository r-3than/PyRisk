import pygame
from lib.Unit import Unit

BLACK = (0,0,0)
WHITE = (255,255,255)

class Region:
    def __init__(self,index,name,worth,provId,points,connections):
        self.index = index
        self.name = name
        self.worth = worth
        self.provId = provId
        self.points = points
        self.connections  = connections
        self.highl = False
        self.VisCenter = findVisualCenter(self.points)
        self.Units = Unit(1,self.VisCenter)
        self.colour = (0,200,0)
        self.ownedby = None
    def loseUnit(self,atckReg):
        self.Units.changeUnits(-1)
        if self.Units.amt <= 0:
            for x in range(0,len(self.ownedby.ownedLand)):
                reg = self.ownedby.ownedLand
                if reg[x].index ==self.index:
                    reg.pop(x)
                    break


            self.SetOwner(atckReg.ownedby)
            atckReg.ownedby.addLand(self)
            self.Units.changeUnits(1)
            atckReg.Units.changeUnits(-1)
            temp = self.Units.amt
            self.Units.amt = atckReg.Units.amt
            atckReg.Units.amt = temp
    def highlight(self):
        self.highl = not self.highl
    def setUnit(self,amt):
        self.Units.amt = amt
    def SetOwner(self,Player):
        self.ownedby = Player
        self.colour = Player.colour
    def draw(self,scr):
        pygame.draw.polygon(scr,self.colour,self.points)
        self.Units.draw(scr)
        if self.highl == True:
            pygame.draw.polygon(scr,WHITE,self.points,3)

def isAdj(reg1,reg2):
    i = reg1.index
    found = False
    for conn in reg2.connections:
        if i == conn:
            found = True
    return found


def findVisualCenter(points):
    x_total = 0
    y_total = 0
    for point in points:
        x_total = x_total + point[0]
        y_total = y_total + point[1]
    x_mean = int(round(x_total / len(points),0))
    y_mean = int(round(y_total / len(points),0))
    return (x_mean,y_mean)
