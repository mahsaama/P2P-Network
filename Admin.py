import Network as nt
import socket


# admin initialization
localHost_admin = '127.0.0.1'
port_admin = 1024
admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (IPv4 , TCP)
admin.bind((localHost_admin, port_admin))
admin.listen()

network = nt.Network()

while True:
    peer, address = admin.accept()
    msg = peer.recv(1024).decode("ascii")
    msg_arr = msg.split()
    if "REQUESTS FOR CONNECTING TO NETWORK ON PORT" in msg:
        data = (msg_arr[0], msg_arr[-1])  # (ID, port)
        parent = network.insert_node(network.root, data)
        if parent is None:
            admin_msg = "CONNECT TO" + str(-1) + "WITH PORT" + str(-1)
        else:
            admin_msg = "CONNECT TO" + str(parent.data[0]) + "WITH PORT" + str(parent.data[1])
        peer.send(admin_msg.encode("ascii"))
