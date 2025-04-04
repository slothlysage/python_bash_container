"""
Details the various flask endpoints for processing and retrieving
command details as well as a swagger spec endpoint
"""

from multiprocessing import Process, Queue
import sys
from flask import Flask, request, jsonify
from flask_swagger import swagger

from db import session, engine
from base import Base, Command
from command_parser import get_valid_commands, process_command_output

import os
from werkzeug.utils import secure_filename

import json

UPLOAD_FOLDER = './app/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/commands', methods=['GET'])
def get_command_output():
	"""
	Returns as json the command details that have been processed
	to date.
	---
	tags: [commands]
	responses:
	  200:
		description: Commands returned OK
	  400:
		description: Commands not found
	"""
	commands = session.query(Command)
	for command in commands:
		print(command.id, command.command_string, command.length, command.duration, command.output)
	return jsonify(Commands = [i.serialize for i in commands.all()])
	


@app.route('/commands', methods=['POST'])
def process_commands():
	"""
	Processes commands from a command list
	---
	tags: [commands]
	parameters:
	  - name: filename
		in: formData
		description: filename of the commands text file to parse
					 which exists on the server
		required: true
		type: string
	responses:
	  200:
		description: Processing OK
	"""
	
	#need to grab and store file from the POST request
	file = request.files['filename']
	filename = secure_filename(file.filename) 
	print("POST filename:", filename)
	#make sure the upload folder exits before storage
	if not os.path.exists(UPLOAD_FOLDER):
		os.makedirs(UPLOAD_FOLDER)
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	queue = Queue()
	get_valid_commands(queue, filename)
	#better queue usage so it isn't limited by range
	while queue.empty() == False:
		process = Process(target=process_command_output, args=(queue,))
		process.start()
		process.join()
	return 'Successfully processed commands.'


@app.route('/database', methods=['POST'])
def make_db():
	"""
	Creates database schema
	---
	tags: [db]
	responses:
	  200:
		description: DB Creation OK
	"""
	Base.metadata.create_all(engine)
	return 'Database creation successful.'


@app.route('/database', methods=['DELETE'])
def drop_db():
	"""
	Drops all db tables
	---
	tags: [db]
	responses:
	  200:
		description: DB table drop OK
	"""
	Base.metadata.drop_all(engine)
	return 'Database deletion successful.'


@app.route('/spec', methods=['GET'])
def swagger_spec():
	"""
	Display the swagger formatted JSON API specification.
	---
	tags: [docs]
	responses:
	  200:
		description: OK status
	"""
	spec = swagger(app)
	spec['info']['title'] = "Intel AI DLS coding challenge API"
	spec['info']['description'] = ("Intel AI deep learning systems coding " +
								   "challenge for interns and full-time hires")
	spec['info']['license'] = {
		"name": "Intel Proprietary License",
		"url": "https://ai.intel.com",
	}
	spec['info']['contact'] = {
		"name": "Intel DLS Team",
		"url": "https://ai.intel.com",
		"email": "scott.leishman@intel.com",
	}
	spec['schemes'] = ['http']
	spec['tags'] = [
		{"name": "db", "description": "database actions (create, delete)"},
		{"name": "commands", "description": "process and retrieve commands"}
	]
	return jsonify(spec)


if __name__ == '__main__':
	"""
	Starts up the flask server
	"""
	port = 8080
	use_reloader = True

	# provides some configurable options
	for arg in sys.argv[1:]:
		if '--port' in arg:
			port = int(arg.split('=')[1])
		elif '--use_reloader' in arg:
			use_reloader = arg.split('=')[1] == 'true'

	app.run(host='0.0.0.0', port=port, debug=True, use_reloader=use_reloader)
