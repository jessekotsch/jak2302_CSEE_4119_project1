#jak2302

import sys
from socket import *



#Make Input later <listen-port> <fake-ip> <server-ip>
listenPort = int(sys.argv[1])
clientIP = sys.argv[2]
serverIP = sys.argv[3]
serverPort = sys.argv[4]




# Step a:
# Establish connection with a client
# 1. Your proxy should listen for connnections from a client on any IP address on the port
# specified as a command line argument.
	#a. connect client (TCP)

ClientSideSocket = socket(AF_INET, SOCK_STREAM)
#ClientSideSocket.connect((clientIP, clientPort))

	#b. bind and listen for message


ClientSideSocket.bind((clientIP, listenPort))
ClientSideSocket.listen(1)

# 2. Your proxy should accept multiple connections from clients (one-by-one)
#while True:
while True:
	#Receive message

	print("Accepting client side socket message...")
	connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET
 

	print("Ready to recieve message")
	message = connectionSocket.recv(2048) 
	print("Message Received...")
	print(message)
	print("Closing connection socket")
	connectionSocket.close()

# Step b
# Establish connection with a server
# 3. Once the proxy gets connected to the client, it should then connect to the server.
	#a. create a server socket (TCP) and connect to it


	print("Opening Server Side Socket...")
	ServerSideSocket = socket(AF_INET, SOCK_STREAM)
	ServerSideSocket.connect((serverIP,serverPort))

    #b. send received message from client
	print("Sending Message...")
	ServerSideSocket.send(message)

	#c. close socket connection
	print("Closing Server Side Socket...")
	ServerSideSocket.close()
    


# 2. Your proxy should accept multiple connections from clients (one-by-one)
# 4. The server IP is provided as a command line argument
# 5. As for the port number, use 8080. 
# 6. Make sure to close connections to the client and server when either of them disconnects. 




