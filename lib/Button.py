import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)

class Button:
    def __init__(self,rect,text,index,subMenu=True):
        self.subMenu = subMenu #What menu the button is in
        self.index = index # the id of the button
        self.rect = list(rect) #size of button
        border = 5 #border size
        self.rect[0] , self.rect[1] , self.rect[2] , self.rect[3] = self.rect[0] - border , self.rect[1] - border , self.rect[2] + 2*border , self.rect[3] + 2*border #do maths to calculate border
        self.font = pygame.font.Font('Marons-Regular.ttf', 35) #get the font
        self.pos=(rect[0],rect[1]) #pos to display
        self.text = text #set text
        self.displayText = self.font.render(text, True, WHITE) # pygame render stuff
        self.pointerIn = False
    def pointInBtn(self,point):
        if self.rect[0] <= point[0] <= self.rect[0]+self.rect[2] and self.rect[1] <= point[1] <=self.rect[1]+self.rect[3]: # is mouse cursor in the button
            return True #return true if in
        else:
            return False #false if not
    def draw(self,scr): #draw the obj
        pygame.draw.rect(scr,BLACK,self.rect) #backdrop
        scr.blit(self.displayText,self.pos) #text
        if self.pointerIn == True: #if mouse over
            pygame.draw.rect(scr,WHITE,self.rect,2) #draw border
