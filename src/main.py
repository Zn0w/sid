import speech_recognition as sr
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
	
	def match(self, word):
		for vocab_word in self.vocabulary:
			if word == vocab_word:
				return True
		
		return False


# TODO : deal with this global variable
commands = []


def process_speech(processor, input_device):
	if not isinstance(processor, sr.Recognizer):
		raise TypeError("processor must be speech_recognition.Recognizer instance")
	
	if not isinstance(input_device, sr.Microphone):
		raise TypeError("input_device must be speech_recognition.Microphone instance")
	
	result = { "success": True, "input": None }

	with input_device as source:
		processor.adjust_for_ambient_noise(source, duration = 1)
		audio_input = processor.listen(source)
		try:
			result["input"] = processor.recognize_google(audio_input)
		except sr.UnknownValueError:
			result["input"] = None
		except sr.RequestError:
			result["success"] = False
			result["input"] = "speech recognition API is unavailable"
	
	return result

def react(input):
	input_words = input.split(" ")
	for command in commands:
		if command.match(input_words[0]):
			print("matched with ", command.vocabulary)

def main():
	# get vocabulary resources
	
	try:
		file = open("resources/commands.sid", "r")
		commands_raw = file.read()
		file.close()
	except IOError:
		print("Couldn't read commands vocabulary file")
		exit
	
	# parse vocabulary resources

	print(commands_raw)	# DEBUG PRINT
	
	compound_commands = commands_raw.split("\n")
	for compound_command in compound_commands:
		command = compound_command.split(":")
		commands.append(Command(command[0], command[1]))

	# DEBUG PRINT
	for command in commands:
		print(command.type.value, command.vocabulary)	

	print("Speech recognition software version: " + sr.__version__)

	r = sr.Recognizer()
	mic = sr.Microphone(device_index = 1)

	while True:
		result = process_speech(r, mic)
		if result["success"] and result["input"] == None:
			print("Sorry, I did not hear you")
		elif not result["success"]:
			print("Technical problems: " + result["input"])
			break
		# TODO : refactor this condition
		elif result["input"] == "goodbye" or result["input"] == "bye":
			print("See you later")
			break
		else:
			print("You said: " + result["input"])
			react(result["input"])


main()