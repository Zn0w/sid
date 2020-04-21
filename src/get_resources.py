import command as c

def read_entire_file(filepath):
	try:
		file = open(filepath, "r")
		file_contents = file.read()
		file.close()
		
		return file_contents
	except IOError:
		print("Couldn't read " + filepath)
		exit

def get_commands():
	commands_raw = read_entire_file("resources/commands.sid")

	commands = []

	compound_commands = commands_raw.split("\n")
	for compound_command in compound_commands:
		command = compound_command.split(" : ")
		commands.append(c.Command(command[0], command[1]))
	
	return commands

def get_scripts():
	scripts_raw = read_entire_file("resources/start_scripts.sid")

	scripts = {}

	compound_scripts = scripts_raw.split("\n")
	for compound_script in compound_scripts:
		script = compound_script.split(" : ")
		scripts.update({script[0] : script[1]})
	
	return scripts

def get_responses():
	responses_raw = read_entire_file("resources/responses.sid")

	responses = {}

	compound_responses = responses_raw.split("\n")
	for compound_responses in compound_responses:
		response = compound_responses.split(" : ")
		responses.update({response[0] : response[1].split(",")})
	
	return responses