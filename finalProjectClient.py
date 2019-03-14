# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 11:07:21 2018

@author: diazrodrigueza
"""
import json
import socket
import sys

servername = 'localhost'
serverport = 9999

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((servername, serverport))

message = clientsocket.recv(1024).decode()
print(message)

clientresponse = input()

clientsocket.send(clientresponse.encode())
message = clientsocket.recv(1024).decode()
print(message)

data = {'h':0, 'b':''}
guesses = []

while clientresponse != 'exit':
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((servername, serverport))
    
    #prints guess 4 colors
    serverresponse = clientsocket.recv(1024).decode()
    print(serverresponse)
    
    guesses.clear()
    
    while len(guesses)<4:
        guesses.append(input())

    data['h'] = data['h']+1
    data['b'] = guesses

    clientsocket.send(json.dumps(data).encode())
    message = clientsocket.recv(1024).decode()
    print(message)
    
    if message==('You won!'):
        break
    
    clientsocket.close()