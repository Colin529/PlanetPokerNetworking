# server program v1.0
# Hefelc 
# 11/27/2025
'''
setting up game flow. Moved game logic to server side to
better demonstrate networking principles. Also allows hypothetical
scaling if multiplayer was desired
'''

from socket import * 
from _thread import *
from random import *

#card_deck
def deckCard():
    deckSize = 40
    raNum = randint(1,deckSize)
    if(raNum <= 5):
        return "Mercury"
    elif(raNum <= 10):
        return "Mars"
    elif(raNum <= 15):
        return "Venus"
    elif(raNum <= 20):
        return "Earth"
    elif(raNum <= 25):
        return "Neptune"
    elif(raNum <= 30):
        return "Uranus"
    elif(raNum <= 35):
        return "Saturn"
    else:
        return "Jupiter"
    
        
def serverGame(connection_socket, userName):
    uN = userName
    returnMessage = "Welcome " + uN + " to Planet Poker."
    connection_socket.send(returnMessage.encode())
    activeGame = True

    userChips = 20
    currPool = 0
    userHand = []
    compHand = []

    if(activeGame):
      #deal userHand and compHand
      for i in range(5):
        userHand.append(deckCard())
        compHand.append(deckCard())
        userHandString = " ".join(userHand)
        compHandString = " ".join(compHand)
    userChips -= 1
    currPool += 1
    dealt_hand = uN + " " + userHandString + " " + str(userChips) + " " +  compHandString + " \n"
    connection_socket.send(dealt_hand.encode())

    drawAction = connection_socket.recv(1024).decode()
    if drawAction.startswith("RedrawCards"):
        cardIndex = drawAction.split(" ")[1]
        numberOfCards = len(cardIndex)

        for i in range(numberOfCards):
            newCard = deckCard()
            cardToReplace = int(cardIndex[i])
            userHand[cardToReplace-1] = newCard

        userHandString = " ".join(userHand)
        new_hand = "RedealtCards " + userHandString + " \n"
        connection_socket.send(new_hand.encode())

    elif drawAction.startswith("DrawDecline"):
        print("User will not redraw")
        connection_socket.send("DrawDeclinedOK \n".encode())

    betAction = connection_socket.recv(1024).decode()
    if betAction.startswith("RaiseBet"):
        raiseAmount = int(betAction.split(" ")[1])
        userChips -= raiseAmount
        currPool += raiseAmount
        newBetMessage = "BetRaised " + str(userChips) + " " + str(currPool) + " \n"
        connection_socket.send(newBetMessage.encode())

    elif betAction.startswith("Check"):
        print("User checks")
        connection_socket.send("CheckOK \n".encode())




        



        
    
    
def serverMain():
    server_port = 12002
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", server_port))
    server_socket.listen(1)

    print('The server is ready to recieve')

    while True:
        connection_socket, addr = server_socket.accept()

        sentence = connection_socket.recv(1024).decode()
        codeWord = sentence.split(' ')[0].strip()
        userName = sentence.split(' ')[1].strip()
        if(codeWord == "PlayGame"):
            serverGame(connection_socket, userName)

        
        connection_socket.close()

serverMain()
