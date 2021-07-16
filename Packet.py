from enum import Enum
import re

class PacketType(Enum):
	'''
	Packet type Enum class. We store type of packets that can be send between
	peers as enums. Each enum has a code, a regex pattern and description.
	'''

	def __new__(cls, value):
		obj = object.__new__(cls)
		obj._value_ = value
		# obj.pattern = re.compile(regex)
		# obj.description = description
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
	
	MESSAGE =   			0
	ROUTING_REQUEST =     	10
	ROUTING_RESPONSE =     	11
	PARENT_ADVERTISE =  	20
	ADVERTISE =  			21
	DESTINATION_NOT_FOUND =	31
	CONNECTION_REQUEST =    41


class Packet:
	def __init__(self, typ: PacketType, src_id: str, dst_id: str, data: str) -> None:
		self.type: PacketType = typ
		self.destination: int = dst_id
		self.source: int = src_id
		self.data: str = data

	def __str__(self) -> str:
		return f"{self.type.code}|{self.source}|{self.destination}|{self.data}"

