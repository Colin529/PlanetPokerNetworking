# client server V1.0
# Hefelc
# 11/27/2025
# Setting up gameflow. Some game logic is being moved to server side

from socket import *
from _thread import *
from random import *

def start_new_game(client_socket):
    userName = input("Enter Username: ")
    playingMessage = "PlayGame " + userName + " \n"
    client_socket.send(playingMessage.encode())
    gameResponse = client_socket.recv(1024).decode()
    if "Welcome" in gameResponse:
        gameTime = True
        highestChips = 20
        while gameTime:
            #Start the game
            #print("**\n")
            dealtHandMessage = client_socket.recv(1024).decode()
            #print("Is it you?\n")
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
                parts = newHand.strip().split(" ")
                userHand = " ".join(parts[1:])
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
                checkMessage = "Check "
                client_socket.send(checkMessage.encode())

            newBet = client_socket.recv(1024).decode()
            if newBet.startswith("BetRaised "):
                parts = newBet.strip().split(" ")
                userChips = parts[1]
                currPool = parts[2]
                print("User Chips = " + str(userChips))
                print("Current Pool = " + str(currPool))
            elif newBet.startswith("CheckOK"):
                print("User Checked")


             #Play or Fold
            timeToPlayHand = input("Play Cards or Fold? (1 to play, 2 to fold)")
            while True:
                if timeToPlayHand == "1":
                    playTime = "PlayingHand"
                    break
                elif timeToPlayHand == "2":
                    playTime = "Fold"
                    break
                else:
                    print("Invaild. Please try again.")
                    timeToPlayHand = input("(1 to play, 2 to fold)")
            client_socket.send(playTime.encode())    
            
            winner = client_socket.recv(1024).decode()
            if winner.startswith("User"):
                print(winner)
                userChips = int(userChips) + (2 * int(currPool))
                if int(userChips) > int(highestChips):
                    highestChips = int(userChips)
            elif winner.startswith("Computer"):
                print(winner)
                #userChips = int(userChips) - int(currPool)
            else:
                print("Tie")



            if int(userChips) <= 0:
                #Game end
                print("Game Over.\n")
                print("Thank you for playing.\n")
                with open("highscore.txt", "a") as bread:
                    bread.write(userName + "," + str(highestChips) + "\n")
                bread.close()
                gameTime = False
                stopper = "Stop"
                client_socket.send(stopper.encode())
                break
            
            cont = input("Another round? (y/n)\n")
            if cont.lower() == "y":
                #Continue on.
                print("Good Luck.")
                poll = "Keep going"
                client_socket.send(poll.encode())

            elif cont.lower() =="n":
                #Quiting
                print("Thank you for playing.\n")
                with open("highscore.txt", "a") as bread:
                    bread.write(userName + "," + str(highestChips) + "\n")
                bread.close()
                gameTime = False
                stopper = "Stop"
                client_socket.send(stopper.encode())


    else:
        print(f"ERROR: Message in unexpected format. Message: '{gameResponse}'")
        return -1


def view_scoreboard(client_socket):
    highscoreMessage = ""
    while(True):
        highscores_action = input("1 - View All Highscores\n"
                                "2 - Search For Username in Highscores\n"
                                "Enter Command:")
        if highscores_action == "1":
            highscoreMessage = "ShowHighscores \n"
            break
        elif highscores_action == "2":
            username_search = input("Enter a username to search: ")
            highscoreMessage = "FindHighscores " + username_search + " \n"
            break
        else:
            print("INVALID INPUT")
            break

    client_socket.send(highscoreMessage.encode())
    highscoreResponse = client_socket.recv(1024).decode()

    #response if wanting entire highscore file
    if highscoreResponse.startswith("EntireHighscore "):
        removeHeader = highscoreResponse.replace("EntireHighscore ", "")
        rows = removeHeader.split("\n")
        for x in rows:
            if not x.strip():
                continue

            parts = x.split(" ")
            #rank = parts[0]
            username = parts[0]
            score = parts[1]
            print(f"{username} -- score: {score}")


    elif highscoreResponse.startswith("UsernameSearch "):
        print(highscoreResponse)

def view_rules(client_socket):
    #client_socket.send("Chill Out".encode())
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
    #con = client_socket.recv(1024).decode()
    #client_main()
    
def view_card_values(client_socket):
    #client_socket.send("Chill Out".encode())
    print("Each card has a value like Poker cards.")
    print("Jupiter - 8 points")
    print("Saturn - 7 points")
    print("Uranus - 6 points")
    print("Neptune - 5 points")
    print("Earth - 4 points")
    print("Venus - 3 points")
    print("Mars - 2 points")
    print("Mercury - 1 points")
    #con = client_socket.recv(1024).decode()
    #client_main()

def client_main():
    server_IP = 'localhost'
    server_port = 12006
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_IP, server_port))
    while True:
        print("Welcome to Planet Poker! Select your choice!")
        print("1 - Play Planet Poker.")
        print("2 - Look up rules.")
        print("3 - Look up card values.")
        print("4 - Look up highest score.")
        print("Q - Exit the application.")

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
