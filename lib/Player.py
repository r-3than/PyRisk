import pygame  , random
class Player:
    def __init__(self,name,colour,availableUnits=1,phase=2):
        self.name = name
        self.colour = colour
        self.availableUnits =  availableUnits
        self.ownedLand = []
        self.Phase = phase
    def nextPhase(self):
        self.Phase = self.Phase + 1
        if self.Phase == 4:
            self.Phase = 1
            return True
        else:
            return None
    def addLand(self,Reg):
        #Reg.colour = self.colour
        self.ownedLand.append(Reg)
        Reg.SetOwner(self)

    def addUnit(self,pos):
        if self.availableUnits > 0:
            for reg in self.ownedLand:
                if isPointInPoly(pos,reg.points) == True:
                    self.availableUnits = self.availableUnits-1
                    reg.Units.changeUnits(1)
                    return reg
    def Transfer(self,reg1,reg2):
        if reg1.Units.amt > 1:
            
            reg1.Units.changeUnits(-1)
            reg2.Units.changeUnits(1)

    def attack(self,atckReg,defReg,ghmanager):
        if atckReg.Units.amt > 1:
            if atckReg.Units.amt > 4:
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
                atckList.append(random.randint(1,6))
            for x in range(0,amountDef):
                defList.append(random.randint(1,6))
            print(atckList,defList)
            atckList = sorted(atckList,reverse=True)
            defList = sorted(defList,reverse=True)
            for x in range(0,min(len(atckList),len(defList))):
                var1 = random.randint(-15,15)
                var2 = random.randint(-15,15)
                if atckList[x] > defList[x]:
                    defReg.loseUnit(atckReg)
                    ghmanager.addGhostText("-1",defReg.VisCenter[0]+var1,defReg.VisCenter[1]+var2,4)
                    # kill a defending unit
                else:
                    atckReg.loseUnit(defReg)
                    ghmanager.addGhostText("-1",atckReg.VisCenter[0]+var1,atckReg.VisCenter[1]+var2,4)
                    #kill atckUnit
    def __repr__(self): # so we can print the obj
        return 'Player: {} , Colour: {} , currentPhase: {} , availableUnits: {}'.format(self.name,self.colour,self.phase,self.availableUnits)

def isPointInPoly(point,poly):
    TrueCrosses = 0
    # point - > (x,y) poly -> [(x1,y1),(x2,y2)... etc ]
    for i in range(0,len(poly)):
        point1 = poly[i]
        point2 = poly[(i+1)%len(poly)]
        if (point2[0] - point1[0]) != 0:
            Grad = (point2[1] - point1[1])/(point2[0] - point1[0])

            #print(Grad)
            const = -(Grad*point1[0] - point1[1])
            if Grad != 0:
                XCross = (point[1]-const)/(Grad)
            else:
                XCross = point1[0]
            YCross = XCross * Grad + const
        else:
            XCross =point1[0]
            YCross = point[1]

        if min(point1[0],point2[0]) <= XCross <= max(point1[0],point2[0]) and point[0] <= XCross and min(point1[1],point2[1]) <= YCross <= max(point1[1],point2[1]):
            TrueCrosses = TrueCrosses + 1
        TrueCrosses = TrueCrosses % 2
    if TrueCrosses % 2 == 0:
        return False
    else:
        return True
