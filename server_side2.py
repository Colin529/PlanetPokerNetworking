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
    
def handValue(hand):
    card1 = hand[0]
    card2 = hand[1]
    card3 = hand[2]
    card4 = hand[3]
    card5 = hand[4]
    value = 0
    
    amounts = []
    for i in range(8):
        amounts.append(0)
    #Search for a Matching
    for i in range(5):
        #AAAAAAAAAAAAHHHHHHHHHHHH
        if(hand[i] == "Mercury"):
            #amountMer += 1
            amounts[0] += 1
        elif(hand[i] == "Mars"):
            #amountMar += 1
            amounts[1] += 1
        elif(hand[i] == "Venus"):
            #amountVen += 1
            amounts[2] += 1
        elif(hand[i] == "Earth"):
            #amountEar += 1
            amounts[3] += 1
        elif(hand[i] == "Neptune"):
            #amountNep += 1
            amounts[4] += 1
        elif(hand[i] == "Uranus"):
            #amountUra += 1
            amounts[5] += 1
        elif(hand[i] == "Saturn"):
            #amountSat += 1
            amounts[6] += 1
        elif(hand[i] == "Jupiter"):
            #amountJup += 1
            amounts[7] += 1

    pair = twoPairs = threeKind = straight = fullHouse = fourKind = fiveKind = False
    whereThree = whereTwo = whereFour = whereFive = endStraight = 0
    for i in range(len(amounts)):
        if amounts[i] == 2:
            whereTwo = i
            if pair:
                twoPairs = True
            if threeKind:
                fullHouse = True
            pair = True
        elif amounts[i] == 3:
            whereThree = i
            if pair: 
                fullHouse = True
            threeKind = True

        elif amounts[i] == 4:
            whereFour = i
            fourKind = True
            break
        elif amounts[i] == 5:
            whereFive = i
            fiveKind = True
            break
    for i in range(len(amounts) - 5):
        if amounts[i] == 1:
            if amounts[i+1] == 1:
                if amounts[i+2] == 1:
                    if amounts[i+3] == 1:
                        if amounts[i+4] == 1:
                            straight = True
                            endStraight = i + 4

    if fiveKind:
        value = 10000 + whereFive + 1
    elif fourKind:
        value = 9000 + whereFour + 1
    elif fullHouse:
        value = 8000 + ((whereThree + 1) * (whereTwo + 1))
    elif threeKind:
        value = 6000 + whereThree + 1
    elif twoPairs:
        value = 5000 + whereTwo + 1
    elif pair:
        value = 4000 + whereTwo + 1
    elif straight:
        value = 7000 + endStraight
    else:
        for i in range(len(amounts)):
            if amounts[i] == 1:
                value = i
    return value




def compareHands(userHand, compHand):
    userValue = handValue(userHand)
    dealerValue = handValue(compHand)

    if(userValue > dealerValue):
        #User wins
        return 1
    elif(userValue < dealerValue):
        #Computer wins
        return 2
    else:
        #Tie
        return 0


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
        parts=drawAction.split(" ")
        for i in parts[1:]:
            if i.strip().isdigit():
                cardToReplace = int(i)
                if 1 <= cardToReplace <= 5:
                    newCard = deckCard()
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

    winnerMessage = ""
    winFlag = compareHands(userHand, compHand)
    if winFlag == 0:
        winnerMessage += "Tied "
    elif winFlag == 1:
        winnerMessage += "User "
    elif winFlag == 2:
        winnerMessage += "Computer "

    winnerMessage += str(handValue(userHand)) + " " + str(handValue(compHand)) + "\n"
    connection_socket.send(winnerMessage.encode())

def serverShowHighscores(connection_socket):
    responseMessage = "EntireHighscore "
    try:
        with open("highscore.txt", "r") as x:
            lines = x.readlines()
            #skip header
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    rank, username, score = parts
                    responseMessage += f"{rank} {username} {score}\n"
    except FileNotFoundError:
        response = "Highscore file not found.\n"

    if not responseMessage:
        responseMessage = "Highscore File Empty.\n"

    connection_socket.send(responseMessage.encode())


def serverFindHighscore(connection_socket, userName):
    responseMessage = "UsernameSearch "
    flag = False #have we found the username flag
    try:
        with open("highscore.txt", "r") as x:
            lines = x.readlines()
            #skip header
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    rank, username_found, score = parts
                    if username_found.strip() == userName:
                        responseMessage += f"Rank {rank}: {username_found} - {score}\n"
                        flag = True
                        break
        if not flag:
            responseMessage += "Username not found\n"

    except FileNotFoundError:
        responseMessage += "Highscore file not found\n"

    connection_socket.send(responseMessage.encode())

def serverMain():
    server_port = 12006
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
        elif(codeWord == "ShowHighscores"):
            serverShowHighscores(connection_socket)
        elif(codeWord == "FindHighscores"):
            print("Looking for score")
            serverFindHighscore(connection_socket, userName)

        
        connection_socket.close()

serverMain()
