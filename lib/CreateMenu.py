
def CreateMenu(List):
    aMenu = Menu()
    x=0
    for item in List:
        aMenu.addBtn(100,1000,item,x)
        x = x+1
    return aMenu
    
def isPointInPoly(point,poly):
    if winding(point,poly) != 0:
        return True
    else:
        return False
        
def isLeft(P0,P1,P2):
    return ((P1[0]-P0[0])*(P2[1]-P0[1]) - (P2[0]-P0[0])*(P1[1]-P0[1]))

def winding(point,poly):
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
                if isLeft(point1,point2,point) <0:
                    wn = wn-1
    return wn