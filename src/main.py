import speech_recognition as sr


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

def main():
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


main()