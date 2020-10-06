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
print("Git moved to visual studio")

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
    for _ in range(0,amt):
        colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        newPlayer = Player(input("Player name:"),colour,100  )
        playerList.append(newPlayer)
    return playerList


myPlayers = CreatePlayers(3)
MyGame = Risk("Map.txt",1800,1000,myPlayers)
#MyGame.loadMap()
