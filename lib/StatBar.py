import pygame
BLACK = (0,0,0)
WHITE = (255,255,255)
class StatBar:
    def __init__(self,Ply):
        self.CurrPlayer = Ply #Player who is currently playing
        self.PhaseDict = {1:"Attack",2:"Deploy",3:"Movement"}
        self.font = pygame.font.Font('Marons-Regular.ttf', 40)
        self.update()
    def ChangePly(self,Ply):
        self.CurrPlayer = Ply
        self.update()
    def update(self):

        curString = "Current player :" + str(self.CurrPlayer.name)

        avaString = "\tUnits :" + str(self.CurrPlayer.availableUnits)

        phaString = "\tPhase :" + self.PhaseDict[self.CurrPlayer.Phase]
        self.StatBarText = curString + avaString +phaString
    def draw(self,scr):
        self.StatLabel = self.font.render(self.StatBarText, True, WHITE)
        scr.blit(self.StatLabel,(0,0))
