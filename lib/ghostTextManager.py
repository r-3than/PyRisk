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
        self.now = datetime.datetime.now()
        if self.now <= self.end:
            startdiff = self.now - self.start # this is timedelta obj
            enddiff = self.dt
            #print(startdiff.total_seconds(),enddiff.total_seconds(),255-round((startdiff.total_seconds()/enddiff.total_seconds())*255,0))
            alpha = 255-(round((startdiff.total_seconds()/enddiff.total_seconds())*255,0))//10
            #print(alpha)
            surface=pygame.Surface((self.rendFont.get_rect()[2],self.rendFont.get_rect()[3]),pygame.SRCALPHA)
            surface.fill((255,255,255))
            surface.set_alpha(alpha)
            self.rendFont.blit(surface,(0,0) ,special_flags=pygame.BLEND_RGBA_MULT)


            scr.blit(self.rendFont, (self.x,self.y))

            #self.rendFont.set_alpha(alpha)
            #scr.blit(self.rendFont,(self.x,self.y))
        else:
            return True

class ghostTextManager:
    def __init__(self):
        self.index = 0
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.GhostTexts = []
    def addGhostText(self,text,x,y,length):
        self.index = self.index +1
        displayText = self.font.render(text, True, WHITE)
        newText = ghostText(displayText,x,y,length,text,self.index)
        self.GhostTexts.append(newText)
    def draw(self,scr):
        for text in self.GhostTexts:
            if text.draw(scr) == True:
                self.GhostTexts.remove(text)
