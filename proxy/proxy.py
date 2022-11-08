#!/usr/bin/python3.10
#jak2302

import sys
from socket import *
import time
import xml.etree.ElementTree as ET


class Proxy:

	def __init__(self, identifier):
		self.identifier = identifier


	def bitrate_select(self, T_curr, bitrate, availible_bitrates):
		"""
		This function calculates the throughput of a single chunk
		Inputs:
			T_curr (int)               : current EWMA Threshold
			availible_bitrates [list]  : availible bitrates found from parsing minifest file
		Outputs:
			bitrate (str)  : chosen bitrate (A connections can support a bitrate if the average throughput is at least 1.5x the bitrate)
        
		"""
		###Make sure they are in decending order since we want the fastets rate it can support
		
		availible_bitrates.sort(reverse = True)


		for rate in availible_bitrates:
			if T_curr/rate >= 1.5:
				bitrate = rate
				break
			else:
				bitrate = min(availible_bitrates)

    
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

		for element in manifest:
			if "bandwidth" in element:
				new_elements = element.split(" ")
				for temp in new_elements:
					if "bandwidth" in temp:
						new_temp = temp.split('"')
						availible_bitrates.append(int(new_temp[1]))


		print("Available Bitrates", availible_bitrates)
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
			header (list)                  : list of seperated header elements
			body (str)                     : body content
		"""

		#split = HTTP_mesaage.split("\\r\\n\\r\\n\\")

		content_list = HTTP_mesaage.split("\\r\\n")

		header = content_list[:-1]

		body = content_list[-1]
		
		return header, body

		
		

	def find_content_length(self, header):
		"""
		This functions parses the HTTP response for the content length 
		Inputs:
			header (list) : HTTP repsonse header split into list by element

		Output :
			content_length (int)     : content length of message
			partial_flag   (boolean) : partial content flag
		"""

		partial_flag = False
		content_length = 0

		for element in header:
			if "Content-Length:" in element:
				content_length = element.split(" ")[1]
			if "Partial Content" in element:
				partial_flag = True

		return int(content_length), partial_flag

	def edit_client_request_message(self, message, bitrate):
		"""
		This process accepts a client request message and edits the bitrate if necessary
		Inputs:
			message : HTTP message
			bitrate(int) : desired bitrate
		Output:
			new_message : edited HTTP message
			mpd_flag    : indicates if mpd file was requested
			new_url     : new chunk name for logging
		"""

		mpd_flag = False

		str_message = message.decode()

		fields = str_message.split("\r\n")
		url = fields[0] # GET / HTTP/1.1

		# Return nolist files so requested bandwidth will always be 1000
		if 'mpd' in url:
			mpd_flag = True
			new_message = str_message.replace("BigBuckBunny_6s.mpd", "BigBuckBunny_6s_nolist.mpd")
			new_url = url.replace("BigBuckBunny_6s.mpd", "BigBuckBunny_6s_nolist.mpd")
		elif "BigBuckBunny" in url:
			new_message = str_message.replace("1000bps", str(bitrate)+'bps')
			new_url = url.replace("1000bps", str(bitrate)+'bps')
		else:
			new_message = str_message
			new_url = url

		return new_message.encode(), mpd_flag, new_url

	def log_data(self, filename, stime, ftime, T_new, T_curr, bitrate, webserverIP, chunkname):
		"""
		This process is responsible for logging important information into
		the file name provided in the command line. The data is formatted as such:

        <time> <duration> <tput> <avg-tput> <bitrate> <server-ip> <chunkname>

		time: The current time in seconds since the epoch.

		duration: A floating point number representing the number of seconds it took to download this chunk from the server to the proxy.

		tput: The throughput you measured for the current link in Kbps.

		avg-tput: Your current EWMA throughput estimate in Kbps.

		actual bitrate: The actual bitrate your proxy requested for this chunk in Kbps (NOT LABELED).

		server-ip: The IP address of the server to which the proxy forwarded this request

		chunkname: The name of the file your proxy requested from the server (that is, the modified file name in the modified HTTP GET message).
		"""

		ctime = time.time()
		duration = ftime - stime
		print("HERE5")
		chunkname.replace('GET', '')
		chunkname.replace('HTTP/1.1', '')
		print("HERE4")
		log = ctime, duration, T_new, T_curr, bitrate, webserverIP, chunkname
		print("HERE")
		f = open(filename, "a")
		print("HERE1")
		f.write(log)
		f.close()

		print("<time> <duration> <tput> <avg-tput> <bitrate> <server-ip> <chunkname>")
		print(log)

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

	#Inputs: <filename> <alpha> <listen-port> <fake-ip> <server-ip>
	filename = str(sys.argv[1])
	alpha = float(sys.argv[2])
	listenPort = int(sys.argv[3])
	fakeIP = sys.argv[4]
	webserverIP = sys.argv[5]

	bufferSize = 4096
 
	T_curr  = 45514
	T_new   = 45514
	bitrate = 45514
	availible_bitrates = None


	# Bind and listen on client side

	ClientSideSocket = socket(AF_INET, SOCK_STREAM)
	ClientSideSocket.bind(('', listenPort))
	ClientSideSocket.listen(10)

	print("Listening on port: " + str(listenPort))

	# Create socket on  web server side and try and connect
	WebServerSideSocket = socket(AF_INET, SOCK_STREAM)
	WebServerSideSocket.bind((fakeIP, 0))
	WebServerSideSocket.connect((webserverIP,8080))


	# Accept request from client
	#connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET

	while True: 

		try:
			# Accept request from client
			connectionSocket, addr = ClientSideSocket.accept() ## RETURNS CONNECTION SOCKET

			message = connectionSocket.recv(bufferSize)
			stime = time.time() #Start by saving time of chunk request

			new_message, mpd_flag, chunkname = Proxy(0).edit_client_request_message(message, bitrate)

			if mpd_flag:
				
				# send request for manifest will all bitrates
				WebServerSideSocket.send(message)
				manifest = WebServerSideSocket.recv(bufferSize)
				manifest_header, manifest_body = Proxy(0).parse_header(str(manifest))


			# Forward request to server

			WebServerSideSocket.send(new_message)
		
			# Accept request from server

			response = WebServerSideSocket.recv(bufferSize)


			header, body = Proxy(0).parse_header(str(response))
			content_length, partial_flag = Proxy(0).find_content_length(header)


			if (content_length > bufferSize):
				total_received = len(body)
				while True:
					temp_response = WebServerSideSocket.recv(bufferSize)
					total_received += len(temp_response)
					response += temp_response
					if len(temp_response) < bufferSize: break



			ftime = time.time()
	
		
			# At beginning search minifest file for availible bitrates 
			if mpd_flag:
				availible_bitrates = Proxy(0).bitrate_search(manifest_header)

				# Initialize current bitrate to lowest bitrate 
				bitrate = min(availible_bitrates)
				T_curr  = bitrate
				T_new   = T_curr
			elif availible_bitrates == None:
				pass
			else:
				T_new = Proxy(0).throughput_calc(content_length, ftime, stime)
				T_curr = Proxy(0).ewma_calc(T_curr, alpha, T_new)
				bitrate = Proxy(0).bitrate_select(T_curr, bitrate, availible_bitrates)
			
			

			# Send Response Back to Client
			connectionSocket.send(response)
			print("WHAT")
			Proxy(0).log_data(stime, filename, ftime, T_new, T_curr, bitrate, webserverIP, chunkname)


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

