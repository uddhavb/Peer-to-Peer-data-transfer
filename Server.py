import socket
import threading

class PeerNode:
    def __init__(self, hostname=None, port_number=None):
        self.hostname = hostname
        self.port_number = port_number
        self.next = None

    def __str__(self):
        return self.hostname + " " + str(self.port_number)

class LinkedList:
    def __init__(self):
        self.head = None

    def printList(self):
        printval = self.head
        while printval is not None:
            print (printval)
            printval = printval.next

    def removeHostName(self, host_name):
        prev = None
        root = self.head
        while root is not None:
            if host_name == root.hostname:
                if prev == None:
                    self.head = self.head.next
                else:
                    prev.next = root.next

            prev = root
            root = root.next

class RFCNode:
    def __init__(self, rfc_number=None, rfc_title=None, hostname=None):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.hostname = hostname
        self.next = None

    def __str__(self):
        return str(self.rfc_number) + " " + self.rfc_title + " " + self.hostname

class RFCLinkedList:
    def __init__(self):
        self.head = None

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

bind_ip = '127.0.0.1'
bind_port = 7734

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print 'Received {}'.format(request)
    client_socket.send('ACK!')
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()

