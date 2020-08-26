import pygame
import os , random
import Map_pb2
import GameState_pb2
import socket , time , threading
from lib.Button import Button
from lib.Client import Client
from lib.Menu import Menu
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
BACKGROUNDCL = ()
rad = 15
def CreateMenu(List):
    aMenu = Menu()
    x=0
    for item in List:
        aMenu.addBtn(100,1000,item,x)
        x = x+1
    return aMenu

class Risk:
    def __init__(self,mapdir,sizex,sizey,PlList,first=True):
        pygame.init()
        self.mapdir = mapdir
        self.totxsize = sizex
        self.totysize = sizey
        self.amtOfPlayers = len(PlList)
        self.multiplayer = False
        self.isHosting = None
        self.Clients = []
        self.done = False
        self.Regions = []
        self.Players = PlList
        self.INFBar = InfoBar(self.Players)
        self.BLACK=(0,0,0)
        self.CurrPlayerTurn = 0
        self.font = pygame.font.Font('Marons-Regular.ttf', 35)
        self.CurrPlayer = self.Players[self.CurrPlayerTurn]
        self.myStatBar = StatBar(self.CurrPlayer)
        self.ghTextManager = ghostTextManager()
        self.recordKeyboard = False
        self.keysPressed = []
        self.CreateMenu()
        self.loadMap()
        #self.CreatePlayers()
        if first == True:
            self.GiveRegions()
        self.Main()

    def CreateMenu(self):
        sizey = self.totysize
        sizex = self.totxsize
        self.MenuOpen = True

        menuItems = [
        "New Game",
        "Load Game",
        "Save Game",
        "Host Game",
        "Connect to Game",
        "How to play",
        "Exit"
        ]
        config = open("config.txt").read().split("\n")
        for details in config:
            details = details.split(":")
            if details[0] == "name":
                self.multiname = details[1]
                nameLab = Label(25,100,"Your name : "+self.multiname)
            if details[0] == "amtply":
                self.multiamtply = int(details[1])
                amtplyLab = Label(25,150,"Amount of players : "+str(self.multiamtply))
            if details[0] == "hostname":
                self.multiHost = details[1]
                HostLab = Label(25,200,"Host address : "+self.multiHost)
            if details[0] == "address":
                self.multiaddress = details[1]
                addrLab = Label(25,250,"Adress to connect to : "+self.multiaddress)
            if details[0] == "port":
                self.multiPort = int(details[1])
                PortLab = Label(25,300,"Port : "+str(self.multiPort))
            if details[0] == "map":
                self.multimapdir = details[1]
                mapdirLab = Label(25,350,"Mapfile : "+self.multimapdir)
        self.MainMenu = CreateMenu(menuItems)
        self.MainMenu.Buttons[len(self.MainMenu.Buttons)-1].index = 99
        self.MainMenu.Buttons[len(self.MainMenu.Buttons)-1].subMenu = False

        newMenu = Menu(25,(100,100))
        mapLab = Label(25,0,"Map Files:")
        newMenu.addItem(mapLab)
        mypath = "./maps"
        saves = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        x= len(self.MainMenu.Buttons)-1
        index = 1
        for save in saves:
            displayText = self.font.render(save, True, WHITE)
            aRect = displayText.get_rect()
            aRect[0] = 25
            aRect[1] = 50 +(index*75)
            btn = Button(aRect,save,x,False)
            newMenu.addBtnManual(btn)
            index = index+1

        plLab = Label(325,0,"Amount of Players:")
        newMenu.addItem (plLab)
        for pl in range(2,9):
            displayText = self.font.render(str(pl), True, WHITE)
            aRect = displayText.get_rect()
            aRect[0] = 325
            aRect[1] = 50 + ((pl-1)*75)
            btn = Button(aRect,str(pl),x+1,False)
            newMenu.addBtnManual(btn)


        displayText = self.font.render("Start", True, WHITE)
        aRect = displayText.get_rect()
        self.InfoLab = Label(25,sizey-aRect[3]-25,"MapFile :         Players :")
        newMenu.addItem(self.InfoLab)



        displayText = self.font.render("Start", True, WHITE)
        aRect = displayText.get_rect()
        print(sizex,aRect)
        aRect[0] = sizex-aRect[2]-25
        aRect[1] = sizey-aRect[3]-25
        startGame = Button(aRect,"Start",x+2,False)
        newMenu.addBtnManual(startGame)
        self.MainMenu.SubMenus.append(newMenu)


        x=x+3 ## load save
        self.loadMenu = Menu()
        displayText = self.font.render("Gamesaves:", True, WHITE)
        aRect = displayText.get_rect()
        infLab = Label(25,25,"Gamesaves:")
        self.loadMenu.addItem(infLab)
        mypath = "./saves"
        self.loadedSaves = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
        for y in range(0,len(self.loadedSaves)):
            displayText = self.font.render(self.loadedSaves[y], True, WHITE)
            aRect = displayText.get_rect()
            aRect[0] = 25
            aRect[1] = 100 + (y*75)
            self.lasty = 100 +(y*75)
            savebtn = Button(aRect,self.loadedSaves[y],x,False)
            self.loadMenu.addBtnManual(savebtn)



        ##Do manual saves here
        x = x+1
        self.MainMenu.SubMenus.append(self.loadMenu)

        saveMenu = Menu()
        infLab = Label(25,25,"Name of savefile:")
        saveMenu.addItem(infLab)
        self.textInp = TextInput(25,100,self.keysPressed)
        saveMenu.addItem(self.textInp)
        displayText = self.font.render("Save", True, WHITE)
        aRect = displayText.get_rect()
        aRect[0] = sizex-aRect[2]-25
        aRect[1] = sizey-aRect[3]-25
        startGame = Button(aRect,"Save",x,False)
        saveMenu.addBtnManual(startGame)
        self.MainMenu.SubMenus.append(saveMenu)

        x = x+1
        multiHMenu = Menu()
        titleLab = Label(25,25,"Multiplayer Host Game")
        multiHMenu.addItem(titleLab)



        displayText = self.font.render("Host", True, WHITE)
        aRect = displayText.get_rect()
        aRect[0] = sizex-aRect[2]-25
        aRect[1] = sizey-aRect[3]-25
        hostBtn = Button(aRect,"Host",x,False)
        multiHMenu.addBtnManual(hostBtn)

        multiHMenu.addItem(nameLab)
        multiHMenu.addItem(amtplyLab)
        multiHMenu.addItem(HostLab)
        multiHMenu.addItem(addrLab)
        multiHMenu.addItem(PortLab)
        multiHMenu.addItem(mapdirLab)

        self.MainMenu.SubMenus.append(multiHMenu)

        x = x+1
        multiCMenu = Menu()
        titleLab = Label(25,25,"Multiplayer connect Game")
        multiCMenu.addItem(titleLab)



        displayText = self.font.render("Connect", True, WHITE)
        aRect = displayText.get_rect()
        aRect[0] = sizex-aRect[2]-25
        aRect[1] = sizey-aRect[3]-25
        connectBtn = Button(aRect,"Connect",x,False)
        multiCMenu.addBtnManual(connectBtn)
        multiCMenu.addItem(nameLab)
        multiCMenu.addItem(amtplyLab)
        multiCMenu.addItem(HostLab)
        multiCMenu.addItem(addrLab)
        multiCMenu.addItem(PortLab)
        multiCMenu.addItem(mapdirLab)
        self.MainMenu.SubMenus.append(multiCMenu)


        htpMenu = Menu()
        DescLab = Label(0,0,"How to play etc etc")
        htpMenu.addItem(DescLab)
        self.MainMenu.SubMenus.append(htpMenu)

    def HostGame(self):
        self.reset(self.multiamtply)
        self.loadMap()
        self.GiveRegions()
        self.multiplayer = True
        self.isHosting = True
        self.PlayerId = 0
        #Host = "192.168.1.134"
        #Port = 52521
        Host = self.multiHost
        Port = self.multiPort


        names = []
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((Host,Port))
        self.Players[0].name = "-Host- "+self.multiname
        while len(self.Clients) < len(self.Players)-1:
            print("Listening for a client")
            sock.listen(0)
            conn , addr = sock.accept()
            plname=conn.recv(4096).decode("windows-1252")

            newClient = Client(conn,addr)
            self.Clients.append(newClient)
            self.Players[len(self.Clients)].name = plname
            print("New client connected! as ",plname)
        print("All clients connected")
        thisState = self.getState()
        print("Current state got!")
        indexer = 0
        for cl in self.Clients:
            indexer = indexer + 1
            cl.conn.send(indexer.to_bytes(32,"big"))
            print("id sent!")
            time.sleep(0.001)
            cl.conn.send(thisState.SerializeToString())
            print("sent state to player",indexer)
        self.sock = sock

        self.ListenerThread = threading.Thread(target=self.ListenerThread)
        self.ListenerThread.start()

    def ConnectGame(self,address="localhost"):
        self.multiplayer = True
        self.isHosting = False

        address = self.multiaddress
        Port = self.multiPort
        ##Port = 52521



        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((address,Port))
        time.sleep(0.01)
        self.sock.send(self.multiname.encode("windows-1252"))

        ## want to update gui

        self.PlayerId = self.sock.recv(1024)
        self.PlayerId = int.from_bytes(self.PlayerId, byteorder='big')
        print("Id has been recved")

        ## send ply name
        self.data = self.sock.recv(4096)
        print("Game state has been recved")
        newGameState = GameState_pb2.Game()
        newGameState.ParseFromString(self.data)
        self.loadData(newGameState)

        print("New state loaded")
        self.ListenerThread = threading.Thread(target=self.ListenerThread)
        self.ListenerThread.start()

        print("Connection has been made",self.PlayerId)

    def GiveRegions(self):
        indexer = 0
        for x in range(0,len(self.Regions)):
            indexValue = random.randint(0,len(self.Regions)-1)
            aRegion = self.Regions[indexValue]
            self.Regions.pop(indexValue)
            self.Players[indexer].addLand(aRegion)
            indexer = (indexer+1) % self.amtOfPlayers

        for ply in self.Players:
            self.Regions = self.Regions + ply.ownedLand

        newUnitsamt = 0
        for reg in self.CurrPlayer.ownedLand:
            var1 = random.randint(-7,7)
            var2 = random.randint(-7,7)

            self.ghTextManager.addGhostText("+"+str(reg.worth),reg.VisCenter[0]+var1,reg.VisCenter[1]+var2,5)
            newUnitsamt = newUnitsamt + reg.worth
        self.CurrPlayer.availableUnits = newUnitsamt
        self.myStatBar.update()

    def loadGame(self,filedir):
        newGameState = GameState_pb2.Game()
        f = open(filedir,"rb")
        newGameState.ParseFromString(f.read())
        self.loadData(newGameState)
        self.Main()

    def loadData(self,data):
        newGameState = data
        plyList = []
        for ply in newGameState.Players:
            aPlayer = Player(ply.playerName,ply.colour,ply.unitsFree)
            plyList.append(aPlayer)

        #self.__init__(newGameState.mapdir,newGameState.sizex,newGameState.sizey,plyList,False)

        self.mapdir = newGameState.mapdir
        self.totxsize = newGameState.sizex
        self.totysize = newGameState.sizey
        self.CurrPlayerTurn = newGameState.currentPlayerIndex


        self.amtOfPlayers = len(plyList)
        self.done = False
        self.Players = plyList
        self.INFBar = InfoBar(self.Players)

        self.CurrPlayer = self.Players[self.CurrPlayerTurn]
        self.myStatBar = StatBar(self.CurrPlayer)
        self.ghTextManager = ghostTextManager()
        self.loadMap()

        for x in range(0,len(plyList)):
            for y in range(0,len(newGameState.Players[x].regionsIndex)):
                currentReg = self.Regions[newGameState.Players[x].regionsIndex[y]]
                plyList[x].ownedLand.append(currentReg)
                currentReg.SetOwner(plyList[x])
                currentReg.setUnit(newGameState.Players[x].unitsIndex[y])

        self.CurrPlayer.Phase = newGameState.currentPlayerPhase
        for gh in newGameState.GhostTexts:
            self.ghTextManager.addGhostText(gh.text,gh.x,gh.y,gh.length)
            #self.Main()
    def UpdateState(self): ##  Only applies update to units in region and player controled regions DOESNT create map again (more effiecnt)
        newGameState = GameState_pb2.Game()
        newGameState.ParseFromString(self.data)
        ## player turn updates:
        self.CurrPlayerTurn = newGameState.currentPlayerIndex
        self.CurrPlayer = self.Players[self.CurrPlayerTurn]
        self.CurrPlayer.Phase = newGameState.currentPlayerPhase
        #self.CurrPlayer.availableUnits = newGameState.unitsFree
        ## add new units etc
        for x in range(0,len(self.Players)):
            self.Players[x].ownedLand = []
            for y in range(0,len(newGameState.Players[x].regionsIndex)):
                index = newGameState.Players[x].regionsIndex[y]
                for reg in self.Regions:
                    if reg.index  == index:
                        currentReg = reg
                        self.Players[x].ownedLand.append(currentReg)
                        currentReg.SetOwner(self.Players[x])
                        currentReg.setUnit(newGameState.Players[x].unitsIndex[y])

        for x in range(0,len(newGameState.Players)):
                self.Players[x].availableUnits = newGameState.Players[x].unitsFree
                self.Players[x].Phase =newGameState.Players[x].phase
        ## Show losses
        for gh in newGameState.GhostTexts:
            found = False
            for contained in self.ghTextManager.GhostTexts:
                if gh.index == contained.index:
                    found = True
            if found == False:
                self.ghTextManager.addGhostText(gh.text,gh.x,gh.y,gh.length)
        self.myStatBar.ChangePly(self.CurrPlayer)
        #self.myStatBar.update()
    def getState(self):
        thisGameState = GameState_pb2.Game()
        thisGameState.name = ""
        thisGameState.mapdir = self.mapdir
        thisGameState.currentPlayerIndex = self.CurrPlayerTurn
        thisGameState.sizex = self.totxsize
        thisGameState.sizey = self.totysize
        thisGameState.currentPlayerPhase = self.CurrPlayer.Phase

        for ply in self.Players:
            APlayer=thisGameState.Players.add()
            APlayer.playerName =ply.name
            APlayer.phase = ply.Phase
            APlayer.unitsFree = ply.availableUnits
            tempColour = [ply.colour[0],ply.colour[1],ply.colour[2]]
            APlayer.colour.extend(tempColour)
            indexList = []
            unitList = []
            for reg in ply.ownedLand:
                indexList.append(reg.index)
                unitList.append(reg.Units.amt)
            APlayer.regionsIndex.extend(indexList)
            APlayer.unitsIndex.extend(unitList)

        for ghText in self.ghTextManager.GhostTexts:
            aText = thisGameState.GhostTexts.add()
            aText.text = ghText.text
            aText.x = ghText.x
            aText.y = ghText.y
            aText.length = ghText.length
            aText.index = ghText.index
            #print(ghText.text)
        return thisGameState

    def saveGame(self,dir):
        state=self.getState()

        print("savegame called with",dir)

        MapFile = open(dir, "wb")

        MapFile.write(state.SerializeToString())

        MapFile.close()

    def reset(self,amtPl):
        playerList =[]
        for x in range(0,amtPl):
            colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            newPlayer = Player("Player "+str(x+1),colour,100  )
            playerList.append(newPlayer)
        self.amtOfPlayers = amtPl
        self.done = False
        self.multiplayer = False
        self.Regions = []
        self.Players = playerList
        self.INFBar = InfoBar(self.Players)
        self.CurrPlayerTurn = 0
        self.CurrPlayer = self.Players[self.CurrPlayerTurn]
        self.myStatBar = StatBar(self.CurrPlayer)

    def BtnCalc(self):

        btn =self.MainMenu.clickPointer(self.pos)
        print(btn)
        if btn != None:
            if btn[0] == 0:
                self.recordKeyboard = True
                print(self.keysPressed)
                #-> NewGame -> create options for the menu to create x amt of players and new map
                print("")
            if btn[0] == 1:

                mypath = "./saves/"
                """temploadedSaves = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
                print(temploadedSaves)
                tempamt =0
                for y in range(0,len(temploadedSaves)):

                    if temploadedSaves[y] not in self.loadedSaves:
                        tempamt = tempamt + 1
                        print(temploadedSaves[y])
                        displayText = self.font.render(temploadedSaves[y], True, WHITE)
                        aRect = displayText.get_rect()
                        aRect[0] = 25
                        aRect[1] = self.lasty + (tempamt*75)
                        savebtn = Button(aRect,temploadedSaves[y],8,False)
                        self.MainMenu.SubMenus[1].addBtnManual(savebtn)
                self.loadedSaves = temploadedSaves
                #-> Load -> list maps files"""

                print("")
            if btn[0] == 2:
                self.recordKeyboard = True
                print(self.keysPressed)
                #-> Save -> saveGame via save state (some nameing system??)
                print("")
            if btn[0] == 3:
                #-> Multiplayer -> Host or connect -> another menu for ip and port (map and amt of players)
                print("WIP!")
            if btn[0] == 99:
                self.done = True

            if btn[0] == 6: # a map file dir btn
                self.filename = btn[1]
                if self.amtPly != None:
                    self.InfoLab.changeText("Map File: " +btn[1] + " Players: " + str(self.amtPly))
                else:
                    self.InfoLab.changeText("Map File: " +btn[1] + " Players: ")


            if btn[0] == 7: # A player amount btn
                self.amtPly = int(btn[1])
                if self.filename != None:
                    self.InfoLab.changeText("Map File: " +self.filename + " Players: " + btn[1])
                else:
                    self.InfoLab.changeText("Map File: " + " Players: "+btn[1])

            if btn[0] == 8: #Start game
                self.mapdir = "./maps/"+self.filename
                self.reset(self.amtPly)
                self.loadMap()
                self.GiveRegions()
                self.MainMenu.display = False
                self.MainMenu.back()

            if btn[0] == 9:
                self.MainMenu.display = False
                self.loadGame("./saves/"+btn[1])



            if btn[0] ==10:
                self.MainMenu.display = False
                print("Called! -> saving game")
                self.saveGame("./saves/"+self.textInp.text)

            if btn[0] == 11:
                self.HostGame()
                self.MainMenu.display = False

            if btn[0] == 12:
                self.ConnectGame()
                self.MainMenu.display = False

    def ListenerThread(self):
        print("Listening for incomming data")
        while self.done == False:
            if self.isHosting == True: #Host
                if self.CurrPlayerTurn != 0:
                    data =self.Clients[self.CurrPlayerTurn-1].conn.recv(4096)
                    for x in range(0,len(self.Clients)):
                        if self.CurrPlayerTurn-1 != x:

                            self.Clients[x].conn.send(data)
                    self.data = data
                    self.UpdateState()

            else: # CLient
                if self.CurrPlayerTurn != self.PlayerId:
                    print("Client is waiting for responses from server")
                    data=self.sock.recv(4096)
                    self.data = data
                    self.UpdateState()
    def checkWin(self):
        varx = random.randint(-50,50)
        vary = random.randint(-50,50)
        for pl in self.Players:
            if pl.amtOfLand() == 0:
                pl.eliminate()
                self.ghTextManager.addGhostText(pl.name + " has been eliminated!",100,self.totysize//3,8)
        if len(self.Players) == 1:
            varx = random.randint(-50,50)
            vary = random.randint(-50,50)
            self.ghTextManager.addGhostText(self.Players[0].name + " Has won the game! \n press Esc to start a new game" ,100+varx,self.totysize//2+vary,8)

    def playerActionMouse(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pos = pygame.mouse.get_pos()
            if self.MainMenu.display == True:
                self.BtnCalc()
                    #-> Exit ->Quit game
            if self.MainMenu.display == False:
                if self.CurrPlayer.Phase == 1: # Phase -> 1 (attack) -> 2 (deploy) -> 3 (movement) ->set back to 1 change curr player
                    if event.button ==1:
                        print("left")
                        for reg in self.CurrPlayer.ownedLand:
                            if reg.highl == True:
                                reg.highlight()
                            if isPointInPoly(self.pos,reg.points) == True:
                                reg.highlight()
                                self.selectedTile = reg
                                print("found reg")
                    elif event.button ==3 and self.selectedTile != None:
                        print("right")
                        for reg in self.Regions:
                            if isPointInPoly(self.pos,reg.points) == True and isAdj(self.selectedTile,reg) ==True and (reg not in self.CurrPlayer.ownedLand):
                                self.CurrPlayer.attack(self.selectedTile,reg,self.ghTextManager)
                        self.checkWin()



                    #print("attacking")

                elif self.CurrPlayer.Phase ==2:

                    print(self.selectedTile)
                    self.selectedTile = None
                    addedReg=self.CurrPlayer.addUnit(self.pos)
                    if addedReg != None:
                        var1 = random.randint(-10,10)
                        var2 = random.randint(-10,10)
                        self.ghTextManager.addGhostText("+1",addedReg.VisCenter[0]+var1,addedReg.VisCenter[1]+var2,3)

                elif self.CurrPlayer.Phase ==3:
                    if event.button ==1:
                        print("left")
                        for reg in self.CurrPlayer.ownedLand:
                            if reg.highl == True:
                                reg.highlight()
                            if isPointInPoly(self.pos,reg.points) == True:
                                reg.highlight()
                                self.selectedTile = reg
                    elif event.button ==3 and self.selectedTile != None:
                        print("right")
                        for reg in self.CurrPlayer.ownedLand:
                            if isPointInPoly(self.pos,reg.points) == True:
                                self.CurrPlayer.Transfer(self.selectedTile,reg)

                #self.CurrPlayer.addUnit(print("movement")self.pos)
                self.myStatBar.update()

    def playerActionKeyboard(self,event):
        if event.type == pygame.KEYDOWN:
            if self.recordKeyboard == True:
                if event.key != pygame.K_BACKSPACE:
                    self.keysPressed.append(chr(event.key))
                elif len(self.keysPressed) != 0:
                    self.keysPressed.pop()
                self.textInp.update(self.keysPressed)


            if event.key ==pygame.K_ESCAPE:
                self.recordKeyboard = False
                self.keysPressed = []
                self.MainMenu.back()
                self.MainMenu.display = not self.MainMenu.display


            #self.selectedTile = None
            self.myStatBar.update()
            if event.key == pygame.K_e and not self.recordKeyboard:
                self.saveGame()
            if event.key == pygame.K_r and not self.recordKeyboard:
                self.loadGame("./GameState.txt")

            if event.key == pygame.K_RETURN:

                nextStage =  self.CurrPlayer.nextPhase()

                if nextStage == True:
                    for reg in self.CurrPlayer.ownedLand:
                        if reg.highl == True:
                            reg.highlight()
                    self.selectedTile = None
                    self.CurrPlayerTurn = (self.CurrPlayerTurn +1) %len(self.Players)
                    self.CurrPlayer = self.Players[self.CurrPlayerTurn]
                    while self.CurrPlayer.dead == True:
                        self.CurrPlayerTurn = (self.CurrPlayerTurn +1) %len(self.Players)
                        self.CurrPlayer = self.Players[self.CurrPlayerTurn]
                    self.myStatBar.ChangePly(self.CurrPlayer)
                    newUnitsamt = 0
                    for reg in self.CurrPlayer.ownedLand:
                        var1 = random.randint(-7,7)
                        var2 = random.randint(-7,7)

                        self.ghTextManager.addGhostText("+"+str(reg.worth),reg.VisCenter[0]+var1,reg.VisCenter[1]+var2,5)
                        newUnitsamt = newUnitsamt + reg.worth
                    self.CurrPlayer.availableUnits = newUnitsamt

                self.myStatBar.update()
                if self.CurrPlayer.Phase == 2:
                    for reg in self.CurrPlayer.ownedLand:
                        if reg.highl == True:
                            reg.highlight()
                    self.selectedTile = None

    def sendAll(self,data):
        for cl in self.Clients:
            cl.conn.send(data)

    def Main(self):
        ## NOTE TO SELF: // multiplayer
        ## if is host use a thread? dedecate to listen to next player in self.Clients array
        ## for client should use a thread to listen for new data or should include
        ## in the main function to get the new data which would be better
        WINDOW_SIZE = [self.totxsize, self.totysize]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.selectedTile = None
        self.filename = None
        self.amtPly = None
        pygame.display.set_caption("Risk Game")
        self.clock = pygame.time.Clock()

        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEMOTION and self.MenuOpen == True:
                    pos = pygame.mouse.get_pos()
                    self.MainMenu.parsePointer(pos)

                else:

                    if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and self.multiplayer:
                        if self.PlayerId == self.CurrPlayerTurn:
                            print("send packet")
                            self.playerActionMouse(event)
                            self.playerActionKeyboard(event)
                            thisState = self.getState()
                            data = thisState.SerializeToString()
                            if not self.isHosting:
                                self.sock.send(data)
                            else:
                                self.sendAll(data)
                        else:
                            print("Not your turn please wait")

                    if not self.multiplayer:
                        self.playerActionMouse(event)
                        self.playerActionKeyboard(event)

            self.draw()
        pygame.quit()

    def draw(self):
        self.screen.fill(self.BLACK)

        if self.MainMenu.display ==True:
            self.MainMenu.draw(self.screen)

        else:
            for Pl in self.Players:
                for Reg in Pl.ownedLand:
                    Reg.draw(self.screen)

            self.myStatBar.draw(self.screen)
            self.INFBar.draw(self.screen)
            self.ghTextManager.draw(self.screen)

        self.clock.tick(60)

        pygame.display.flip()

    def loadMap(self):
        self.Regions = []
        Map = Map_pb2.Map()
        f = open(self.mapdir,"rb")
        Map.ParseFromString(f.read())
        print(Map)
        for Reg in Map.regions:
            newPoints = []
            for x in range(0,len(Reg.points),2):
                newPoints.append((Reg.points[x],Reg.points[x+1]))
            newRegion = Region(Reg.index,Reg.name,Reg.worth,Reg.provId,newPoints,Reg.connections)
            self.Regions.append(newRegion)
        print(self.Regions)
        for Reg in self.Regions:
            print(Reg.points)


def findVisualCenter(points):
    x_total = 0
    y_total = 0
    for point in points:
        x_total = x_total + point[0]
        y_total = y_total + point[1]
    x_mean = int(round(x_total / len(points),0))
    y_mean = int(round(y_total / len(points),0))
    return (x_mean,y_mean)

def isAdj(reg1,reg2):
    i = reg1.index
    found = False
    for conn in reg2.connections:
        if i == conn:
            found = True
    return found

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
