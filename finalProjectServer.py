# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:54:47 2018

@author: diazrodrigueza
"""

import json
import socket
import sys
import random

def rules():
    message = 'Guess the right color combination randomly chosen by the server. \n All the colors in the combination are unique and the server will let \n you know which colors are in the correct location and which are not. \n The colors used in this game are red, orange, yellow, green, blue, and purple. \n'
      
    return message


def createcode():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    pickedcolors = []
    x = 0

    while x < 4:
        rng = random.randint(0, 5)

        pickedcolors.append(colors[rng])

        x = x + 1
        
    if not duplicates(pickedcolors):
        return pickedcolors
    else:
        return repick(pickedcolors, colors)


def repick(pickedcolors, colors):
    repicked = []

    for item in pickedcolors:
        if item not in repicked and len(repicked)<4:
            repicked.append(item)
        else:
            while len(repicked) < 4:
                
                rng = random.randint(0, 5)
                newcolor = colors[rng]

                if newcolor not in repicked:
                    repicked.append(newcolor)

    return repicked


def duplicates(pickedcolors):
    finalcolors = []

    for item in pickedcolors:
        if item not in finalcolors:
            finalcolors.append(item)

    if len(finalcolors) == len(pickedcolors):
        return False

    return True


def correctplace(pickedcolors, guessedcolors):
    x = 0
    correct = 0

    while x<4:
        if pickedcolors[x] == guessedcolors[x]:
            correct = correct + 1
        x += 1
    return correct


def correctcolor(pickedcolors, guessedcolors):
    correct = 0
    
    for color in guessedcolors:
        if color in pickedcolors and pickedcolors.index(color)!=guessedcolors.index(color):
            correct+=1
    
    return correct

def ifwon(correct):
    if correct==4:
        return True

def play(guessedcolors, correctcolors):
    x = -1
    
    cp = correctplace(correctcolors, guessedcolors)
    
    if ifwon(cp):
        x = 0
    else:
        x = 1
    
    return x

def play2(guessedcolors, correctcolors):
    message = ''
    
    cp = correctplace(correctcolors, guessedcolors)
    cc = correctcolor(correctcolors, guessedcolors)
    
    if ifwon(cp):
        message = 'You won!'
    else:
        message = str(cp)+' color(s) are in the correct place and '+str(cc)+' color(s) are correct but in the wrong place.'
    
    return message
###############################################################################
    
serverport = 9999
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', serverport))
serversocket.listen(1)

welcome = 'Welcome to Mastermind! Would you like to hear the rules before playing? (y/n)'

connectionsocket, address = serversocket.accept()
connectionsocket.send(welcome.encode())

message = connectionsocket.recv(1024).decode()
if message=='y':
    connectionsocket.send(rules().encode())

code = createcode()
for color in code:
    print(color)

guess4colors = ('Guess four colors: ')
lose = ('Sorry! You lost!')

connectionsocket.close()

blank = ''

while True:
    connectionsocket, address = serversocket.accept()
    
    connectionsocket.send(guess4colors.encode())
    
    data = connectionsocket.recv(1024).decode()
    data_loaded = json.loads(data)
    
    if data_loaded['h']>=10:
        connectionsocket.send(lose.encode())
        connectionsocket.close()
        break
    
    score = play2(data_loaded['b'], code)
    
    if play(data_loaded['b'], code) == 0:
        connectionsocket.send(score.encode())
        connectionsocket.close()
        break
        
    connectionsocket.send(score.encode())

connectionsocket.close()