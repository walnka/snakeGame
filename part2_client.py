from socket import *
import time

# Define Constants
receiveTimeout = 1 #ms
# Set Up Local Host connection as client
serverName = "localhost"
serverPort=12000
clientSocket=socket(AF_INET,SOCK_DGRAM)


message=input("Input lowercase sentence:")
clientSocket.sendto(message.encode(),(serverName,serverPort))
packetSentTime = time.time()
while (time.time() - packetSentTime < receiveTimeout):
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
clientSocket.close()
