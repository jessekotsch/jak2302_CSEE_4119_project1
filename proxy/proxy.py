#jak2302

import sys
from socket import *
import time



#Make Input later <listen-port> <fake-ip> <server-ip>
listenPort = int(sys.argv[1])
fakeIP = sys.argv[2]
serverIP = sys.argv[3]

bufferSize = 8



# Step a:
# Establish connection with a client
# 1. Your proxy should listen for connnections from a client on any IP address on the port
# specified as a command line argument.
	#a. connect client (TCP)

print("Connecting Client")
ClientSideSocket = socket(AF_INET, SOCK_STREAM)
ClientSideSocket.bind(('', listenPort))
ClientSideSocket.listen(10)


ServerSideSocket = socket(AF_INET, SOCK_STREAM)
ServerSideSocket.bind((fakeIP, 0))
#ServerSideSocket.connect((serverIP,8080))


while True:
	print("Connecting Server")
	ServerSideSocket.connect((serverIP,8080))
	print("Listening for Client...")
	connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET

	while True:


		print("Client Connected: Ready to recieve message")
		message = connectionSocket.recv(bufferSize)
		# if the connection with the client sdrops before the first message is sent then close the connection and start over
		if not message:
			print("Client Connection Has Beed Lost. Closing Connections...")
			break
		else:
			print("Message Received...")
			print(message)
	


	#b. send received message from client
			#b. send received message from client
		print("Sending Message...")
		try:
			ServerSideSocket.send(message)
		except:
			print("Server Connection Has Beed Lost. Closing Connections...")
			break


    
	print("Closing connection socket")
	connectionSocket.close()
	#close socket connection

	# Assuming socket connection never fails for preliminary stage 
	#print("Closing Server Side Socket...")
	#ServerSideSocket.close()



# 2. Your proxy should accept multiple connections from clients (one-by-one)
# 4. The server IP is provided as a command line argument
# 5. As for the port number, use 8080. 
# 6. Make sure to close connections to the client and server when either of them disconnects. 




