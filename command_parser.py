"""
Handles the work of validating and processing command input.
"""
import time, subprocess, shlex, os
from db import session
from base import Command

UPLOAD_FOLDER = './app/uploads/'

def get_valid_commands(queue, filename):
	## open file
	print("filename:", filename)
	f = open(os.path.join(UPLOAD_FOLDER, filename), "r")
	## parse valid options
	commands = {}
	valid = {}
	c = 0
	for line in f:
		line = line[:-1]
		if line == "":
			continue
		elif line == "[COMMAND_LIST]":
			c = 1
			print("Now parsing COMMAND_LIST")
		elif line == "[VALID_COMMANDS]":
			c = 2
			print("Now parsing VALID_COMMANDS")
		if c == 1:
			if not hash(line) in commands:
				commands[hash(line)] = line
				print("Command to run: {" + line + "}")
		elif c == 2:
			valid[hash(line)] = line
			print("Valid commands: {" + line + "}")
	f.close()
	## compare commands against valid ones
	for h, command in commands.items():
		if not h in valid:
			continue
		else:
			## add valid commands to queue
			queue.put(command)
			print("Putting valid command into queue: {" + command + "}")
	

def process_command_output(queue):
	command = queue.get()
	# check for existance of command in db before running, so as not to waste computation
	for ran_command in session.query(Command).filter(Command.command_string==command):
		if (ran_command):
			print("command", command, "already processed")
			return
	print("About to run:", command)
	c = 0
	## start timer to store
	start = time.time()
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	## catch stdout with subprocess for storage
	try:
		stdout, stderr = proc.communicate(timeout=60)
		ttime = int((time.time() - start) * 1000)
	except subprocess.TimeoutExpired:
		proc.kill()
		stdout, stderr = proc.communicate()
		ttime = 0
	print("command: {" + command + "} took", ttime, "milliseconds")
	## put results to db
	db_in = Command(command_string=command, length=len(command), duration=ttime, output=stdout)
	print("put in database => command:", db_in.command_string,
		"len:", db_in.length,
		"time:", db_in.duration,
		"stdout:", db_in.output)
	session.add(db_in)
	session.commit()
	print("successfully put command to database")
