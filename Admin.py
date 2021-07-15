import Network as nt
import socket
import threading
from commons import dprint, MSG_SIZE

# admin initialization
HOST = '127.0.0.1'
PORT = 23000

class Admin:
	def __init__(self) -> None:
		self.network = nt.Network()
		self.peers = {}


	def client_handler(self, peer):
		try:
			while True:
				msg = peer.recv(MSG_SIZE).decode("ascii")
				if msg == '':
					dprint(f"Connection to peer {peer.getpeername()} closed.")
					peer.close()
					break

				dprint(f"Got message from peer {peer.getpeername()}: {msg}")

				if "REQUESTS FOR CONNECTING TO NETWORK ON PORT" in msg:
					msg_arr = msg.split()
					id, port = msg_arr[0], msg_arr[-1]
					self.peers[id] = peer
					data = (id, port)
					parent = self.network.insert_node(self.network.root, data)
					if parent is None:
						admin_msg = "CONNECT TO " + str(-1) + " WITH PORT " + str(-1)
					else:
						admin_msg = "CONNECT TO " + str(parent.data[0]) + " WITH PORT " + str(parent.data[1])
					peer.send(admin_msg.encode("ascii"))


		except socket.error as e:
			peer.close()
			dprint(f"Error. Peer {peer.getpeername()} shutdown.", e)

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
