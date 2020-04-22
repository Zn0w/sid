import speech_recognition as sr
import os
import webbrowser
import requests
from datetime import datetime
from gtts import gTTS
import playsound
import random
import sys

import command as c
import get_resources


# TODO : deal with global variables
commands = []
scripts = {}
responses = {}
active = True


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

def speak(text):
	speech = gTTS(text = text, lang = "en")
	speech.save("temp/speech.mp3")
	playsound.playsound("temp/speech.mp3")
	os.remove("temp/speech.mp3")

def execute_start_command(words):
	# occasionaly sid will give a response
	# P = 0.5 * 0.5 * 0.5 = 0.125, i.e. the response will be given in 12.5% of the occurences
	if (random.randint(0, 1) + random.randint(0, 1) + random.randint(0, 1)) == 3:
		speak(responses["ok"][random.randint(0, len(responses["ok"]) - 1)])

	for key in scripts.keys():
		if key in words:
			for script_command in scripts[key].split(","):
				os.system(script_command)
			break

def execute_search_command(words):
	speak("Opening in the browser")
	query = "robot ai uprising"
	for command in commands:
		if command.type == c.CommandType.SEARCH: # get search command object from the global commands pool
			for vocab_word in command.vocabulary:
				if vocab_word in words:
					query = words[len(vocab_word) + 1:] # substring with only query in it ('+ 1' for one space)
					break
	url = "https://www.google.com/search?q={}".format(query)
	webbrowser.open(url)

def execute_time_command(words):
	result = requests.get("http://worldtimeapi.org/api/ip")
	if result.status_code == 200:
		time_data = result.json()
		# "datetime":"2020-04-20T16:02:15.687382+03:00"
		current_time = datetime.strptime(time_data["datetime"][:10] + " " + time_data["datetime"][11:-13], "%Y-%m-%d %H:%M:%S")
		speak("It's " + current_time.strftime("%H:%M %A %d of %B %Y") + " in " + time_data["timezone"])
		print("It's ", current_time.strftime("%H:%M %A %d of %B %Y"), " in ", time_data["timezone"])
	else:
		current_time = datetime.now()
		speak("It's " + current_time.strftime("%H:%M %A %d of %B %Y"))
		print("It's ", current_time.strftime("%H:%M %A %d of %B %Y"))

def execute_weather_command(words):
	# for now no weather api, just a google search
	# TODO : evaluate the relative day (e.g. today, tomorrow) and location (e.g. london, chicago)
	speak("Opening in the browser")
	url = "https://www.google.com/search?q={}".format("weather")
	webbrowser.open(url)

def execute_chat_command(command):
	# the first word in vocabulary (in commands.sid) corresponds to the name of the response type
	response_type = responses[command.vocabulary[0]]
	speak(response_type[random.randint(0, len(response_type) - 1)])

	if command.type == c.CommandType.BYE:
		sys.exit()

def execute_sleep_command():
	speak("Going to sleep")
	global active
	active = False

def execute_wake_command():
	speak("Yes sir")
	global active
	active = True

def react(input):
	if active:
		for command in commands:
			if command.match(input):
				if command.type == c.CommandType.START:
					execute_start_command(input)
				elif command.type == c.CommandType.SEARCH:
					execute_search_command(input)
				elif command.type == c.CommandType.TIME:
					execute_time_command(input)
				elif command.type == c.CommandType.WEATHER:
					execute_weather_command(input)
				elif command.type == c.CommandType.HELLO or command.type == c.CommandType.BYE or command.type == c.CommandType.THANKS:
					execute_chat_command(command)
				elif command.type == c.CommandType.SLEEP:
					execute_sleep_command()
				break
	else:
		for command in commands:
			if command.type == c.CommandType.WAKE and command.match(input):
				execute_wake_command()
				break


def main():
	random.seed()	# init random number generator

	global commands
	global scripts
	global responses

	commands = get_resources.get_commands()
	scripts = get_resources.get_scripts()
	responses = get_resources.get_responses()

	# DEBUG PRINT
	for command in commands:
		print(command.type.value, command.vocabulary)
	print(scripts)	# DEBUG PRINT
	print(responses)	# DEBUG PRINT

	print("Speech recognition software version: " + sr.__version__)

	r = sr.Recognizer()
	mic = sr.Microphone(device_index = 1) # if no device_index supplied, then default mic (i'm not using the default one atm)

	while True:
		result = process_speech(r, mic)
		if result["success"] and result["input"] == None:
			print("Sorry, I did not hear you")
		elif not result["success"]:
			speak("I'm sorry but I cannot work properly due to a technical problem: " + result["input"] + ". Please contact tech support.")
			print("Technical problems: " + result["input"])
			break
		else:
			print("You said: " + result["input"])
			react(result["input"])


main()