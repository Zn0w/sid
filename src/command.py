from enum import Enum


class CommandType(Enum):
	START = 1
	POSITIVE = 2
	NEGATIVE = 3
	SEARCH = 4
	TIME = 5
	WEATHER = 6
	UNKNOWN = 7

class Command():
	def __init__(self, type_str, vocab_str):
		if type_str == "start":
			self.type = CommandType.START
		elif type_str == "positive":
			self.type = CommandType.POSITIVE
		elif type_str == "negative":
			self.type = CommandType.NEGATIVE
		elif type_str == "search":
			self.type = CommandType.SEARCH
		elif type_str == "time":
			self.type = CommandType.TIME
		elif type_str == "weather":
			self.type = CommandType.WEATHER
		else:
			self.type = CommandType.UNKNOWN
		
		self.vocabulary = vocab_str.split(",")
	
	def match(self, words):
		# special condition for search command, because the search query may contain words what trigger other commands
		if self.type == CommandType.SEARCH:
			for vocab_word in self.vocabulary:
				if words.find(vocab_word) == 0:
					return True
			return False
		else:
			for vocab_word in self.vocabulary:
				if vocab_word in words:
					return True
			return False