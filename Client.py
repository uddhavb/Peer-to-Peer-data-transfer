import socket
import os.path

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
	retMsg += "Title: " + str(rfc.title)
	return retMsg

def listAllMessage(hostname, port_number):
	retMsg = "LIST ALL " + version + "\n"
	retMsg += "Host: " + hostname + "\n"
	retMsg += "Port: " + str(port_number)
	return retMsg

def lookupRFCMessage(rfcNumber, rfcTitle, hostname, port_number):
	retMsg = "LOOKUP RFC " + str(rfcNumber) + " " + version + "\n"
	retMsg += "Host: " + hostname + "\n"
	retMsg += "Port: " + str(port_number) + "\n"
	retMsg += "Title: " + rfcTitle
	return retMsg

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = input("Enter Hostname ")
port_number = input("Enter Port number ")


num_of_rfc = input("Enter Number for RFCs ")
rfc_list = []
i = 0
while i < num_of_rfc:
	temp_rfc = RFC(input("Enter RFC Number "), raw_input("Enter RFC title "), raw_input("Enter Location of file "))
	if not os.path.isfile(temp_rfc.file_location):
		print("File does not exists. Please Re-enter details ")
	else:
		rfc_list.append(temp_rfc)
		i += 1

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 7734))

# send initial hostname and portNumber
data = "Connect: hostname:" + hostname + " portNumber:" + str(port_number)
data = bytearray(data, 'utf8')
client.send(data)

for rfc in rfc_list:
	data = bytearray(addRFCMessage(rfc, hostname, port_number), 'utf8')
	client.send(data)

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)
print(response)

while True:
	inp = input('Accpeted Commands are "ADD", "LOOKUP", "LIST", "DOWNLOAD" and "EXIT"')
