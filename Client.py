import socket
import os.path
import platform
import threading
from datetime import datetime, date, time

version = "P2P-CI/1.0"


class RFC:
	def __init__(self, rfc_number, rfc_title, rfc_file_location):
		self.number = rfc_number
		self.title = rfc_title
		self.file_location = rfc_file_location


def addRFCMessage(rfc, hostname, port_number):
	retMsg = "ADD RFC " + str(rfc.number) + " " + version + "\n"
	retMsg += "Host: " + hostname + "\n"
	retMsg += "Port: " + str(port_number) + "\n"
	retMsg += "Title: " + str(rfc.title) + "\n"
	return retMsg


def listAllMessage(hostname, port_number):
	retMsg = "LIST ALL " + version + "\n"
	retMsg += "Host: " + hostname + "\n"
	retMsg += "Port: " + str(port_number) + "\n"
	return retMsg


def lookupRFCMessage(rfcNumber, rfcTitle, hostname, port_number):
	retMsg = "LOOKUP RFC " + str(rfcNumber) + " " + version + "\n"
	retMsg += "Host: " + hostname + "\n"
	retMsg += "Port: " + str(port_number) + "\n"
	retMsg += "Title: " + rfcTitle + "\n"
	return retMsg


def downloadRFCMessage(rfcNumber, host_name):
	retMsg = "GET " + rfcNumber + " " + version + "\n"
	retMsg += "Host: " + host_name + "\n"
	retMsg += "OS: " + platform.system() + " " + platform.release() + " " + platform.version() + "\n"
	return retMsg

def handle_peer_request(peer_sock):
	request = peer_sock.recv(1024)
	request = request.decode("utf-8")
	print(request)
	request = request.split('\n')
	splitValue = request[0].split(" ")
	method = splitValue[0]
	rfcNumber = " ".join(splitValue[1:-1])
	ver = splitValue[-1]
	requestedHostname = request[1].split(" ")[1]

	if method != "GET":
		print("400 Bad Request")
		msg = responseHeader("400 Bad Request")
		peer_sock.send(bytearray(msg, "utf8"))
		# peer_sock.send(bytearray("\nEND\n", "utf8"))
		peer_sock.close()
		return
	elif ver != version:
		print("505 P2P-CI Version Not Supported")
		msg = responseHeader("505 P2P-CI Version Not Supported")
		peer_sock.send(bytearray(msg, "utf8"))
		# peer_sock.send(bytearray("\nEND\n", "utf8"))
		peer_sock.close()
		return
	elif requestedHostname != hostname:
		print("400 Bad Request")
		msg = responseHeader("400 Bad Request")
		peer_sock.send(bytearray(msg, "utf8"))
		# peer_sock.send(bytearray("\nEND\n", "utf8"))
		peer_sock.close()
		return

	for singleRFC in rfc_list:
		print(str(singleRFC.number) + " find-> " + str(rfcNumber))
		if str(rfcNumber) == str(singleRFC.number):
# 			Send Data to server
			print("200 OK")
			msg = responseHeader("200 OK")
			# peer_sock.send(bytearray(msg, "utf8"))

			msg += responseData(singleRFC.file_location)
			peer_sock.send(bytearray(msg, "utf8"))

			# peer_sock.send(bytearray("\nEND\n", "utf8"))
			peer_sock.close()
			return

	msg = responseHeader("404 Not Found")
	peer_sock.send(bytearray(msg, "utf8"))
	# peer_sock.send(bytearray("\nEND\n", "utf8"))
	print("Peer Close")
	peer_sock.close()

def responseHeader(status):
	retMsg =  version + " " + status + "\n"
	retMsg += "Date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT") + "\n"
	retMsg += "OS: " + platform.system() + " " + platform.release() + " " + platform.version() + "\n"
	return retMsg

def responseData(fileName):
	file = open(fileName, 'r')
	fileStat = os.stat(fileName)

	retMsg = ""
	filemodified = datetime.utcfromtimestamp(fileStat.st_mtime)
	retMsg += "Last-Modified: " + str(filemodified.strftime("%a, %d %b %Y %H:%M:%S GMT")) + "\n"
	retMsg += "Content-Length: " + str(fileStat.st_size) + "\n"
	retMsg += "Content-Type: text/plain" + "\n"
	retMsg += file.read()
	return retMsg


class UploadPeer(threading.Thread):

	def __init__(self, hostname, portNumber):
		super().__init__(name="random name")
		self.hostname = hostname
		self.portNumber = int(portNumber)

	def run(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.hostname, self.portNumber))
		server.listen(5)

		while True:
			client_sock, address = server.accept()
			client_handler = threading.Thread(
				target=handle_peer_request,
				args=(client_sock,)
			)
			client_handler.start()



# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = input("Enter Hostname ")
port_number = input("Enter Port number ")

num_of_rfc = int(input("Enter Number for RFCs "))
rfc_list = []
i = 0
while i < num_of_rfc:
	temp_rfc = RFC(input("Enter RFC Number "), input("Enter RFC title "), input("Enter Location of file "))
	if not os.path.isfile(temp_rfc.file_location):
		print("File does not exists. Please Re-enter details ")
	else:
		rfc_list.append(temp_rfc)
		i += 1

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 7734))

# send initial hostname and portNumber
data = "Connect: hostname:" + hostname + " portNumber:" + str(port_number) + "\n"
data = bytearray(data, 'utf8')
client.send(data)

for rfc in rfc_list:
	data = bytearray(addRFCMessage(rfc, hostname, port_number), 'utf8')
	client.send(data)

# receive the response data (4096 is recommended buffer size)
# response = client.recv(4096)
# print(response)
u = UploadPeer(hostname, port_number)
u.daemon = True
u.start()

while True:
	inp = input(
		'Accpeted Commands are "ADD" to add a locally available RFC to the servers index,\n"LOOKUP" to find peers that have the specified RFC\n"LIST" to request the whole index of RFCs from the server,\n"DOWNLOAD" to download RFC from peer\n and "EXIT" to exit\n')
	if inp == "ADD":
		temp_rfc = RFC(input("Enter RFC Number "), input("Enter RFC title "), input("Enter Location of file "))
		if not os.path.isfile(temp_rfc.file_location):
			print("File does not exists ")
		else:
			rfc_list.append(temp_rfc)
			data = bytearray(addRFCMessage(temp_rfc, hostname, port_number), 'utf8')
			client.send(data)
	elif inp == "LOOKUP":
		data = bytearray(lookupRFCMessage(input("Enter RFC Number "), input("Enter RFC Title "), hostname, port_number),
						 'utf8')
		client.send(data)
	elif inp == "LIST":
		data = bytearray(listAllMessage(hostname, port_number), 'utf8')
		client.send(data)
	elif inp == "DOWNLOAD":
		rfcNumber = input("Enter RFC number to be downloaded ")
		hostname = input("Enter hostname from which to download the RFC ")
		portNumber = int(input("Enter port number of the peer "))
		peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		peerSocket.connect((hostname, portNumber))
		data = bytearray(downloadRFCMessage(rfcNumber, hostname), 'utf8')
		peerSocket.send(data)

		request = peerSocket.recv(1024)
		request = request.decode("utf-8")
		print(request)
		peerSocket.close()

	elif inp == "EXIT":
		client.close()
		break
