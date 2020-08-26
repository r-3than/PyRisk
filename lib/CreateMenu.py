
def CreateMenu(List):
    aMenu = Menu()
    x=0
    for item in List:
        aMenu.addBtn(100,1000,item,x)
        x = x+1
    return aMenu

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
