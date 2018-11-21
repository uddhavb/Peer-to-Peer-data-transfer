import socket

hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
target = '{}.{}.{}'.format(hostname, sld, tld)

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = input("Enter Hostname ")
port_number = input("Enter Port number ")

num_of_rfc = int(input("Enter Number for RFCs"))
rfc_list = []
for i in range(0, num_of_rfc):
    rfc_name = input("Enter RFC name ")
    rfc_list.append(rfc_name)

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 7734))

# send some data (in this case a HTTP GET request)
data = "GET /index.html HTTP/1.1\r\nHost: {}.{}\r\n\r\n".format(sld, tld)
data = bytearray(data, 'utf8')
client.send(data)

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print(response)
