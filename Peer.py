import socket
import sys


class Peer:
    def __init__(self, ID, port):
        self.ID = ID
        self.lsn_port = port
        self.known_peers = []



lsnPort = 1025 # TODO this should change
ID = 2020 # TODO should change

adminHost = '127.0.0.1'
adminPort = 1024


# use when terminal
def connect_network():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((adminHost, adminPort))
        conn_msg = str(ID) + "REQUESTS FOR CONNECTING TO NETWORK ON PORT" + str(lsnPort)
        s.sendall(bytes(conn_msg, 'utf-8'))
        msg = s.recv(1024)
        # Now go say hello to your Dad :)
