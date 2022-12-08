# UDP Socket Client
# Group Name: G29
# Group Members: Willem Van Dam, Liam Foster

from socket import *
import time

# Define Constants
receiveTimeout = 1 #s
numPackets = 5 # Number of packets sent

# Set Up Local Host connection as client (based off of template in CPEN333 lecture slides)
serverName = "localhost"
serverPort=12000
clientSocket=socket(AF_INET,SOCK_DGRAM) # setup as UDP socket protocol
clientSocket.settimeout(receiveTimeout) # set timeout of socket commands to 1s

# Send numPackets amount of packets to the server
for packetNum in range(numPackets):
    message = f"PING {packetNum+1} - hello world" # message to send
    clientSocket.sendto(message.encode(),(serverName,serverPort)) # encode and send the message to the server (based off of template in CPEN 333 lecture slides)
    packetSentTime = time.time() # store the time that the packet was sent
    # try block to deal with timout if packet is dropped
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(32) # receive message (based off of template in CPEN 333 lecture slides)
        rtt = round((time.time() - packetSentTime)*1000,3) # calculate RTT in ms and round to nearest us
        print(modifiedMessage.decode(), ": time = ", rtt, "ms") # print received message and RTT
    except:
        print(f"Request for packet {packetNum+1} timed out") # Timeout error message if packet was dropped
clientSocket.close() # Close socket
