from enum import Enum
import re

DEBUG = True
MSG_SIZE = 1024

def dprint(*args):
    if DEBUG:
        print(*args)


class PacketType(Enum):
	'''
	Packet type Enum class. We store type of packets that can be send between
	peers as enums. Each enum has a code, a regex pattern and description.
	'''

	def __new__(cls, value, regex, description):
		obj = object.__new__(cls)
		obj._value_ = value
		obj.pattern = re.compile(regex)
		obj.description = description
		return obj
	
	@property
	def args_no(self):
		''' return number of arguments that will be followed after message code. '''
		return self.pattern.groups

	@property
	def code(self):
		''' return code type value as two charecter string '''
		return str(self.value).zfill(2)
	
	@classmethod
	def get_packet_type_from_code(cls, code):
		''' return type based on code '''
		try:
			return cls(int(code))
		except ValueError:
			return None

	''' Packet types ''' 
	
	# TODO clean these

	MESSAGE =   			0,	'',      				'Enter user-id'
	ROUTING_REQUEST =     	10,	'(\w+) (.+)', 			'show message from user'
	ROUTING_RESPONSE =     	11,	'(\w+) (.+)', 			'show message from user'
	PARENT_ADVERTISE =  	20,	'(\w+) (\w+) (.+)', 	'advertize  to parent'
	ADVERTISE =  			21,	'', 					'advertize self'
	DESTINATION_NOT_FOUND =	31,	'',      				'destination not found'
	CONNECTION_REQUEST =    41,	'(d+)',					'connection request to another peer, data: port'


class Packet:
	def __init__(self, packet_type: PacketType, source:int, destination: int, msg: str) -> None:
		self.type: PacketType = packet_type
		self.destination: int = destination
		self.source: int = source
		self.msg: str = msg


class MySocket:
	def __init__(self, socket):
		self.socket = socket


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
