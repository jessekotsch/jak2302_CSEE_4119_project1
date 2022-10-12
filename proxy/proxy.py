#jak2302

import sys
from socket import *



#Make Input later <listen-port> <fake-ip> <server-ip>
listenPort = int(sys.argv[1])
clientIP = sys.argv[2]
serverIP = sys.argv[3]

serverPort = 8080

bufferSize = 8



# Step a:
# Establish connection with a client
# 1. Your proxy should listen for connnections from a client on any IP address on the port
# specified as a command line argument.
	#a. connect client (TCP)

ClientSideSocket = socket(AF_INET, SOCK_STREAM)

	#b. bind and listen for message


ClientSideSocket.bind((clientIP, listenPort))
ClientSideSocket.listen(1)

print("Accepting client side socket message...")
connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET


print("Ready to recieve message")
message = connectionSocket.recv(bufferSize) 
print("Message Received...")
print(message)


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

# Repeat until connection needs to be closed
while True:


	fullMessage = bytearray()


	print("Ready to recieve message")
	receivingMessage = True 
	message = connectionSocket.recv(bufferSize)
	 

	print("Message Received...")
	print(message)
	

    #b. send received message from client
	print("Sending Message...")
	try:
		ServerSideSocket.send(message)
	except:
		print("No Server Connection")
		break



    
print("Closing connection socket")
connectionSocket.close()
#close socket connection
print("Closing Server Side Socket...")
ServerSideSocket.close()



# 2. Your proxy should accept multiple connections from clients (one-by-one)
# 4. The server IP is provided as a command line argument
# 5. As for the port number, use 8080. 
# 6. Make sure to close connections to the client and server when either of them disconnects. 




