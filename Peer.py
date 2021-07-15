import socket
import threading
threading
from commons import dprint


ADMIN_HOST = '127.0.0.1'
ADMIN_PORT = 23000

PEER_HOST = '127.0.0.1'

class Client:
	def __init__(self, host):
		self.host = host
		self.listen_port = 0
		self.user_id = None
		self.quit = False


	def receiving_handler(self):
		''' Receive messages '''
		while True:
			if self.quit:
				break

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


	def sending_handler():
		''' Get inputs from terminal and send messages '''
		start_msg = input()
		start_msg_arr = start_msg.split()
		ID, listening_port = start_msg_arr[2], start_msg_arr[-1]
		sending_port = int(listening_port) + 1
		conn_msg = str(ID) + " REQUESTS FOR CONNECTING TO NETWORK ON PORT " + str(listening_port)
		peer.send(conn_msg.encode("ascii"))
		# while True:
		#     pass


	def listen(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: # (IPv4 , TCP)
			server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			server.bind((self.host, 0)) # passing zero will choose a random free port
			self.listen_port = server.getsockname()[1]
			server.listen()
			dprint(f"Peer is listening on {self.host}:{self.listen_port}")

			while True:
				peer, address = server.accept()
				dprint(f"Peer {address} is connected")
				thread = threading.Thread(target=self.receiving_handler, args=[peer])
				thread.start()


	def connect_to_network(self, admin_host, admin_port):
		# start listening on a port
		thread = threading.Thread(target=self.listen)
		thread.start()

		# connect to admin to get parent
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer_socket:
			peer_socket.connect((admin_host, admin_port))
			dprint(f"Client is connected to admin {admin_host}:{admin_port}")



if __name__ == "__main__":
	client = Client(PEER_HOST)
	client.connect_to_network(ADMIN_HOST, ADMIN_PORT)
