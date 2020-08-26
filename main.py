import Map_pb2
import GameState_pb2
import pygame
import random
import time
import datetime
import os
import socket
import threading

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
from lib.Risk import Risk
from lib.Player import Player
print("Github Commit test from Atom")

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

def isAdj(reg1,reg2):
    i = reg1.index
    found = False
    for conn in reg2.connections:
        if i == conn:
            found = True
    return found

def findVisualCenter(points):
    x_total = 0
    y_total = 0
    for point in points:
        x_total = x_total + point[0]
        y_total = y_total + point[1]
    x_mean = int(round(x_total / len(points),0))
    y_mean = int(round(y_total / len(points),0))
    return (x_mean,y_mean)

def CreatePlayers(amt):
    playerList =[]
    for x in range(0,amt):
        colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        newPlayer = Player(input("Player name:"),colour,100  )
        playerList.append(newPlayer)
    return playerList


myPlayers = CreatePlayers(3)
MyGame = Risk("Map.txt",1000,1000,myPlayers)
#MyGame.loadMap()
