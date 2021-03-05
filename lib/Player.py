import pygame  , random
class Player:
    def __init__(self,name,colour,availableUnits=1,phase=2,):
        self.name = name        #define player object
        self.colour = colour
        self.availableUnits =  availableUnits
        self.ownedLand = []
        self.Phase = phase
        self.dead= False
    def amtOfLand(self):
        return len(self.ownedLand) #return amt of landed owned (used for the winning conditions)
    def eliminate(self):
        self.availableUnits =0 #also used for winning conditions
        self.dead = True
    def nextPhase(self):
        self.Phase = self.Phase + 1 #loops through phase
        if self.Phase == 4:
            self.Phase = 1
            return True #end of the 3 phases reset and turn true
        else:
            return None
    def addLand(self,Reg): #adds land to that player
        #Reg.colour = self.colour
        self.ownedLand.append(Reg) #adds it to their regions
        Reg.SetOwner(self) #sets them as the owner

    def addUnit(self,pos): #adds units to the region
        if self.availableUnits > 0: #checks if they have units 
            for reg in self.ownedLand:
                if isPointInPoly(pos,reg.points) == True: #finds region clicked
                    self.availableUnits = self.availableUnits-1
                    reg.Units.changeUnits(1) 
                    return reg
    def Transfer(self,reg1,reg2):
        if reg1.Units.amt > 1: #checks so they cannot have less than 1 unit on a region

            reg1.Units.changeUnits(-1)#moves units from one to another
            reg2.Units.changeUnits(1)

    def attack(self,atckReg,defReg,ghmanager): ##attack function 
        if atckReg.Units.amt > 1:
            if atckReg.Units.amt > 4:                   ##Do checks to find amt of dice to throw
                amountAtck = 3
            else:
                amountAtck = atckReg.Units.amt - 1
            if defReg.Units.amt > 2:
                amountDef = 2
            else:
                amountDef = defReg.Units.amt
            atckList = []
            defList = []
            for x in range(0,amountAtck):
                atckList.append(random.randint(1,6)) ##add attack dice and def dice
            for x in range(0,amountDef):
                defList.append(random.randint(1,6))##add attack dice and def dice
            print(atckList,defList)
            atckList = sorted(atckList,reverse=True) #sorted dice required in risk to calculate correct stuff
            defList = sorted(defList,reverse=True) #sorted dice required in risk to calculate correct stuff
            for x in range(0,min(len(atckList),len(defList))): ## do some maths stuff loop the least amt of dice
                var1 = random.randint(-15,15) 
                var2 = random.randint(-15,15)
                if atckList[x] > defList[x]: # if attacking wins 
                    defReg.loseUnit(atckReg) #def region loses a unit
                    ghmanager.addGhostText("-1",defReg.VisCenter[0]+var1,defReg.VisCenter[1]+var2,4) # add the ghost text visuals
                    # kill a defending unit
                else:
                    atckReg.loseUnit(defReg)
                    ghmanager.addGhostText("-1",atckReg.VisCenter[0]+var1,atckReg.VisCenter[1]+var2,4)  # add the ghost text visuals
                    #kill atckUnit
            return (atckList,defList) #return dice thrown so dice handler can draw to main screen
    def __repr__(self): # so we can print the obj
        return 'Player: {} , Colour: {} , currentPhase: {} , availableUnits: {}'.format(self.name,self.colour,self.Phase,self.availableUnits)

def isPointInPoly(point,poly): # uses the maths magic for determinding if point is in polygon from the winding number.
    if winding(point,poly) != 0:
        return True
    else:
        return False
        
def isLeft(P0,P1,P2):
    return ((P1[0]-P0[0])*(P2[1]-P0[1]) - (P2[0]-P0[0])*(P1[1]-P0[1])) #Maths magic

def winding(point,poly): #More Maths magic see here  -> https://en.wikipedia.org/wiki/Winding_number
    wn = 0
    for i in range(0,len(poly)):
        point1 = poly[i]
        point2 = poly[(i+1)%len(poly)]
        if point1[1] <= point[1]:
            if point2[1] >point[1]:
                if isLeft(point1,point2,point) >0:
                    wn = wn +1
        else:
            if point2[1] <= point[1]:
                if isLeft(point1,point2,point)<0:
                    wn = wn-1
    return wn  