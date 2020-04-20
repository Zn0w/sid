from enum import Enum


class CommandType(Enum):
	START = 1
	POSITIVE = 2
	NEGATIVE = 3
	UNKNOWN = 4

class Command():
	def __init__(self, type_str, vocab_str):
		if type_str == "start":
			self.type = CommandType.START
		elif type_str == "positive":
			self.type = CommandType.POSITIVE
		elif type_str == "negative":
			self.type = CommandType.NEGATIVE
		else:
			self.type = CommandType.UNKNOWN
		
		self.vocabulary = vocab_str.split(",")
	
	def match(self, words):
		for vocab_word in self.vocabulary:
			if vocab_word in words:
				return True
		
		return False