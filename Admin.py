import Network as nt
import socket
import sys

localHost = '127.0.0.1'
port = 1024

network_root = nt.Node()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((localHost, port))
    s.listen()
    conn, address = s.accept()

    with conn:
        msg = conn.recv(1024)
        if "REQUESTS FOR CONNECTING TO NETWORK ON PORT" in msg.decode("utf-8"):
            msg_arr = msg.decode('utf-8').split(" ")
            if network_root.Data is None:
                admin_msg = "CONNECT TO" + str(-1) + "WITH PORT" + str(-1)
                conn.sendall(bytes(admin_msg, 'utf-8'))
                network_root.set_data((msg_arr[0], msg_arr[-1])) # TODO maybe add an object of Peer type instead?
            else:
                candid_par = nt.candid_parent(network_root)
                candid_par.add_child((msg_arr[0], msg_arr[-1]))
                admin_msg = "CONNECT TO" + str(candid_par.Data[0]) + "WITH PORT" + str(candid_par.Data[1])
                conn.sendall(bytes(admin_msg, 'utf-8'))


