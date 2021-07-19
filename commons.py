
from Packet import Packet, PacketType
import socket

LOG_LEVEL = 3	# higher number -> more log
MSG_SIZE = 1024

class bcolors:
	PINK = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	ORANGE = '\033[93m'
	RED = '\033[91m'
	NORMAL = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def dprint(*args, level=1):
	if LOG_LEVEL >= level:
		if level == 1:
			print(bcolors.GREEN, *args, bcolors.NORMAL)
		elif level == 2:
			print(bcolors.BLUE, *args, bcolors.NORMAL)
		else:
			print(bcolors.PINK, *args, bcolors.NORMAL)

class BaseSenderReceiver:
	def send(self, socket: socket.SocketType, msg, addr=None):
		dprint(f"Send message to peer {addr if addr else socket.getpeername()} msg: {msg}", level=2)
		msg = msg.encode("ascii")
		if not addr:
			socket.send(msg)
		else:
			socket.sendto(msg, addr)

	def receive(self, socket: socket.SocketType):
		msg = socket.recv(MSG_SIZE).decode("ascii")
		msg = msg.strip()
		if msg:
			dprint(f"Got message from peer {socket.getpeername()}: {msg}")
		return msg

	def send_packet(self, socket: socket.SocketType, packet: Packet, addr=None):	
		self.send(socket, packet.__str__(), addr)

	def receive_packet(self, socket) -> Packet:
		msg = self.receive(socket)
		if not msg:
			return None
		splited = msg.split('|')
		packet = Packet(PacketType.get_packet_type_from_code(splited[0]), splited[1], splited[2], splited[3])
		return packet

	def receive_packet_udp(self, socket: socket.SocketType):
		msg, address = socket.recvfrom(MSG_SIZE)
		if not msg:
			return None
		msg = msg.decode("ascii")
		msg = msg.strip()
		dprint(f"Got message from peer {address}: {msg}")
		splited = msg.split('|')
		packet = Packet(PacketType.get_packet_type_from_code(splited[0]), splited[1], splited[2], splited[3])
		return packet, address
