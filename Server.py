import socket
import threading


peers = {}
# peers = {hostname: port_number}

RFCs = []
# RFCs = [[rfc_number ,rfc_title, hostname]]

bind_ip = '127.0.0.1'
bind_port = 7734

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))

def addToPeerList(hostname, port_number):
    print("Add host to list")
    peers[hostname] = port_number

def removeFromPeerList(hostname):
    print("Remove host from list")
    del peers[hostname]

def addToIndex(rfc_number, hostname, rfc_title):
    print("Adding")
    RFCs.append([rfc_number, rfc_title, hostname])

def lookup(rfc_number):
    print("lookup")
    for RFC in RFCs:
        if RFC[0] == rfc_number:
            print(RFC[2], end="\t")

def list():
    print("list all RFCs")
    for RFC in RFCs:
        print(RFC)

def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print("-------------------------------------")
    print(type(request))
    print('Received {}'.format(request))
    print("-------------------------------------")
    client_socket.send(bytearray('ACK!', 'utf8'))
    client_socket.close()


while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
        )
    client_handler.start()

# peerList = LinkedList();
# peerList.head = PeerNode("Random Hostname", 1234)
# one = PeerNode("Ra Hostname", 5678)
# two = PeerNode("Random Host", 1234)
# three = PeerNode("Ratname", 983247)
#
# peerList.head.next = one
# one.next = two
# two.next = three
#
# peerList.printList()
# print "After Deleting"
# peerList.removeHostName("Ratname")
# peerList.printList()

# rfcList = LinkedList();
# rfcList.head = RFCNode(1, "RFC Title 1", "Random Hostname")
# a = RFCNode(1, "RFC Title 2", "Ra Hostname")
# b = RFCNode(1, "RFC Title 3", "Random Host")
# c = RFCNode(1, "RFC Title 4", "Ratname")
#
# rfcList.head.next = a
# a.next = b
# b.next = c
#
# rfcList.printList()
# print "After Deleting"
# rfcList.removeHostName("Ra Hostname")
# rfcList.printList()
