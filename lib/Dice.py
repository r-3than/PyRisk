import pygame

def one(bSize):
    return [Pip(bSize//2,bSize//2)]

def two(bSize):
    return [Pip(bSize//6,bSize//6),Pip(bSize*5//6,bSize*5//6)]

def three(bSize):
    return [Pip(bSize//6,bSize//6),Pip(bSize*5//6,bSize*5//6),Pip(bSize//2,bSize//2)]

def four(bSize):
    return [Pip(bSize//6,bSize//6),Pip(bSize*5//6,bSize*5//6),Pip(bSize*5//6,bSize//6),Pip(bSize//6,bSize*5//6)]

def five(bSize):
    return [Pip(bSize//6,bSize//6),Pip(bSize*5//6,bSize*5//6),Pip(bSize*5//6,bSize//6),Pip(bSize//6,bSize*5//6),Pip(bSize//2,bSize//2)]

def six(bSize):
     return [Pip(bSize//6,bSize//6),Pip(bSize*5//6,bSize*5//6),Pip(bSize*5//6,bSize//6),Pip(bSize//6,bSize*5//6),Pip(bSize*5//6,bSize*3//6),Pip(bSize//6,bSize*3//6)]
switcher = {1:one,2:two,3:three,4:four,5:five,6:six}
RED = (200,10,10)
BLUE = (10,10,200)
class DiceHandler:
    def __init__(self,atkVals,defVals,r1,r2): #r's are is region 
        self.atkVals = atkVals #Lists of the dice throws ( already sorted)
        self.defVals = defVals
        diff = 30
        self.Die = []
        startpoint = ((r1.VisCenter[0]+r2.VisCenter[0])//2,(r1.VisCenter[1]+r2.VisCenter[1])//2)
        for x in range(0,len(self.atkVals)):
            aDice = Dice(self.atkVals[x],startpoint[0]+x*diff,startpoint[1],RED)
            self.Die.append(aDice)
        for x in range(0,len(self.defVals)):
            aDice = Dice(self.defVals[x],startpoint[0]+x*diff,startpoint[1]+diff,BLUE)
            self.Die.append(aDice)
    def draw(self,scr):
        for dice in self.Die:
            dice.draw(scr)

class Dice:
    def __init__(self,value,x1,y1,colour,boxSize=25):
        self.value = value
        self.boxSize = boxSize
        self.colour = colour
        self.rect = (x1,y1,boxSize,boxSize)
        self.Pips = switcher[value](boxSize)
    def draw(self,scr):
        pygame.draw.rect(scr,self.colour,self.rect)
        for p in self.Pips:
            p.draw(scr,self.rect[0],self.rect[1])
        

class Pip:
    def __init__(self,rx1,ry1):
        self.rx1 = rx1
        self.ry1 = ry1
        self.colour = (255,255,255)
        self.rad = 3
    def draw(self,scr,x,y):
        pygame.draw.circle(scr,self.colour,(x+self.rx1,y+self.ry1),self.rad)
    
