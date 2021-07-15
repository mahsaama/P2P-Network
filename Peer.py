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
		self.known_peers = {}

		# self.quit = False

	def add_to_known_peers(self, id_, port=None):
		self.known_peers[id_] = port


	def send_packet_to_peer(self, peer_port, packet):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
			peer.connect((self.host, peer_port))
			dprint(f"connected to {self.host}:{peer_port}", level=2)
			self.send_packet(peer, packet)


	def advertise_to_parent(self, peer_id):
		if not self.parent_port:
			return
		packet = Packet(PacketType.PARENT_ADVERTISE, self.id, self.parent_id, peer_id)
		self.send_packet_to_peer(self.parent_port, packet)


	def peer_receiving_handler(self, peer):
		''' Receive messages from peers '''
		while True:
			try:
				packet = self.receive_packet(peer)
				if not packet:
					dprint(f"Connection to peer {peer.getpeername()} closed.")
					peer.close()
					break

				self.add_to_known_peers(packet.source)

				if packet.type == PacketType.CONNECTION_REQUEST:
					peer_port = int(packet.data)
					self.add_to_known_peers(packet.source, peer_port)
					self.advertise_to_parent(packet.source)

				elif packet.type == PacketType.PARENT_ADVERTISE:
					peer_id = packet.data
					self.add_to_known_peers(peer_id)
					self.advertise_to_parent(peer_id)



			# MESSAGE 
			# ROUTING_REQUEST
			# ROUTING_RESPONSE
			# PARENT_ADVERTISE
			# ADVERTISE
			# DESTINATION_NOT_FOUND 

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
			if re.match('SHOW KNOWN CLIENTS', msg):
				for p in self.known_peers.keys():
					print(p)
			

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
					self.add_to_known_peers(self.parent_id, self.parent_port)
					packet = Packet(PacketType.CONNECTION_REQUEST, self.id, self.parent_id, self.listening_port)				
					self.send_packet_to_peer(self.parent_port, packet)
				
				dprint('successfully connected to network')
				
				# start listening for commands
				self.input_handler()

			else:
				print("INVALID COMMAND")
		

if __name__ == "__main__":
	client = Client(ADMIN_HOST, ADMIN_PORT, PEER_HOST)
	client.start()
