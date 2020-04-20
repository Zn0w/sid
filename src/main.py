import speech_recognition as sr
import os
import webbrowser

import command as c


# TODO : deal with global variables
commands = []
scripts = {}


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

def execute_start_command(words):
	for key in scripts.keys():
		if key in words:
			for script_command in scripts[key].split(","):
				os.system(script_command)
			break

def execute_search_command(words):
	# TODO : get rid of the command part
	url = "https://www.google.com/search?q={}".format(words)
	webbrowser.open(url)

def react(input):
	for command in commands:
		if command.match(input):
			if command.type == c.CommandType.START:
				execute_start_command(input)
			elif command.type == c.CommandType.SEARCH:
				execute_search_command(input)
			break


def main():
	# get vocabulary resources
	
	try:
		file = open("resources/commands.sid", "r")
		commands_raw = file.read()
		file.close()
	except IOError:
		print("Couldn't read commands vocabulary file")
		exit
	
	try:
		file = open("resources/start_scripts.sid", "r")
		scripts_raw = file.read()
		file.close()
	except IOError:
		print("Couldn't read start_scripts file")
		exit
	
	# parse vocabulary resources

	print(commands_raw)	# DEBUG PRINT
	print(scripts_raw)	# DEBUG PRINT
	
	compound_commands = commands_raw.split("\n")
	for compound_command in compound_commands:
		command = compound_command.split(" : ")
		commands.append(c.Command(command[0], command[1]))
	
	compound_scripts = scripts_raw.split("\n")
	for compound_script in compound_scripts:
		script = compound_script.split(" : ")
		scripts.update({script[0] : script[1]})

	# DEBUG PRINT
	for command in commands:
		print(command.type.value, command.vocabulary)
	print(scripts)	# DEBUG PRINT

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