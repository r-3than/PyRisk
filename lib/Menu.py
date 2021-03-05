import pygame
from lib.Button import Button
from lib.Client import Client
from lib.InfoBar import InfoBar
from lib.Label import Label
from lib.Region import Region
from lib.StatBar import StatBar
from lib.TextInput import TextInput
from lib.Unit import Unit
from lib.ghostTextManager import ghostTextManager
from lib.Player import Player
BLACK = (0,0,0)
WHITE = (255,255,255)

class Menu:
    def __init__(self,spacing=25,offset=(100,25)):
        self.display = True
        self.spacing = spacing
        self.offset = offset
        self.Buttons = []
        self.items = []
        self.CurrentMenuIndex = 0
        self.SubMenus = [self] #going to use a tree data structure in main program we add menus to this and code within each menu support this
        self.CurrentMenu = self
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
    def addBtnManual(self,btn):
        self.Buttons.append(btn)
    def addItem(self,item):
        self.items.append(item)
    def addBtn(self,x1,y1,text,index): #autoplace button with alignment
        displayText = self.font.render(text, True, WHITE)
        aRect = displayText.get_rect()
        if len(self.Buttons) == 0:
            print("Called!")
            newRect = (100,aRect[1]+self.offset[1],aRect[2],aRect[3])
            aButton = Button(newRect,text,index)
            self.Buttons.append(aButton)
        else:
            lastButton = self.Buttons[len(self.Buttons)-1]
            lastRect = lastButton.rect
            newrect = (100,lastRect[1]+lastRect[3]+self.spacing,aRect[2],aRect[3])
            x1,y1,x2,y2 = newrect
            newButton = Button(newrect,text,index)
            self.Buttons.append(newButton)
    def back(self): # goes back to the main menu
        self.CurrentMenuIndex= 0 #save where it is in the tree
        self.CurrentMenu = self
    def draw(self,scr):
        currentDrawing = self.CurrentMenu 
        #print(currentDrawing)
        if self.display: # draws all item in the menu
            for btn in currentDrawing.Buttons:
                btn.draw(scr)
            for item in currentDrawing.items:
                item.draw(scr)
    def clickPointer(self,point):
        for btn in self.CurrentMenu.Buttons:
            if btn.pointInBtn(point) == True:
                if btn.subMenu == True:
                    self.CurrentMenuIndex= btn.index + 1 # finds the menu index
                    self.CurrentMenu = self.SubMenus[self.CurrentMenuIndex] #uses the tree thing
                return (btn.index,btn.text) # return btn.index and text so we know what to do
    def parsePointer(self,point): #parses pointer so the buttons know when click / hovered over
        point = [point[0],point[1]]
        if self.display:
            for btn in self.CurrentMenu.Buttons:
                if btn.pointInBtn(point) == True:
                    btn.pointerIn = True
                else:
                    btn.pointerIn = False
