
def CreateMenu(List):
    aMenu = Menu()
    x=0
    for item in List:
        aMenu.addBtn(100,1000,item,x)
        x = x+1
    return aMenu
    
