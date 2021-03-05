import pygame
BLACK = (0,0,0)
WHITE = (255,255,255)
class TextInput:
    def __init__(self,x1,y1,textlist):
        textlist = []
        self.pos = (x1,y1)
        self.textlist = textlist
        self.text = "".join(self.textlist) #Stack that will display text
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.displayText = self.font.render(self.text, True, WHITE)
    def update(self,textlist):
        self.textlist = textlist
        self.text = "".join(self.textlist)
        self.displayText = self.font.render(self.text, True, WHITE)
    def draw(self,scr):
        scr.blit(self.displayText,self.pos)
