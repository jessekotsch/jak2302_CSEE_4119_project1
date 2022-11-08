#!/usr/bin/python3.10
#jak2302

import sys
from socket import *
import time
import xml.etree.ElementTree as ET


class Proxy:

	def __init__(self, listenPort, fakeIP, webserverIP):
		self.listenPort = listenPort
		self.fakeIP = fakeIP
		self.webserverIP = webserverIP

	def bitrate_select(self, T_curr, availible_bitrates):
		"""
		This function calculates the throughput of a single chunk
		Inputs:
			T_curr (int)               : current EWMA Threshold
			availible_bitrates [list]  : availible bitrates found from parsing minifest file
		Outputs:
			bitrate (str)  : chosen bitrate (A connections can support a bitrate if the average throughput is at least 1.5x the bitrate)
        
		"""
		###TO DO
		bitrate = 45514
    
		return bitrate


	def bitrate_search(self, manifest):
		"""
		This function parses the manifest (mpd) file requested at the beginning of the stream for available bitrates
		(noted as bandwidths in the file"
		Inputs:
			manifest (str) : .mdp file requested at the beginning of the stream (encoded in XML). Used to extract possible bitrates. 
		Outputs:
			availible_bitrates [list]  : availible bitrates found from parsing minifest file

		"""

		availible_bitrates = []

		print("Found!")
		root = ET.fromstring(str(manifest.decode()))
		#for child in root: 
			#print(child.tag, child.attrib)

    
		return availible_bitrates



	def throughput_calc(self, beta, ftime, stime):
		"""
		This function calculates the throughput of a single chunk
		Inputs:
			beta  : size of chunk (bits)
			ftime : time when full chunk has been recieved 
			stime : time of chunk request 
		Outputs:
			throughput : how much data is processed in a given time window
		"""
		throughput = beta/(ftime - stime)
		return throughput



	def ewma_calc(self, T_curr, alpha, T_new):
		"""
		This functions calcualtes the exponentially-weighted moving average (EWMA)
		Inputs:
			T_curr : current EWMA Threshold
			alpha  : constant 0 ≤ α ≤ 1 controls the tradeoff between a smooth throughput estimate (α closer to 0) and one that reacts quickly to changes (α closer to 1)
			T_new  : latest threshold calculation

		Output :
			newT_curr : new current EWMA Threshold
		"""

		newT_curr = alpha*T_new + (1-alpha)*T_curr

		return newT_curr

	def parse_header(self, HTTP_mesaage):
		"""
		This functions takes in an HTTP  message and seperates the
		body from the header
		Inputs:
			HTTP_mesaage (str) : HTTP message as string
		Outputs:

		"""

		split = HTTP_mesaage.split("\\r\\n\\r\\n\\")

		header = split[0].split("\r\n")
		
		

		print("HEADER")
		print(len(header))

		
		

	def find_content_length(self, response):
		"""
		This functions parses the HTTP response for the content length 
		Inputs:
			response (str) : HTTP repsonse message

		Output :
			content_length (int) : content length of message
		"""
		start = 'Content-Length:'
		end = 'Content-Range'
		
		temp = ((response.split(start))[1].split(end)[0])
		content_length = temp.split('\n')
		print(len(content_length))
		return content_length


###############################################
###############################################
###############################################
###############################################
## PROXY CODE
###############################################
###############################################
###############################################
###############################################

if __name__ == '__main__':

	#Inputs: <listen-port> <fake-ip> <server-ip>
	listenPort = int(sys.argv[1])
	fakeIP = sys.argv[2]
	webserverIP = sys.argv[3]
	bufferSize = 4096

	beta = 1
	alpha = 1
	T_curr = 45514


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

			stime = time.time() #Start by saving time of chunk request
			print("##########################")
			print("##########################")
			print("CLIENT REQUEST MESSAGE. Time =" +str(stime))
			str_message = message.decode()
			print(message.decode())
			print("##########################")
			print("##########################")

			print("Parsing GET Request")
			fields = str_message.split("\r\n")
			url = fields[0] # GET / HTTP/1.1
			print(url)

			# Forward request to server
			WebServerSideSocket.send(message)
			print("Message forwarded to web server")
		
			# Accept request from server

			response = WebServerSideSocket.recv(bufferSize)

			Proxy(listenPort, fakeIP, webserverIP).parse_header(str(response))

			#content_lingth = Proxy(listenPort, fakeIP, webserverIP).find_content_length(str(response))

			ftime = time.time()

			"""

			if 'Partial Content' in str(response):

				content_lingth = Proxy(listenPort, fakeIP, webserverIP).find_content_length(str(response))
				print("CONTENT LENGTH")
				print(content_lingth)

			
			
				while True:
					# print("Adding Partial Content together")
					try: 
						partial_response = WebServerSideSocket.recv(bufferSize)
						response += partial_response
						#print("############")
						#print(str(partial_response))
					except:
						break
					
			"""
			
			availible_bitrates = [45514,176827,506300,1006743] ###~!!! NEED TO CHANGE
			print("Message Received")
			# At beginning search minifest file for availible bitrates
			if 'mpd' in str(response):
				print("Parsing Manifest")
				availible_bitrates = [45514,176827,506300,1006743] ###~!!! NEED TO CHANGE 
				#availible_bitrates = Proxy(listenPort, fakeIP, webserverIP).bitrate_search(response)

				# Initialize current bitrate to lowest bitrate 
				bitrate = min(availible_bitrates)
				T_curr = bitrate
			else:
				print("Calculating Throughput")
				T_new = Proxy(listenPort, fakeIP, webserverIP).throughput_calc(beta, ftime, stime)
				T_curr = Proxy(listenPort, fakeIP, webserverIP).ewma_calc(T_curr, alpha, T_new)
				bitrate = Proxy(listenPort, fakeIP, webserverIP).bitrate_select(T_curr, availible_bitrates)
			
			

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

