# client server V0.1
# Hefelc
# 11/13/2025
# Setting up basic framework

from socket import *
from _thread import *
from random import *

def start_new_game(client_socket):

def view_scoreboard(client_socket):

def view_rules(client_socket):
    
def view_card_values(client_socket):

def exit_program(client_socket):

def client_main():
    server_IP = '127.0.0.1'
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_IP, server_port))

    print("--Welcome To Planet Poker--")
    print("Select an Option")
    print ("1 - play new game")
    print ("2 - view scoreboard")
    print ("3 - view rules")
    print ("4 - view card values")
    print ("5 - quit")

    choice = input("Enter command: ")

    if choice == '1':
        start_new_game(client_socket)
    elif choice == '2':
        view_scoreboard(client_scoket)
    elif choice == '3':
        view_rules(client_socket)
    elif choice == '4':
        view_card_values(client_socket)
    elif choice == '5':
        exit_program(client_socket)

    else:
        print("Invalid Input... try again!")

    client_socket.close()


client_main()
