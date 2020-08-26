import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)

class Button:
    def __init__(self,rect,text,index,subMenu=True):
        self.subMenu = subMenu
        self.index = index
        self.rect = list(rect)
        border = 5
        self.rect[0] , self.rect[1] , self.rect[2] , self.rect[3] = self.rect[0] - border , self.rect[1] - border , self.rect[2] + 2*border , self.rect[3] + 2*border
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.pos=(rect[0],rect[1])
        self.text = text
        self.displayText = self.font.render(text, True, WHITE)
        self.pointerIn = False
    def pointInBtn(self,point):
        if self.rect[0] <= point[0] <= self.rect[0]+self.rect[2] and self.rect[1] <= point[1] <=self.rect[1]+self.rect[3]:
            return True
        else:
            return False
    def draw(self,scr):
        pygame.draw.rect(scr,BLACK,self.rect)
        scr.blit(self.displayText,self.pos)
        if self.pointerIn == True:
            pygame.draw.rect(scr,WHITE,self.rect,2)
