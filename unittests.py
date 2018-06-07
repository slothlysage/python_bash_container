import unittest

from command_parser import get_valid_commands, process_command_output
from main import *

from multiprocessing import Queue
from db import session
from base import Command
import json

class CommandParsingTestCase(unittest.TestCase):

	def setUp(self):
		make_db()
		self.QQ = Queue()
		self.filename = "commands.txt"
		
	def tearDown(self):
		drop_db()

	def testCommandInput(self):
		get_valid_commands(self.QQ, self.filename)
		assert self.QQ.qsize() == 7

	def testProcessCommand(self):
		while self.QQ.empty() == False:
			process_command_output(self.QQ)
		commands = session.query(Command)
		to_json = [i.serialize for i in commands.all()]
		print(json.dumps(to_json))

if __name__ == "__main__":
	unittest.main()
