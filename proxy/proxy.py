#!/usr/bin/python3.10
#jak2302

import sys
from socket import *
import time
import xml.etree.ElementTree as ET


#Start by saving time of chunk request

#stime = time.time()
#print("start time: ", stime)

#Inputs: <listen-port> <fake-ip> <server-ip>
listenPort = int(sys.argv[1])
fakeIP = sys.argv[2]
webserverIP = sys.argv[3]
bufferSize = 4096


# Bind and listen on client side
ClientSideSocket = socket(AF_INET, SOCK_STREAM)
ClientSideSocket.bind(('', listenPort))
ClientSideSocket.listen(10)

print("Listening on port: " + str(listenPort))





while True: 

	try:
		# Create socket on  web server side and try and connect
		print("Connecting to Webserver") 
		WebServerSideSocket = socket(AF_INET, SOCK_STREAM)
		WebServerSideSocket.bind((fakeIP, 0))
		WebServerSideSocket.connect((webserverIP,8080))


		# Accept request from client
		connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET  
		message = connectionSocket.recv(bufferSize)
		print("##########################")
		print("##########################")
		print("CLIENT REQUEST MESSAGE:")
		print(message.decode())
		print("##########################")
		print("##########################")

		# Forward request to server 
		WebServerSideSocket.send(message)
		print("Message forwarded to web server")
		
		# Accept request from server
		response = WebServerSideSocket.recv(bufferSize)
		if 'mpd' in str(response):
			print("Found!")
			root = ET.fromstring(str(response.decode()))
			#for child in root: 
				#print(child.tag, child.attrib)
			"""
			print("Response Received")
			print("##########################")
			print("##########################")
			print("SERVER RESPONSE MESSAGE:")
			print(response)
			print("##########################")
			print("##########################")
			"""

		# Send Response Back to Client
		connectionSocket.send(response)
		print("Response Sent")


	except Exception as e:
		print("An Error Has Occured:")
		print(e)
		time.sleep(3)
	






























#########################
# ORIGINAL PROXY CODE
# SAVE JUST IN CASE
########################
"""
#Inputs: <listen-port> <fake-ip> <server-ip>
listenPort = int(sys.argv[1])
fakeIP = sys.argv[2]
serverIP = sys.argv[3]

bufferSize = 8



# Create client side socket, bind and listen 
print("Connecting Client")
ClientSideSocket = socket(AF_INET, SOCK_STREAM)
ClientSideSocket.bind(('', listenPort))
ClientSideSocket.listen(10)


while True:
	try:
		# Connect to server  
		print("Connecting Server")
		ServerSideSocket = socket(AF_INET, SOCK_STREAM)
		ServerSideSocket.bind((fakeIP, 0))
		ServerSideSocket.connect((serverIP,8080))
		
	except Exception as e:
		# If server is not running print error and keep tryin to connect
		print(e)
		time.sleep(3)
	else:
		# if Server connects then wait for client 
		print("Listening for Client...")
		connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET

		while True:
            
			# client has connected to wait until message is recieved 
			print("Client Connected: Ready to recieve message")
			message = connectionSocket.recv(bufferSize)
			# if the connection with the client drops before the first message is sent then close the connection and start over
			if not message:
				print("Client Connection Has Beed Lost. Closing Connections...")
				break
			else:
				print("Message Received...")
				print(message)
	

			# try sending the message to the server
			try:
				ServerSideSocket.send(message)
			except:
				# If message fails to send the server has been disconnected
				print("Server Connection Has Beed Lost. Closing Connections...")
				break


		# Close client and sever connections and restart
		print("Closing connection socket")
		connectionSocket.close()
		#close socket connection

		# Assuming socket connection never fails for preliminary stage 
		print("Closing Server Side Socket...")
		ServerSideSocket.close()



"""

