import Network as nt
import socket
import threading


# admin initialization
localHost_admin = '127.0.0.1'
port_admin = 23000
admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # (IPv4 , TCP)
admin.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
admin.bind((localHost_admin, port_admin))
admin.listen()

network = nt.Network()
peers = {}


def handle(peer):
    while True:
        try:
            pass
        except:
            admin.close()
            break


while True:
    print("*****")
    peer, address = admin.accept()
    print("Connected with:", address)
    msg = peer.recv(1024).decode("ascii")
    msg_arr = msg.split()
    if "REQUESTS FOR CONNECTING TO NETWORK ON PORT" in msg:
        id, port = msg_arr[0], msg_arr[-1]
        peers[id] = peer
        data = (id, port)
        parent = network.insert_node(network.root, data)
        if parent is None:
            admin_msg = "CONNECT TO" + str(-1) + "WITH PORT" + str(-1)
        else:
            admin_msg = "CONNECT TO" + str(parent.data[0]) + "WITH PORT" + str(parent.data[1])
        peer.send(admin_msg.encode("ascii"))
        thread = threading.Thread(target=handle, args=(peer,))
        thread.start()
