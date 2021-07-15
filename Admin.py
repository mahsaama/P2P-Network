import Network as nt
import socket
import threading
import re
from commons import dprint, BasePeer

# admin initialization
HOST = '127.0.0.1'
PORT = 23000

class Admin(BasePeer):
	def __init__(self) -> None:
		self.network = nt.Network()
		self.peers = {}

	def client_handler(self, peer):
		try:
			while True:
				msg = self.receive(peer)
				if msg == '':
					dprint(f"Connection to peer {peer.getpeername()} closed.")
					peer.close()
					break

				if re.match('(\w+) REQUESTS FOR CONNECTING TO NETWORK ON PORT (\d+)', msg):
					msg_arr = msg.split()
					id_, port = msg_arr[0], msg_arr[-1]
					
					if self.get_peer_from_id(id_):
						admin_msg = f"ID {id_} already exist"
					else:
						self.peers[id_] = peer
						parent = self.network.insert_new_node(id_, port)
						if parent is None:
							admin_msg = f"CONNECT TO -1 WITH PORT -1"
						else:
							admin_msg = f"CONNECT TO {parent.id} WITH PORT {parent.port}"

					self.send(peer, admin_msg)

		except socket.error as e:
			peer.close()
			dprint(f"Error. Peer {peer.getpeername()} shutdown.", e)


	def get_peer_from_id(self, id_):
		if id_ in self.peers:
			return self.peers[id_]
		return None
		

	def listen(self, host, port):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: # (IPv4 , TCP)
			server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			server.bind((host, port))
			server.listen()
			dprint(f"Server is listening on {host}:{port}")

			while True:
				peer, address = server.accept()
				dprint(f"Peer {address} is connected to server")
				thread = threading.Thread(target=self.client_handler, args=[peer])
				thread.start()


if __name__ == "__main__":
	admin = Admin()
	admin.listen(HOST, PORT)			
