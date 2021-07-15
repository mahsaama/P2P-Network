

from Packet import Packet, PacketType


LOG_LEVEL = 2	# 0 for no log, 1 for normal log, 2 for full log
MSG_SIZE = 1024

def dprint(*args, level=1):
    if LOG_LEVEL >= level:
        print(*args)


class BasePeer:

	def send(self, socket, msg):
		dprint(f"Send message to peer {socket.getpeername()}: {msg}", level=2)
		socket.send(msg.encode("ascii"))

	def receive(self, socket):
		msg = socket.recv(MSG_SIZE).decode("ascii")
		if msg:
			dprint(f"Got message from peer {socket.getpeername()}: {msg}")
		return msg

	def send_packet(self, socket, packet:Packet):
		self.send(socket, packet.__str__())

	def receive_packet(self, socket):
		msg = self.receive(socket)
		splited = msg.split('|')
		packet = Packet(PacketType.get_packet_type_from_code(splited[0]), splited[1], splited[2], splited[3])
		return packet

	# def send_fixed_length(self, message, desired_length = MSG_SIZE):
	# 	''' Send message to peer for length `desired_length`. Default to `MSG_SIZE` 
	# 	which is set at top of the file and must be same in peers. '''

	# 	message = message.rjust(desired_length, ' ')
	# 	if len(message) > desired_length:
	# 		message = message[:desired_length]
	# 	self.client.send(message.encode('ascii'))


	# def recieve_fixed_length(self, desired_length = MSG_SIZE):
	# 	''' Recieve message for length `desired_length`. Default to `MSG_SIZE`. '''

	# 	message = b''
	# 	while len(message) < desired_length:
	# 		message += self.socket.recv(desired_length - len(message))	
	# 	message = message.decode('ascii').strip()
	# 	return message


	# def send(self, message, *args):
	# 	''' Send message code in 2 bytes and then send arguments in `MSG_SIZE`. '''

	# 	dprint("Sending...", message, args)

	# 	self.send_fixed_length(message.code, 2)
	# 	for arg in args:
	# 		dprint("send arg:", arg)
	# 		self.send_fixed_length(arg)


	# def recieve(self):	
	# 	''' Recieve message code in 2 bytes and then if message enum is found
	# 	recieve arguments. '''

	# 	dprint("Receiving...")

	# 	message_code = self.recieve_fixed_length(2)
	# 	dprint("msg code:", message_code)

	# 	message = self.recieve_enum_class.get_code(message_code)
	# 	if message is None:
	# 		return (None, [])
		
	# 	args = []
	# 	for _ in range(message.args_no):
	# 		arg = self.recieve_fixed_length()
	# 		dprint("received arg:", arg)
	# 		args.append(arg)

	# 	return (message, args)
