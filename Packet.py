from enum import Enum
import re

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
	
	# @property
	# def args_no(self):
	# 	''' return number of arguments that will be followed after message code. '''
	# 	return self.pattern.groups

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
	def __init__(self, typ: PacketType, src_id: str, dst_id: str, data: str) -> None:
		self.type: PacketType = typ
		self.destination: int = dst_id
		self.source: int = src_id
		self.data: str = data

	def __str__(self) -> str:
		return f"{self.type.code}|{self.destination}|{self.source}|{self.data}"

