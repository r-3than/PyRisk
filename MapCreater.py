import pygame , random

from Map_pb2 import Region

from Map_pb2 import Map

import Map_pb2


class RiskGame:
    def __init__(self):
        self.name = ""


class Region:
    def __init__(self,index,name,worth,provId,points,connections):
        self.index = index
        self.name = name
        self.worth = worth
        self.provId = provId
        self.points = points
        self.connections  = connections




class MapDrawer:
    def __init__(self,height,width):
        self.lengthx = width
        self.lengthy = height
        self.BLACK = (0,0,0)
        self.GREEN = (0,200,0)
        self.RED = (200,0,0)
        self.polygonList = [[]]
        self.main()
    def Reset(self):
        #index  = 0
        WINDOW_SIZE = [self.lengthx, self.lengthy]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.done = False
        pygame.display.set_caption("Risk map creater")
        self.clock = pygame.time.Clock()
    def main(self):
        index = 0
        self.Reset()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.polygonList[index].append(self.pos)
                    print(self.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.polygonList[index]) != 0:
                            self.polygonList[index].pop()

                    if event.key == pygame.K_e:
                        for x in range(0,len(self.polygonList[index]),2):
                            cord1 = self.polygonList[index][x]
                            cord2 = self.polygonList[index][x+1]
                            newcord = ((cord1[0]+cord2[0])//2,(cord1[1]+cord2[1])//2)
                            self.polygonList[index].insert(x,newcord)
                    if event.key == pygame.K_SPACE:
                        index = index + 1
                        self.polygonList.append([])
                    if event.key == pygame.K_RETURN:
                        self.done = True

            self.screen.fill(self.BLACK)
            for pol in self.polygonList:
                if len(pol) >= 3:
                    pygame.draw.polygon(self.screen , self.GREEN, pol)


            self.clock.tick(60)

            pygame.display.flip()
        print("Defining regions has been completed.")
        self.defPolygons()

    def defPolygons(self):
        ## For each poly gone - display and ask for input of its worth and region.
        ## Also make the bounding of poly gons mapping them to each other
        ## Going to need the Winding Algo or the ray casting to determine if mouse click is in poly
        ## Save that shape or not then display final shape
        index = 0
        self.Regions = []

        self.Reset()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    isPointInPoly(self.pos,self.polygonList[0])
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Name = input("Name : ")
                        Worth = input("Worth : ")
                        provId = input("provId : ")
                        self.Regions.append(Region(index,Name,Worth,provId,currPol,[]))
                        index = (index + 1) % len(self.polygonList)
                        print("It has been added")
                    if event.key == pygame.K_RETURN:
                        self.done = True

            self.screen.fill(self.BLACK)
            currPol = self.polygonList[index]
            if len(currPol) >= 3:
                pygame.draw.polygon(self.screen , self.GREEN, currPol)

            self.clock.tick(60)

            pygame.display.flip()
        print("Regions have been finalised, now setting up connections.")
        self.connectionsPolygon()

    def connectionsPolygon(self):

        self.Reset()
        index = 0
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    #print(isPointInPoly(self.pos,self.Regions[index].points))
                    for x in range(0,len(self.Regions)):
                        #print(self.Regions[x].name)
                        if isPointInPoly(self.pos,self.Regions[x].points) == True:
                            if self.Regions[index] != self.Regions[x]:
                                self.Regions[index].connections.append(self.Regions[x].index)
                                print(self.Regions[index].name,"Has been bounded to",self.Regions[x].name)
                        for BoundedConn in self.Regions[x].connections:
                            print(self.Regions[x].name,BoundedConn)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        index = (index +1) % len(self.Regions)
                        print("")
                    if event.key == pygame.K_RETURN:
                        self.done = True

            self.screen.fill(self.BLACK)
            for x in range (0,len(self.Regions)):
                pol = self.Regions[x]
                if pol == self.Regions[index]:
                    pygame.draw.polygon(self.screen , self.RED, pol.points)
                elif len(pol.points) >= 3:
                    pygame.draw.polygon(self.screen , self.GREEN, pol.points)




            self.clock.tick(60)

            pygame.display.flip()
        self.Save()

    def Save(self):
        thisMap = Map_pb2.Map()
        for x in range(0,len(self.Regions)):
            RealRegion = self.Regions[x]
            ARegion=thisMap.regions.add()
            ARegion.index = int(RealRegion.index)
            ARegion.name = RealRegion.name
            ARegion.worth = int(RealRegion.worth)
            ARegion.provId = int(RealRegion.provId)
            newlist = []
            for point in RealRegion.points:
                newlist.append(point[0])
                newlist.append(point[1])
            ARegion.points.extend(newlist)
            print(RealRegion.connections,"<-")
            ARegion.connections.extend(RealRegion.connections)
            print(ARegion.connections)

        MapFile = open("World.txt", "wb")

        MapFile.write(thisMap.SerializeToString())

        MapFile.close()


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





CreateMap = MapDrawer(1000,1800)
