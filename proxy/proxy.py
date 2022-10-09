#jak2302

import sys
from socket import *

#for debug
debugcontinue = "no"


#Make Input later
clientIP = '4.0.0.1'
clientPort = 8080



# Step a:
# Establish connection with a client
# 1. Your proxy should listen for connnections from a client on any IP address on the port
# specified as a command line argument.
	#a. connect client (TCP)

ClientSideSocket = socket(AF_INET, SOCK_STREAM)
#ClientSideSocket.connect((clientIP, clientPort))

	#b. bind and listen for message

#ClientSideSocket.bind((clientIP, clientPort))

ClientSideSocket.bind(('', 11000))
ClientSideSocket.listen(1)

# 2. Your proxy should accept multiple connections from clients (one-by-one)
#while True:
while debugcontinue == "yes":
	#Receive message

    print("Accepting client side socket message...")
	connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET
	print("Message Received...")
	message = connectionSocket.recv(2048) 


# Step b
# Establish connection with a server
# 3. Once the proxy gets connected to the client, it should then connect to the server.
	#a. create a server socket (TCP) and connect to it


	print("Opening Server Side Socket...")
	ServerSocket = socket(AF_INET, SOCK_STREAM)
	ServerSideSocket.connect((serverName,serverPort))

    #b. send received message from client
    print("Sending Message...")
	connectionSocket.send(message)

	#c. close socket connection
    print("Closing Server Side Socket...")
	ServerSideSocket.close()


	debugcontinue = input("Would you like to continue (yes/no:" )
    


# 2. Your proxy should accept multiple connections from clients (one-by-one)
# 4. The server IP is provided as a command line argument
# 5. As for the port number, use 8080. 
# 6. Make sure to close connections to the client and server when either of them disconnects. 




