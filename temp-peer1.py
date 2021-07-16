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
		
		self.parent_id = None
		self.parent_port = None
		
		self.known_peers = {} 		# dict of {peer_id: peer_port}. peer_port is None for all except children
		self.children_subtree = {} 	# dict of {child_id: list of peer_id}
		
		# self.quit = False

	def add_to_known_peers(self, id_, port=None):
		if id_ not in self.known_peers or self.known_peers[id_] == None:
			dprint(f'add peer with id {id_} and port {port} to known peers', level=2)
			self.known_peers[id_] = port

	def send_packet_to_peer(self, peer_port, packet):
		sending_port = self.get_sending_port_from_listening_port(self.listening_port)
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
				peer.bind((self.host, sending_port))
				peer.connect((self.host, peer_port))
				dprint(f"connected to {self.host}:{peer_port} from port {sending_port}", level=2)
				self.send_packet(peer, packet)
				peer.shutdown(socket.SHUT_RDWR)
				peer.close()
		except OSError as e:
			dprint(f"could not send packet: {packet} to port {peer_port} from port {sending_port}, err: {e}")
		
		dprint(f"connected to {self.host}:{peer_port} tamam nashot?", level=2)


	def advertise_to_parent(self, peer_id):
		if not self.parent_port:
			return
		packet = Packet(PacketType.PARENT_ADVERTISE, self.id, self.parent_id, peer_id)
		self.send_packet_to_peer(self.parent_port, packet)

	def add_new_child(self, id_):
		dprint(f'add new child with id {id_}', level=2)
		self.children_subtree[id_] = []
		self.add_to_child_subtree(id_, id_)

	def add_to_child_subtree(self, new_peer_id, child_id):
		dprint(f'add new peer with id {new_peer_id} to child subtree with id {child_id}', level=2)
		if child_id not in self.children_subtree:
			raise ValueError('Child_id is not in child_ids dict.')

		self.children_subtree[child_id].append(new_peer_id)

	def get_sending_port_from_listening_port(self, listening_port):
		return listening_port + 1

	def get_listen_port_from_sending_port(self, sending_port):
		return sending_port - 1
		
	def are_ports_for_same_peer(self, listen_port, sending_port):
		return self.get_listen_port_from_sending_port(sending_port) == listen_port


	def route_all(self, packet:Packet, sender_port=None):
		for child in self.children_subtree.keys():
			if not self.are_ports_for_same_peer(self.known_peers[child], sender_port):
				dprint(f'route packet with source {packet.source} and destination {packet.destination} to CHILD {child} with port {self.known_peers[child]}', level=3)
				self.send_packet_to_peer(self.known_peers[child], packet)
			
		if self.parent_port:
			if not self.are_ports_for_same_peer(self.parent_port, sender_port):
				dprint(f'route packet with source {packet.source} and destination {packet.destination} to PARENT {self.parent_id} with port {self.parent_port}', level=3)
				self.send_packet_to_peer(self.parent_port, packet)


	def route_packet(self, packet:Packet, sender_port=None):
		# TODO check if dest is in known filters????

		if not sender_port:
			sender_port = self.get_sending_port_from_listening_port(self.listening_port)

		if packet.destination == '-1':
			self.route_all(packet, sender_port)
			return True

		for child in self.children_subtree.keys():
			if packet.destination in self.children_subtree[child]:
				dprint(f'route packet with source {packet.source} and destination {packet.destination} to CHILD {child} with port {self.known_peers[child]}', level=3)
				self.send_packet_to_peer(self.known_peers[child], packet)
				return True
		
		if self.parent_port:
			dprint(f'route packet with source {packet.source} and destination {packet.destination} to PARENT {self.parent_id} with port {self.parent_port}', level=3)
			self.send_packet_to_peer(self.parent_port, packet)
			return True
		
		if packet.source != self.id:
			not_found_packet = Packet(PacketType.DESTINATION_NOT_FOUND, self.id, packet.source, f"DESTINATION {packet.destination} NOT FOUND")
			self.send_packet_to_peer(self.get_listen_port_from_sending_port(sender_port), not_found_packet)
			
		dprint(f'could not route packet with source {packet.source} and destination {packet.destination}', level=3)
		return False


	def peer_receiving_handler(self, peer: socket.SocketType):
		''' Receive messages from peers '''
		peer_port = peer.getpeername()[1]
		while True:
			try:
				packet = self.receive_packet(peer)
				if not packet:
					dprint(f"Connection to peer {peer.getpeername()} closed.")
					peer.close()
					break

				self.add_to_known_peers(packet.source)

				# If packet is routing response we need to change it before continue
				if packet.type == PacketType.ROUTING_RESPONSE:
					if packet.source == self.parent_id:
						new_data = f'{self.id} <- {packet.data}'
					else:
						new_data = f'{self.id} -> {packet.data}'
					packet = Packet(PacketType.ROUTING_RESPONSE, self.id, packet.destination, new_data)
					
				# If packet dest is not only us we need to route it
				if packet.destination != self.id:
					self.route_packet(packet, peer_port)
				
				# If we aren't included in packet dist we pass
				if packet.destination != '-1' and packet.destination != self.id:
					continue
				
				# If we reach here it means packet is for us
				if packet.type == PacketType.CONNECTION_REQUEST:
					peer_port = int(packet.data)
					self.add_to_known_peers(packet.source, peer_port)
					self.advertise_to_parent(packet.source)
					self.add_new_child(packet.source)

				elif packet.type == PacketType.PARENT_ADVERTISE:
					peer_id = packet.data
					self.add_to_known_peers(peer_id)
					self.advertise_to_parent(peer_id)
					self.add_to_child_subtree(peer_id, packet.source)

				elif packet.type == PacketType.ADVERTISE:
					
					pass

				elif packet.type == PacketType.ROUTING_REQUEST:
					response_packet = Packet(PacketType.ROUTING_RESPONSE, self.id, packet.source, self.id)
					self.route_packet(response_packet, peer_port)
				
				elif packet.type == PacketType.ROUTING_RESPONSE:
					print(packet.data)
				
				elif packet.type == PacketType.DESTINATION_NOT_FOUND:
					print(packet.data)

				elif packet.type == PacketType.MESSAGE:
					pass # TODO


			except socket.error as e:
				peer.close()
				dprint(f"Error. Peer {peer.getpeername()} shutdown.", e)


	def input_handler(self):
		''' Get inputs from terminal and send messages '''
		while True:
			msg = input()
			if re.fullmatch('SHOW KNOWN CLIENTS', msg, flags=re.IGNORECASE):
				for p in self.known_peers.keys():
					print(p)
			
			elif re.fullmatch('ROUTE (\w+)', msg, flags=re.IGNORECASE):
				dest_id = msg.split()[1]
				packet = Packet(PacketType.ROUTING_REQUEST, self.id, dest_id, '')
				self.route_packet(packet)

			elif re.fullmatch('ADVERTISE (\w+)', msg, flags=re.IGNORECASE):
				dest_id = msg.split()[1]
				packet = Packet(PacketType.ADVERTISE, self.id, dest_id, '')
				self.route_packet(packet)

			else:
				print("INVALID COMMAND")


	def listen_handler(self, server):
		server.listen()
		dprint(f"Peer is listening on {self.host}:{self.listening_port}")

		while True:
			peer, address = server.accept()
			dprint(f"Peer {address} is connected")
			thread = threading.Thread(target=self.peer_receiving_handler, args=[peer])
			thread.start()
			

	def start(self):
		''' Get inputs from terminal and send messages '''
		while True:
			start_msg = input()
			if re.fullmatch('CONNECT AS (\w+) ON PORT (\d+)', start_msg, flags=re.IGNORECASE):
				start_msg_arr = start_msg.split() 
				self.id, self.listening_port = start_msg_arr[2], int(start_msg_arr[-1])

				try:
					server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
					server.bind((self.host, self.listening_port)) # passing zero will choose a random free port
				except OSError:
					print(f"could not bind to {self.host} {self.listening_port}")
					continue

				# connect to admin to get parent in network
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as peer:
					peer.connect((self.admin_host, self.admin_port))
					dprint(f"Client is connected to admin {self.admin_host}:{self.admin_port}")

					conn_msg = f"{self.id} REQUESTS FOR CONNECTING TO NETWORK ON PORT {self.listening_port}"
					self.send(peer, conn_msg)

					msg = self.receive(peer)
					if re.fullmatch('CONNECT TO (-?\w+) WITH PORT (-?\d+)', msg, flags=re.IGNORECASE):
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