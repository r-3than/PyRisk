
import random
from lib.Player import Player
from lib.Risk import Risk
print("Git moved to visual studio")
def CreatePlayers(amt):
    playerList =[]
    for _ in range(0,amt):
        colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        newPlayer = Player("Player " + str(_),colour,100  )
        playerList.append(newPlayer)
    return playerList


myPlayers = CreatePlayers(3) #Preload with three players
MyGame = Risk("Map.txt",1800,1000,myPlayers)

