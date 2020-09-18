import pygame
switcher = {1:one,2:two,3:three,4:four,5:five,6:six}
class Dice:
    def __init__(self,value,x1,y1,colour,boxSize=25):
        self.value = value
        self.boxSize = boxSize
        self.colour = colour
        self.rect = (x1,y1,boxSize,boxSize)
        self.Pips = switcher[value]()
    def draw(self,scr):
        pygame.draw.rect(scr,self.colour,self.rect)
        for p in self.Pips:
            p.draw(scr,self.rect[0],self.rect[1])
        

class Pip:
    def __init__(self,rx1,ry1):
        self.rx1 = rx1
        self.ry1 = ry1
        self.colour = (255,255,255)
        self.rad = 5
    def draw(self,scr,x,y):
        pygame.draw.circle(scr,self.colour,(x+self.rx1,y+self.ry1),self.rad)
    
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