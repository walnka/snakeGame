# UDP Socket Server
# Group Name: G29
# Group Members: Willem Van Dam, Liam Foster

from socket import *
import random
import time

# Set Up Local Host connection as server (based off of lecture notes from CPEN 333 slide)
serverName = "localhost"
serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM) # setup as UDP socket protocol
serverSocket.bind(('',serverPort))
print("The server is ready to receive")

# while the server is running wait to receive messages
while True:
    # Recieve message
    message, clientAddress = serverSocket.recvfrom(32) # receive up to 32 bytes from client (based off of lecture notes from CPEN 333 slide)
    # Generate random 10% chance that message is lost
    if ( random.randint(0,9) != 0):
        # Delay for random time between 5ms-50ms
        time.sleep(random.uniform(.005, .05))
        modifiedMessage = message.decode().replace("hello world", "ditto") # decode and replace hello world with ditto
        serverSocket.sendto(modifiedMessage.encode(), clientAddress) # encode message and send back to same client address that sent it    
