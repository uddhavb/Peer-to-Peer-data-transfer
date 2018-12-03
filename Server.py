import socket
import threading
import time
peers = {}
# peers = {hostname: port_number}

RFCs = []
# RFCs = [[rfc_number ,rfc_title, hostname, portnumber]]

bind_ip = input("Enter port number for Server\n NOTE: For localhost USE 127.0.0.1 ")
bind_port = 7734

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print('Listening on {}:{}'.format(bind_ip, bind_port))


def addToPeerList(hostname, port_number):
    global peers
    #print("Add host to list")
    peers[hostname] = port_number


def removeFromPeerList(hostname):
    global peers
    #print("Remove host from list")
    del peers[hostname]


def addToIndex(rfc_number, hostname, portNumber, rfc_title):
    #print("Adding")
    rfc_title = ' '.join([str(x) for x in rfc_title]).strip()
    #print("TITLE: " + rfc_title)
    RFCs.append([rfc_number.strip(), rfc_title.strip(), hostname.strip(), portNumber.strip()])


def lookup(rfc_number):
    global RFCs
    #print("lookup")
    retRFCs = []
    for RFC in RFCs:
        if RFC[0] == rfc_number:
            retRFCs.append(RFC)
    return retRFCs


def list():
    global RFCs
    #print("list all RFCs")
    list_of_rfcs = []
    for RFC in RFCs:
        list_of_rfcs.append(RFC)
    return list_of_rfcs


def handle_client_connection(client_socket):
    global peers
    global RFCs
    '''
    Connect: hostname:uddhav portNumber:1234
    ADD RFC 21 P2P-CI/1.0
    Host: uddhav
    Port: 1234
    Title: hello world
    ADD RFC 22 P2P-CI/1.0
    Host: uddhav
    Port: 1234
    Title: hola
    LOOKUP RFC 3457 P2P-CI/1.0
    Host: thishost.csc.ncsu.edu
    Port: 5678
    Title: Requirements for IPsec Remote Access Scenarios
    LIST ALL P2P-CI/1.0
    Host: thishost.csc.ncsu.edu
    Port: 5678
    '''
    try:
        while True:
            request = client_socket.recv(8192)
            request = request.decode("utf-8")
            originalRequest = request
            request = request.split('\n')
            index = 0
            while request[index] != [] and index < len(request):
                line = request[index]
                line = line.split()
                request[index] = line
                if line == []:
                    time.sleep(1)
                elif line[0] == "Connect:":
                    addToPeerList(line[1].split(':')[1], line[2].split(':')[1])
                    exit_host = line[1].split(':')[1]
                    exit_port = line[2].split(':')[1]
                    index+=1
                elif line[0] == "ADD":
                    '''
                    P2P-CI/1.0 200 OK
                    RFC 123 A Proferred Official ICP thishost.csc.ncsu.edu 5678
                    '''
                    print("---------------------------------------------------------------\n")
                    print(str(originalRequest))
                    rfcNumber = line[2]
                    hostName = request[index + 1].split()[1]
                    portNumber = (request[index + 2].split(':')[1])
                    rfcTitle = request[index + 3].split(':')[1:]
                    addToIndex(rfcNumber, hostName, portNumber, rfcTitle)
                    str_to_send = "P2P-CI/1.0 200 OK\nRFC " + line[2] +\
                                  " " + request[index + 1].split()[1] + \
                                  " " + ' '.join([str(x) for x in request[index + 3].split(':')[1:]]).strip() + \
                                  " " + request[index + 2].split()[1]
                    client_socket.send(bytearray(str_to_send, "utf8"))
                    index += 4
                elif line[0] == "LIST":
                    '''
                    version <sp> status code <sp> phrase <cr> <lf>
                    <cr> <lf>
                    RFC number <sp> RFC title <sp> hostname <sp> upload port number<cr><lf>
                    RFC number <sp> RFC title <sp> hostname <sp> upload port number<cr><lf>
                    ...
                    <cr><lf>

                    LIST ALL P2P-CI/1.0
                    Host: thishost.csc.ncsu.edu
                    Port: 5678
                    '''
                    print("---------------------------------------------------------------\n")
                    print(str(originalRequest))
                    list_of_rfcs = list()
                    str_to_send = line[2] + " 200 OK\n"
                    for rfc in list_of_rfcs:
                        str_to_send += "RFC " + rfc[0] + " RFC " + rfc[1] + " " + rfc[2] + " " + rfc[3] + "\n"
                    client_socket.send(bytearray(str_to_send, "utf8"))
                    index += 3
                elif line[0] == "LOOKUP":
                    '''
                    version <sp> status code <sp> phrase <cr> <lf>
                    <cr> <lf>
                    RFC number <sp> RFC title <sp> hostname <sp> upload port number<cr><lf>
                    RFC number <sp> RFC title <sp> hostname <sp> upload port number<cr><lf>
                    ...
                    <cr><lf>
                    '''
                    print("---------------------------------------------------------------\n")
                    print(str(originalRequest))
                    list_of_rfcs = lookup(line[2])
                    str_to_send = "P2P-CI/1.0 200 OK\n"
                    for rfc in list_of_rfcs:
                        str_to_send += rfc[0] + " " + rfc[1] + " " + rfc[2] + " " + rfc[3] + "\n"
                    client_socket.send(bytearray(str_to_send, "utf8"))
                    index += 4
                elif line[0] == "EXIT":
                    # EXIT hostname port
                    exit_host = line[1]
                    exit_port = line[2]
                    break;
        print("-------------------------------------")
        peers.pop(exit_host, None)
        new_RFCs = []
        for rfc in RFCs:
            if rfc[2] == exit_host and rfc[3] == exit_port:
                print("")
            else:
                new_RFCs.append(rfc)
        RFCs = new_RFCs
        client_socket.close()
    except:
        # print("Exception and HostName: " + exit_host + " portNumber: " + exit_port)
        peers.pop(exit_host, None)
        new_RFCs = []
        for rfc in RFCs:
            if rfc[2] == exit_host and rfc[3] == exit_port:
                print("")
            else:
                new_RFCs.append(rfc)
        RFCs = new_RFCs
        client_socket.close()


while True:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()
