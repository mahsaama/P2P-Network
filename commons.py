
from Packet import Packet, PacketType
import socket
import Chatroom

LOG_LEVEL = 1	# higher number -> more log
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

class BasePeer:
	def __init__(self):
		self.firewall = []

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
		if self.firewall_check(packet.__str__().split('|'), flag=True):
			self.send(socket, packet.__str__(), addr)

	def receive_packet(self, socket) -> Packet:
		msg = self.receive(socket)
		if not msg:
			return None
		splited = msg.split('|')
		if self.firewall_check(splited, flag=False):
			packet = Packet(PacketType.get_packet_type_from_code(splited[0]), splited[1], splited[2], splited[3])
			return packet
		return None

	def receive_packet_udp(self, socket: socket.SocketType):
		msg, address = socket.recvfrom(MSG_SIZE)
		if not msg:
			return None
		msg = msg.decode("ascii")
		msg = msg.strip()
		dprint(f"Got message from peer {address}: {msg}")
		splited = msg.split('|')
		if self.firewall_check(splited, flag=False):
			packet = Packet(PacketType.get_packet_type_from_code(splited[0]), splited[1], splited[2], splited[3])
			return packet, address
		return None

	def firewall_check(self, msg_arr, flag):  # flag_send = True, flag_receive = False
		typ, id_src, id_dst = msg_arr[:3]
		for rule in self.firewall:
			rule_direction = rule[0]
			rule_source = rule[1]
			rule_destination = rule[2]
			rule_packet_type = rule[3]
			rule_action = rule[4]

			if rule_packet_type == typ and rule_action == "ACCEPT":
				if rule_direction == 'INPUT' and (rule_source == id_src or rule_source == '*') and (rule_destination == id_dst or id_dst == '-1'):
					dprint(f"Your input packet is accepted in match with {rule} rule.", level=2)
					return True
				elif rule_direction == 'OUTPUT' and rule_source == id_src and (rule_destination == id_dst or id_dst == '-1' or rule_destination == '*'):
					dprint(f"Your output packet is accepted in match with {rule} rule.", level=2)
					return True
				elif rule_direction == 'FORWARD' and (rule_source == id_src or rule_source == '*') and (rule_destination == id_dst or id_dst == '-1' or rule_destination == '*'):
					if flag:
						dprint(f"Your forward packet is accepted in match with {rule} rule.", level=2)
						return True
			elif rule_packet_type == typ and rule_action == "DROP":
				if rule_direction == 'INPUT' and (rule_source == id_src or rule_source == '*') and (rule_destination == id_dst or id_dst == '-1'):
					dprint(f"Your input packet is dropped in match with {rule} rule.", level=2)
					return False
				elif rule_direction == 'OUTPUT' and rule_source == id_src and (rule_destination == id_dst or id_dst == '-1' or rule_destination == '*'):
					dprint(f"Your output packet is dropped in match with {rule} rule.", level=2)
					return False
				elif rule_direction == 'FORWARD' and (rule_source == id_src or rule_source == '*') and (rule_destination == id_dst or id_dst == '-1' or rule_destination == '*'):
					if flag:
						dprint(f"Your forward packet is dropped in match with {rule} rule.", level=2)
						return False
		return True
