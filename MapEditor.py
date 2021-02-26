import Map_pb2
import pygame

def loadFile(dirname):
    MapState = Map_pb2.Map()
    f = open(dirname,"rb")
    MapState.ParseFromString(f.read())
    return MapState

filename = "./World.txt"
Map = loadFile(filename)

class Region:
    def __init__(self,index,name,worth,provId,points,connections):
        self.index = index
        self.name = name
        self.worth = worth
        self.provId = provId
        self.points = points
        self.connections  = connections


class MapEditor:
    def __init__(self,height,width,Mapping):
        self.lengthx = width
        self.lengthy = height
        self.BLACK = (0,0,0)
        self.GREEN = (0,200,0)
        self.RED = (200,0,0)
        self.polygonList = [[]]
        self.Regions = []
        self.ParseFile(Mapping)
        self.main()
    def ParseFile(self,Mapping):
        for reg in Mapping.regions:
            print(str(reg.name),"Has been loaded")
            newPoints = []
            for x in range(0,len(reg.points),2):
                newPoints.append((reg.points[x],reg.points[x+1]))
            aReg = Region(int(reg.index),reg.name,reg.worth,reg.provId,newPoints,[])
            self.Regions.append(aReg)
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

def isPointInPoly(point,poly):
    if winding(point,poly) != 0:
        return True
    else:
        return False
def isLeft(P0,P1,P2): # all are points in form (x,y)
      return ((P1[0] - P0[0]) * (P2[1] - P0[1]) - (P2[0] -  P0[0]) * (P1[1] - P0[1]))

def winding(point,poly):
    wn=0
    for i in range(0,len(poly)):
        point1 = poly[i]
        point2 = poly[(i+1)%len(poly)]
        if point1[1] <= point[1]:
           if point2[1] >  point[1]:
               if isLeft(point1,point2,point) > 0:
                   wn = wn + 1
        else:
            if point2[1] <= point[1]:
                if isLeft(point1,point2,point) <0:
                    wn = wn -1
    return wn


Testing = MapEditor(1000,1800,Map)


