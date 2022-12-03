from socket import *
import random
import time

# Set Up Local Host connection as server
serverName = "localhost"
serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print("The server is ready to receive")

while True:
    # Recieve message
    message, clientAddress = serverSocket.recvfrom(2048)
    # Generate random 10% chance that message is lost
    if ( 10%10 != 0):
        # Delay for random time between 5ms-50ms
        time.sleep(round(random.uniform(.005, .05), 3))
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    