from Packet import Packet, PacketType
import re
import socket
import threading
threading
from commons import dprint, BasePeer


ADMIN_HOST = '127.0.0.1'
ADMIN_PORT = 23000

PEER_HOST = '127.0.0.1'

class Client(BasePeer):
	def __init__(self, admin_host, admin_port, peer_host):
		self.admin_host = admin_host
		self.admin_port = admin_port
		self.host = peer_host
		self.listening_port = 0
		self.id = None
		# self.quit = False


	def peer_receiving_handler(self, peer):
		''' Receive messages from peers '''
		while True:
			try:
				msg = self.receive(peer)
				if msg == '':
					dprint(f"Connection to peer {peer.getpeername()} closed.")
					peer.close()
					break

				msg_arr = msg.split()
				if "CONNECT TO" in msg:
					parent_id = msg_arr[2]
					parent_port = msg_arr[-1]
					print(parent_id, parent_port)

			except socket.error as e:
				peer.close()
				dprint(f"Error. Peer {peer.getpeername()} shutdown.", e)


	def listen_handler(self, server):
		server.listen()
		dprint(f"Peer is listening on {self.host}:{self.listening_port}")

		while True:
			peer, address = server.accept()
			dprint(f"Peer {address} is connected")
			thread = threading.Thread(target=self.peer_receiving_handler, args=[peer])
			thread.start()


	def input_handler(self):
		''' Get inputs from terminal and send messages '''
		while True:
			msg = input()
			

	def start(self):
		''' Get inputs from terminal and send messages '''
		while True:
			start_msg = input()
			if re.match('CONNECT AS (\w+) ON PORT (\d+)', start_msg):
				start_msg_arr = start_msg.split() 
				self.id, self.listening_port = start_msg_arr[2], int(start_msg_arr[-1])

				try:
					server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
					server.bind((self.host, self.listening_port)) # passing zero will choose a random free port
				except OSError as e:
					print(f"could not bind to {self.host} {self.listening_port}")
					continue

				# connect to admin to get parent in network
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
					peer.connect((self.admin_host, self.admin_port))
					dprint(f"Client is connected to admin {self.admin_host}:{self.admin_port}")

					conn_msg = f"{self.id} REQUESTS FOR CONNECTING TO NETWORK ON PORT {self.listening_port}"
					self.send(peer, conn_msg)

					msg = self.receive(peer)
					if re.match('CONNECT TO (-?\w+) WITH PORT (-?\d+)', msg):
						msg_splited = msg.split()
						self.parent_id = msg_splited[2] if msg_splited[2] != '-1' else None
						self.parent_port = int(msg_splited[-1]) if msg_splited[2] != '-1' else None
					else:
						print(msg)
						continue

				# start listening on desired port
				thread = threading.Thread(target=self.listen_handler, args=[server])
				thread.start()
				
				# connect to parent and send listening port to parent if it is not root
				if self.parent_id:
					with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
						peer.connect((self.host, self.parent_port))
						dprint(f"Client is connected to parent {self.host}:{self.parent_port}")

						packet = Packet(PacketType.CONNECTION_REQUEST, self.id, self.parent_id, self.listening_port)
						self.send_packet(peer, packet)
				
				dprint('successfully connected to network')
				
				# start listening for commands
				self.input_handler()

			else:
				print("INVALID COMMAND")
		

if __name__ == "__main__":
	client = Client(ADMIN_HOST, ADMIN_PORT, PEER_HOST)
	client.start()
