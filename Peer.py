import socket
import threading

localHost_admin = '127.0.0.1'
port_admin = 23000
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer.connect((localHost_admin, port_admin))


# This is listening to receive a message
def receiving():
    while True:
        try:
            msg = peer.recv(1024).decode("ascii")
            msg_arr = msg.split()
            if "CONNECT TO" in msg:
                parent_id = msg_arr[2]
                parent_port = msg_arr[-1]
                print(parent_id, parent_port)
        except:
            peer.close()
            break


# This is for sending a message and terminal input commands
def sending():
    start_msg = input()
    start_msg_arr = start_msg.split()
    ID, listening_port = start_msg_arr[2], start_msg_arr[-1]
    sending_port = int(listening_port) + 1
    conn_msg = str(ID) + " REQUESTS FOR CONNECTING TO NETWORK ON PORT " + str(listening_port)
    peer.send(conn_msg.encode("ascii"))
    # while True:
    #     pass


receiving_thread = threading.Thread(target=receiving)
receiving_thread.start()

sending_thread = threading.Thread(target=sending)
sending_thread.start()
