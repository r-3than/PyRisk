import pygame , datetime
BLACK = (0,0,0)
WHITE = (255,255,255)

class ghostText:
    def __init__(self,rendFont,x,y,length,text,index):
        self.rendFont = rendFont
        self.x = x
        self.y = y
        self.text = text
        self.length = length
        self.index = index
        self.now = datetime.datetime.now()
        self.start = self.now
        self.dt = datetime.timedelta(seconds=length)
        self.end = self.now + datetime.timedelta(seconds=length)
    def draw(self,scr):
        self.now = datetime.datetime.now() #get current time
        if self.now <= self.end: # if its still within the value
            startdiff = self.now - self.start # this is timedelta obj
            enddiff = self.dt 
            alpha = 255-(round((startdiff.total_seconds()/enddiff.total_seconds())*255,0))//10  ## FADE amt relative from time
            surface=pygame.Surface((self.rendFont.get_rect()[2],self.rendFont.get_rect()[3]),pygame.SRCALPHA) #do pygame magic to draw alpha channel
            surface.fill((255,255,255)) #do pygame magic to draw alpha channel
            surface.set_alpha(alpha) #do pygame magic to draw alpha channel
            self.rendFont.blit(surface,(0,0) ,special_flags=pygame.BLEND_RGBA_MULT)#do pygame magic to draw alpha channel


            scr.blit(self.rendFont, (self.x,self.y)) #draw to screen

        else: #if ended return a true
            return True

class ghostTextManager:
    def __init__(self):
        self.index = 0
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.GhostTexts = []
    def addGhostText(self,text,x,y,length):
        self.index = self.index +1 #id for ghost text
        displayText = self.font.render(text, True, WHITE) #render the text
        newText = ghostText(displayText,x,y,length,text,self.index) #create obj
        self.GhostTexts.append(newText) #add to list
    def draw(self,scr):
        for text in self.GhostTexts: # loop each text obj
            if text.draw(scr) == True: #if ended 
                self.GhostTexts.remove(text) #remove the text from the drawing queue
