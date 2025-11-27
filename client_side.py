# client server V1.0
# Hefelc
# 11/27/2025
# Setting up gameflow. Some game logic is being moved to server side

from socket import *
from _thread import *
from random import *

def start_new_game(client_socket):
    userName = input("What is your user name? ")
    playingMessage = "PlayGame " + userName + " \n"
    client_socket.send(playingMessage.encode())
    gameResponse = client_socket.recv(1024).decode()
    if "Welcome" in gameResponse:
        gameTime = True
        if gameTime:
            #Start the game
            dealtHandMessage = client_socket.recv(1024).decode()
            if dealtHandMessage.startswith(userName):

                #check to make sure the full message reached the client
                try:
                    parts = dealtHandMessage.split(" ")

                    if len(parts) < 12:
                        raise ValueError("Message was malformed or incomplete.")

                    userHand = " ".join(parts[1:6])
                    userChips = int(parts[6].strip())
                    compHand = " ".join(parts[7:12])

                    currPool = 1 #current pool will always start at 1, taken at the server side

                except(IndexError, ValueError) as e:
                    print("ERROR: Failed to parse message")
                    print(f"Received message: '{dealtHandMessage}'")
                    return -1

            else:
                print(f"ERROR: Message in unexpected format. Message: '{dealtHandMessage}'")
                return -1

        print("Current Prize Pool = " + str(currPool))
        print("User Chips = " + str(userChips) + "\n\n")
        print("Users Hand:\n" + userHand + "\n")

        #Redraw Cards Logic
        userReplaceCards = input("Would you like to replace any of your cards? (y/n)")
        if userReplaceCards.lower() == "y":
            print("Current User Hand:\n" + userHand)
            replaceCards = input("Which cards would you like to replace? (ex. 1 2 3 or 4 5)").strip()
            redrawCardsMessage = "RedrawCards " + replaceCards + " \n"
            client_socket.send(redrawCardsMessage.encode())

        else:
            drawDeclineMessage = "DrawDecline"
            client_socket.send(drawDeclineMessage.encode())

        newHand = client_socket.recv(1024).decode()
        if newHand.startswith("RedealtCards"):
            userHand = newHand.strip(" ")[1]
            print("Users New Hand")
            print(userHand)
        elif newHand.startswith("DrawDeclinedOK"):
            print("User Declined Draw")


        #Bet logic
        userRaiseBet = input("Would you like to raise your bet? (y/n)")
        if userRaiseBet.lower() == "y":
            raiseAmount = input(f"How many chips would you like to raise? Current Amount: '{userChips}': ")
            if int(raiseAmount) <= userChips:
                raiseBetMessage = "RaiseBet " + raiseAmount + " \n"
                client_socket.send(raiseBetMessage.encode())
            elif int(raiseAmount) > userChips:
                print("ERROR: Amount cannot be greater than your chips")
                return -1
        elif userRaiseBet.lower() == "n":
            checkMessage = "check"
            client_socket.send(checkMessage.encode())

        newBet = client_socket.recv(1024).decode()
        if newBet.startswith("BetRaised "):
            userChips = newBet.strip(" ")[1]
            currPool = newBet.strip(" ")[2]
            print("User Chips = " + str(userChips))
            print("Current Pool = " + str(currPool))
        elif newBet.startswith("CheckOK"):
            print("User Checked")

    else:
        print(f"ERROR: Message in unexpected format. Message: '{gameResponse}'")
        return -1


def view_scoreboard(client_socket):
    print("NULL")
def view_rules(client_socket):
    print("The player and bot will both draw five random cards.")
    print("The winner is decided by who has the most points.")
    print("Points are gained by cards and the pattern they appear in.")
    print("Patterns by most points to least points:")
    print("1st - Five of a Kind.")
    print("2nd - Four of a Kind.")
    print("3rd - Full House.")
    print("4th - Straight.")
    print("5th - Three of a Kind.")
    print("6th - Two Pairs.")
    print("7th - One Pair.")
    print("8th - No Pair.")
    client_main()
    
def view_card_values():
    print("Each card has a value like Poker cards.")
    print("Jupiter - 8 points")
    print("Saturn - 7 points")
    print("Uranus - 6 points")
    print("Neptune - 5 points")
    print("Earth - 4 points")
    print("Venus - 3 points")
    print("Mars - 2 points")
    print("Mercury - 1 points")
    client_main()

def client_main():
    server_IP = 'localhost'
    server_port = 12002
    while True:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_IP, server_port))

        print("Welcome to Planet Poker! Select your choice!")
        print("1 - Play Planet Poker.")
        print("2 - Look up rules.")
        print("3 - Look up card values.")
        print("4 - Look up highest score.")
        print("Other - Exit the application.")

        ##choice = input("Enter command: ")
        choice = input("Please make your choice.")
        if(choice == '1'):
            #Play Game
            start_new_game(client_socket)
        elif(choice == '2'):
            #Rules
            view_rules(client_socket)
        elif(choice == '3'):
            #Card Values
            view_card_values(client_socket)
        elif(choice == '4'):
            #Highest Score
            view_scoreboard(client_socket)
        else:
            #Exiting
            client_socket.close()
            break
        
        client_socket.close()


client_main()
