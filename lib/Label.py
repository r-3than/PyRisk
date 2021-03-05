import pygame
WHITE = (255,255,255)
class Label: #simple label obj just displays text in the menus
    def __init__(self,x1,y1,text):
        self.pos = (x1,y1)
        self.text = text
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.displayText = self.font.render(self.text, True, WHITE)
    def draw(self,scr):
        scr.blit(self.displayText,self.pos)
    def changeText(self,text):
        self.text = text
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.displayText = self.font.render(self.text, True, WHITE)
